from app.routes.base_route import assign_roles_to_route
from app.shared.role_route_constants import RoleRouteConstant
from app.shared.route_constants import RoutePathConstants


def assign_user_code_verification_roles(app) -> None:
    """Назначение ролей для эндпоинтов UserCodeVerification"""
    base_url = f"{RoutePathConstants.BasePathName}/user-code-verification"

    # Admin-only endpoints (CRUD operations)
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.IndexPathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )

    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.AllPathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )

    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.CreatePathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )

    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.UpdatePathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )

    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.GetByIdPathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )

    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.DeleteByIdPathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )

    # Public endpoints (SMS verification)
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/send-code",
        roles=[RoleRouteConstant.CommonTagName],
    )

    assign_roles_to_route(
        app=app,
        path=f"{base_url}/verify-code",
        roles=[RoleRouteConstant.CommonTagName],
    )