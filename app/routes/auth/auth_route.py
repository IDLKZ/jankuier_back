from app.routes.base_route import assign_roles_to_route
from app.shared.role_route_constants import RoleRouteConstant
from app.shared.route_constants import RoutePathConstants


def assign_auth_roles(app) -> None:
    """
    Начало блока Роли включающих в себя создание обновление удаление весь список получение по айди и значению
    """
    base_url = f"{RoutePathConstants.BasePathName}{RoutePathConstants.AuthPathName}"

    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.LoginPathName}",
        roles=[
            RoleRouteConstant.AdministratorTagName,
            RoleRouteConstant.CommonTagName,
        ],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.RegisterPathName}",
        roles=[
            RoleRouteConstant.AdministratorTagName,
            RoleRouteConstant.CommonTagName,
        ],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.RefreshTokenPathName}",
        roles=[
            RoleRouteConstant.AdministratorTagName,
            RoleRouteConstant.CommonTagName,
        ],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.GetMePathName}",
        roles=[
            RoleRouteConstant.AdministratorTagName,
            RoleRouteConstant.CommonTagName,
        ],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.ResetPasswordPathName}",
        roles=[
            RoleRouteConstant.AdministratorTagName,
            RoleRouteConstant.CommonTagName,
        ],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.UpdateProfilePathName}",
        roles=[
            RoleRouteConstant.AdministratorTagName,
            RoleRouteConstant.ClientTagName,
        ],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.UpdatePasswordPathName}",
        roles=[
            RoleRouteConstant.AdministratorTagName,
            RoleRouteConstant.ClientTagName,
        ],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.UpdateProfilePhotoPathName}",
        roles=[
            RoleRouteConstant.AdministratorTagName,
            RoleRouteConstant.ClientTagName,
        ],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.DeleteProfilePhotoPathName}",
        roles=[
            RoleRouteConstant.AdministratorTagName,
            RoleRouteConstant.ClientTagName,
        ],
    )
