from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv

# Load env and LangSmith client before any pipeline/langsmith imports.
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

from src.core.tracing import configure_langsmith  # noqa: E402

configure_langsmith()

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402

from src.api.routes import router  # noqa: E402
from src.core.logger import get_logger, setup_logging  # noqa: E402
from src.core.policy_loader import get_policy_loader  # noqa: E402

setup_logging()


_log = get_logger("api.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    _log.info("API starting up — warming policy loader")
    get_policy_loader()
    _log.info("Policy loaded — ready to serve claims")
    yield
    _log.info("API shutting down")


app = FastAPI(
    title="Multi-Agent Claims Pipeline",
    description="Health insurance claims processing via LangGraph agents",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")
