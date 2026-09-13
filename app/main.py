from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from sqlalchemy import text
from swagger_ui_bundle import swagger_ui_path

from app.core.config import settings
from app.core.throttle import limiter
from app.infrastructure.database.seed import seed_initial_users
from app.infrastructure.database.session import engine
from app.infrastructure.services.security.password_hasher_impl import (
    Argon2PasswordHasher,
)
from app.infrastructure.utils.logging import configure_logging
from app.presentation.graphql.router import graphql_app
from app.presentation.rest.errors.handlers import app_exception_handler
from app.presentation.rest.routers.auth_router import router as auth_router
from app.presentation.rest.routers.user_router import router as user_router
from app.presentation.rest.utils.dependencies import get_uow
from app.presentation.rest.utils.trace_id import TraceIDMiddleware
from app.utils.app_exception import AppException


@asynccontextmanager
async def lifespan(_app: FastAPI):
    uow = get_uow()
    password_hasher = Argon2PasswordHasher()
    await seed_initial_users(uow=uow, password_hasher=password_hasher)
    yield


def _docs_url() -> str | None:
    return None


def _redoc_url() -> str | None:
    return settings.SWAGGER_REDOC_PATH if settings.docs_enabled else None


def _openapi_url() -> str | None:
    return settings.SWAGGER_OPENAPI_PATH if settings.docs_enabled else None


app = FastAPI(
    lifespan=lifespan,
    title="FastAPI Core Clean",
    version=settings.APP_VERSION,
    docs_url=_docs_url(),
    redoc_url=_redoc_url(),
    openapi_url=_openapi_url(),
    openapi_version="3.0.3",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

if settings.docs_enabled:
    app.mount("/swagger", StaticFiles(directory=swagger_ui_path), name="swagger")

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        openapi_schema["openapi"] = "3.0.3"
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi  # type: ignore[method-assign]

    @app.get(settings.SWAGGER_DOCS_PATH, include_in_schema=False)
    async def custom_swagger_ui():
        return get_swagger_ui_html(
            openapi_url=settings.SWAGGER_OPENAPI_PATH,
            title="API Docs",
            swagger_js_url="/swagger/swagger-ui-bundle.js",
            swagger_css_url="/swagger/swagger-ui.css",
        )


@app.get("/health")
async def health():
    timestamp = datetime.now(UTC).isoformat()
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "ok",
            "timestamp": timestamp,
        }
    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unavailable",
                "database": "unavailable",
                "timestamp": timestamp,
            },
        )


app.add_middleware(TraceIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, app_exception_handler)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(graphql_app, prefix="/graphql")

configure_logging()
