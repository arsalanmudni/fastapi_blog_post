import os

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from blog_api.api import blog_router
from db.session import create_db_and_tables
from user_api.api import user_router
from user_api.auth import CustomMiddleware

security = HTTPBearer()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="Blog Post API with Bearer Auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",  # Use string instead of SecuritySchemeType.http
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path:
            path[method]["security"] = [{"bearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def include_routers(app):
    app.include_router(blog_router)
    app.include_router(user_router)


def start_application():
    app = FastAPI()
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="blog-api-cache")
    app.add_middleware(CustomMiddleware)
    app.openapi = custom_openapi
    include_routers(app)
    if os.getenv("TESTING") != "1":
        create_db_and_tables()
    # create_db_and_tables()
    return app


app = start_application()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)