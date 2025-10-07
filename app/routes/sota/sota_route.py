from typing import List

from app.routes.base_route import assign_roles_to_route
from app.shared.role_route_constants import RoleRouteConstant
from app.shared.route_constants import RoutePathConstants


def assign_sota_roles(app) -> None:
    base_url = f"{RoutePathConstants.BasePathName}/sota"
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/registers/countries",
        roles=[RoleRouteConstant.CommonTagName],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/registers/tournaments",
        roles=[RoleRouteConstant.CommonTagName],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/public/v1/games",
        roles=[RoleRouteConstant.CommonTagName],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}" + "/public/v1/seasons/{seasonId}/score_table",
        roles=[RoleRouteConstant.CommonTagName],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}" + "/public/v1/games/{gameId}/teams",
        roles=[RoleRouteConstant.CommonTagName],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}" + "/public/v1/games/{gameId}/players",
        roles=[RoleRouteConstant.CommonTagName],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}" + "/public/v1/games/{gameId}/pre_game_lineup",
        roles=[RoleRouteConstant.CommonTagName],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/preload-data",
        roles=[RoleRouteConstant.AdministratorTagName],
    )