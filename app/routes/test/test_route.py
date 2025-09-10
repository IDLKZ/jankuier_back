from app.routes.base_route import assign_roles_to_route
from app.shared.role_route_constants import RoleRouteConstant
from app.shared.route_constants import RoutePathConstants


def assign_test_roles(app) -> None:
    base_url = f"{RoutePathConstants.BasePathName}test"
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.TestGetPathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.TestPostPathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )