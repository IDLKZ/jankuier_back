from fastapi import FastAPI

from app.adapters.api.category_modification.category_modification_api import (
    CategoryModificationApi,
)
from app.adapters.api.city.city_api import CityApi
from app.adapters.api.country.country_api import CountryApi
from app.adapters.api.modification_type.modification_type_api import ModificationTypeApi
from app.adapters.api.modification_value.modification_value_api import (
    ModificationValueApi,
)
from app.adapters.api.permission.permission_api import PermissionApi
from app.adapters.api.product.product_api import ProductApi
from app.adapters.api.product_category.product_category_api import ProductCategoryApi
from app.adapters.api.product_variant.product_variant_api import ProductVariantApi
from app.adapters.api.product_variant_modification.product_variant_modification_api import (
    ProductVariantModificationApi,
)
from app.adapters.api.role.role_api import RoleApi
from app.adapters.api.sport.sport_api import SportApi
from app.adapters.api.user.user_api import UserApi
from app.core.app_cors import set_up_cors
from app.core.role_docs import setup_role_documentation
from app.infrastructure.app_config import app_config
from app.middleware.registry_middleware import registry_middleware
from app.shared.route_constants import RoutePathConstants

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

# API Routes
app.include_router(
    CategoryModificationApi().router,
    prefix=f"{RoutePathConstants.BasePathName}/category-modification",
    tags=["Модификации категорий"],
)

app.include_router(
    CityApi().router,
    prefix=f"{RoutePathConstants.BasePathName}/city",
    tags=["Города"],
)

app.include_router(
    CountryApi().router,
    prefix=f"{RoutePathConstants.BasePathName}/country",
    tags=["Страны"],
)

app.include_router(
    ModificationTypeApi().router,
    prefix=f"{RoutePathConstants.BasePathName}/modification-type",
    tags=["Типы модификаций"],
)

app.include_router(
    ModificationValueApi().router,
    prefix=f"{RoutePathConstants.BasePathName}/modification-value",
    tags=["Значения модификаций"],
)

app.include_router(
    PermissionApi().router,
    prefix=f"{RoutePathConstants.BasePathName}{RoutePathConstants.PermissionPathName}",
    tags=[RoutePathConstants.PermissionTagName],
)

app.include_router(
    ProductApi().router,
    prefix=f"{RoutePathConstants.BasePathName}/product",
    tags=["Товары"],
)

app.include_router(
    ProductCategoryApi().router,
    prefix=f"{RoutePathConstants.BasePathName}/product-category",
    tags=["Категории товаров"],
)

app.include_router(
    ProductVariantApi().router,
    prefix=f"{RoutePathConstants.BasePathName}/product-variant",
    tags=["Варианты товаров"],
)

app.include_router(
    ProductVariantModificationApi().router,
    prefix=f"{RoutePathConstants.BasePathName}/product-variant-modification",
    tags=["Модификации вариантов товаров"],
)

app.include_router(
    RoleApi().router,
    prefix=f"{RoutePathConstants.BasePathName}{RoutePathConstants.RolePathName}",
    tags=[RoutePathConstants.RoleTagName],
)

app.include_router(
    SportApi().router,
    prefix=f"{RoutePathConstants.BasePathName}/sport",
    tags=["Виды спорта"],
)

app.include_router(
    UserApi().router,
    prefix=f"{RoutePathConstants.BasePathName}{RoutePathConstants.UserPathName}",
    tags=[RoutePathConstants.UserTagName],
)

# Role-based documentation
setup_role_documentation(app)


@app.get("/")
async def root():
    return {"message": "Jankuier Back API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
