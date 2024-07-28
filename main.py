import os
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from config.config import settings
from api import router as api_router
from starlette.status import HTTP_403_FORBIDDEN

SECRET_KEY = os.getenv("SUPERSECRETKEY", "Cowabunga")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == SECRET_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid API Key"
        )

app = FastAPI(
    title=settings.APP_NAME,
    description="A FastAPI project with SQLAlchemy, MySQL, and Swagger UI",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    dependencies=[Depends(get_api_key)]
)

# Include the router
app.include_router(api_router, prefix="/api")