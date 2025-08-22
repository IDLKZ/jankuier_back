from fastapi import FastAPI

from app.core.app_cors import set_up_cors
from app.core.role_docs import setup_role_documentation
from app.infrastructure.app_config import app_config
from app.middleware.registry_middleware import registry_middleware
from app.routes.registry_route import enable_routes

app = FastAPI(
    title=app_config.app_name,
    version=app_config.app_version,
    docs_url="/docs" if app_config.app_debug else None,
    redoc_url="/redoc" if app_config.app_debug else None,
)

# Middleware
registry_middleware(app)

# CORS
set_up_cors(app)

# Routes registration and role assignment
enable_routes(app)

# Role-based documentation
setup_role_documentation(app)


@app.get("/")
async def root():
    return {"message": "Jankuier Back API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
