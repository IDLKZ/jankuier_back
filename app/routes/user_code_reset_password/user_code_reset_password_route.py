from app.routes.base_route import assign_roles_to_route
from app.shared.role_route_constants import RoleRouteConstant
from app.shared.route_constants import RoutePathConstants


def assign_user_code_reset_password_roles(app) -> None:
    base_url = f"{RoutePathConstants.BasePathName}/user-code-reset-password"

    # Index (paginated list) - Administrator only
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.IndexPathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )

    # All (full list) - Administrator only
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.AllPathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )

    # Create - Administrator only
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.CreatePathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )

    # Update - Administrator only
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.UpdatePathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )

    # Get by ID - Administrator only
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.GetByIdPathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )

    # Delete - Administrator only
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.DeleteByIdPathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )

    # Send SMS Reset Password Code - Public endpoint (Common)
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/send-sms-reset-password-code",
        roles=[RoleRouteConstant.CommonTagName],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/verify-sms-reset-password-code",
        roles=[RoleRouteConstant.CommonTagName],
    )
