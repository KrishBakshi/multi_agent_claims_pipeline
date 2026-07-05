"""LangSmith tracing configuration for the claims pipeline.

LangGraph runs and LangChain LLM calls are traced automatically when enabled.
Non-LangChain paths (e.g. Gemini Vision OCR) use ``@traceable`` decorators.

Enable tracing via environment variables (see ``.env.example``):

    LANGSMITH_TRACING=true
    LANGSMITH_API_KEY=lsv2_...
    LANGSMITH_PROJECT=claims-pipeline
    LANGSMITH_ENDPOINT=https://apac.api.smith.langchain.com

Legacy ``LANGCHAIN_*`` names are also accepted and normalised at startup.

Call ``configure_langsmith()`` before importing pipeline modules so the
global LangSmith client uses the correct regional endpoint (APAC vs US).
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from langchain_core.runnables import RunnableConfig

from src.core.logger import get_logger

_log = get_logger("core.tracing")

_ROOT = Path(__file__).resolve().parent.parent.parent
_TRUTHY = frozenset({"1", "true", "yes", "on"})
_DEFAULT_ENDPOINT = "https://api.smith.langchain.com"


def _is_truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in _TRUTHY


def _strip_env(value: str) -> str:
    return value.strip().strip('"').strip("'")


def _load_env() -> None:
    """Load ``.env`` from the project root (no-op if python-dotenv missing)."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv(_ROOT / ".env", override=False)


def _mirror_env(primary: str, fallback: str) -> str | None:
    """Read either env name and write the value to both (force, not setdefault)."""
    raw = os.getenv(primary) or os.getenv(fallback)
    if not raw or not _strip_env(raw):
        return None
    value = _strip_env(raw)
    os.environ[primary] = value
    os.environ[fallback] = value
    return value


def _clear_langsmith_caches() -> None:
    try:
        from langsmith.utils import get_env_var, get_tracer_project

        get_env_var.cache_clear()
        get_tracer_project.cache_clear()
    except Exception:
        pass


def _configure_langsmith_client(
    *,
    api_key: str,
    api_url: str,
    project: str | None,
) -> None:
    """Bind a global LangSmith client so all traces use the chosen endpoint."""
    import langsmith as ls
    from langsmith import Client

    client = Client(api_url=api_url.rstrip("/"), api_key=api_key)
    ls.configure(
        client=client,
        enabled=True,
        project_name=project,
    )


def is_tracing_enabled() -> bool:
    """Return True when LangSmith tracing is turned on."""
    return _is_truthy(os.getenv("LANGSMITH_TRACING")) or _is_truthy(
        os.getenv("LANGCHAIN_TRACING_V2")
    )


def get_langsmith_endpoint() -> str:
    """Return the configured LangSmith API endpoint (after ``configure_langsmith``)."""
    return (
        _strip_env(os.getenv("LANGSMITH_ENDPOINT") or os.getenv("LANGCHAIN_ENDPOINT") or "")
        or _DEFAULT_ENDPOINT
    )


def configure_langsmith() -> bool:
    """Load env, normalise LangSmith settings, and register the global client.

    Returns:
        True when tracing is enabled and an API key is present.
    """
    _load_env()

    api_key = _mirror_env("LANGSMITH_API_KEY", "LANGCHAIN_API_KEY")
    project = _mirror_env("LANGSMITH_PROJECT", "LANGCHAIN_PROJECT")
    endpoint = _mirror_env("LANGSMITH_ENDPOINT", "LANGCHAIN_ENDPOINT")

    tracing_requested = _is_truthy(
        os.getenv("LANGSMITH_TRACING") or os.getenv("LANGCHAIN_TRACING_V2")
    )
    if tracing_requested:
        os.environ["LANGSMITH_TRACING"] = "true"
        os.environ["LANGCHAIN_TRACING_V2"] = "true"

    _clear_langsmith_caches()

    if not is_tracing_enabled():
        _log.debug("LangSmith tracing disabled")
        return False

    if not api_key:
        _log.warning(
            "LangSmith tracing is enabled but LANGSMITH_API_KEY is not set — "
            "traces will not be exported"
        )
        return False

    api_url = endpoint or _DEFAULT_ENDPOINT
    # Ensure both names are set before any Client() is constructed.
    os.environ["LANGSMITH_ENDPOINT"] = api_url
    os.environ["LANGCHAIN_ENDPOINT"] = api_url

    _configure_langsmith_client(api_key=api_key, api_url=api_url, project=project)

    _log.info(
        "LangSmith tracing enabled — project=%s endpoint=%s",
        project or "default",
        api_url,
    )
    return True


def build_run_config(claim_id: str, claim_input: dict[str, Any]) -> RunnableConfig:
    """Build a LangGraph ``RunnableConfig`` with claim metadata for LangSmith."""
    tags = [
        "claims-pipeline",
        str(claim_input.get("claim_category") or "UNKNOWN"),
    ]
    if claim_input.get("simulate_component_failure"):
        tags.append("simulated-failure")

    return RunnableConfig(
        run_name=f"claim-{claim_id}",
        tags=tags,
        metadata={
            "claim_id": claim_id,
            "member_id": claim_input.get("member_id"),
            "policy_id": claim_input.get("policy_id"),
            "claim_category": claim_input.get("claim_category"),
            "claimed_amount": claim_input.get("claimed_amount"),
            "treatment_date": str(claim_input.get("treatment_date")),
            "document_count": len(claim_input.get("documents") or []),
            "simulate_component_failure": claim_input.get(
                "simulate_component_failure", False
            ),
        },
    )


def redact_document_inputs(inputs: dict[str, Any]) -> dict[str, Any]:
    """Strip binary payloads from trace inputs (used by ``@traceable``)."""
    redacted = dict(inputs)
    doc = redacted.get("doc")
    if isinstance(doc, dict) and "file_data" in doc:
        file_data = doc["file_data"]
        size = len(file_data) if isinstance(file_data, (bytes, bytearray)) else "unknown"
        redacted["doc"] = {
            **doc,
            "file_data": f"<{size} bytes redacted>",
        }
    return redacted
