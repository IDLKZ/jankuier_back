from app.routes.base_route import assign_roles_to_route
from app.shared.role_route_constants import RoleRouteConstant
from app.shared.route_constants import RoutePathConstants


def assign_user_code_verification_roles(app) -> None:
    base_url = f"{RoutePathConstants.BasePathName}/user-code-verification"

    # Send SMS code - Common access (can be used by anyone for verification)
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/send-code",
        roles=[RoleRouteConstant.CommonTagName]
    )

    # Verify SMS code - Common access (can be used by anyone for verification)
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/verify-code",
        roles=[RoleRouteConstant.CommonTagName]
    )