import os
from pathlib import Path

import structlog
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from ..shared import config, db, log
from .routers import v1

os.chdir(Path(__file__).resolve().parent.parent)

cfg = config.parse(os.environ["CONFIG_PATH"])

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[cfg.main.default_ratelimit],
)

app = FastAPI(docs_url="/docs")

app.logger = structlog.get_logger()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.mount(
    "/static",
    StaticFiles(directory="/usr/src/anonqa-bot/anonqa/web/static"),
    name="static",
)

app.state.database = db
app.state.cfg = cfg

app.include_router(v1.router)


@app.get("/ping", include_in_schema=False)
async def ping() -> str:
    return "pong"


@app.get("/{html}", include_in_schema=False)
async def index(html: str) -> FileResponse:
    if (Path("web/templates") / f"{html}.html").exists():
        return FileResponse(f"web/templates/{html}.html")

    raise HTTPException(
        status_code=404,
        detail="Page not found",
    )


@app.on_event("startup")
async def startup() -> None:
    app.state.database.init()
    db = app.state.database.database
    if not db.is_connected:
        await db.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    db = app.state.database.database
    if db.is_connected:
        await db.disconnect()


log.init_web(app)
