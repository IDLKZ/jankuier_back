from app.routes.base_route import assign_roles_to_route
from app.shared.role_route_constants import RoleRouteConstant
from app.shared.route_constants import RoutePathConstants


def assign_academy_roles(app) -> None:
    base_url = f"{RoutePathConstants.BasePathName}/academy"
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.IndexPathName}",
        roles=[
            RoleRouteConstant.AdministratorTagName,
            RoleRouteConstant.ClientTagName,
        ],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.AllPathName}",
        roles=[
            RoleRouteConstant.AdministratorTagName,
            RoleRouteConstant.ClientTagName,
        ],
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
        roles=[
            RoleRouteConstant.AdministratorTagName,
            RoleRouteConstant.ClientTagName,
        ],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.GetByValuePathName}",
        roles=[
            RoleRouteConstant.AdministratorTagName,
            RoleRouteConstant.ClientTagName,
        ],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.DeleteByIdPathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )