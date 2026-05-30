import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from alembic.config import Config
from alembic import command

from app.api.routes import router as api_router
from app.core.database import get_database_url

logger = logging.getLogger(__name__)


def run_migrations() -> None:
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", get_database_url())
    logger.info("Running database migrations...")
    command.upgrade(alembic_cfg, "head")
    logger.info("Database migrations complete.")


app = FastAPI(title="AdPeek-Server")

app.add_middleware(
    CORSMiddleware,
        allow_origins=[
        "http://localhost:5173",
        "https://adpeek-client.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    run_migrations()


@app.get("/")
def root():
    return {"message": "AdPeek-Server"}