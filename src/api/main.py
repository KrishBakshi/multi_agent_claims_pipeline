from __future__ import annotations

from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router
from src.core.logger import get_logger, setup_logging
from src.core.policy_loader import get_policy_loader

load_dotenv()
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
