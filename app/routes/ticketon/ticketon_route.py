from app.routes.base_route import assign_roles_to_route
from app.shared.role_route_constants import RoleRouteConstant
from app.shared.route_constants import RoutePathConstants


def assign_ticketon_roles(app) -> None:
    """
    Назначение ролей для маршрутов Ticketon API.
    
    Ticketon API предоставляет доступ к внешним данным о сеансах и мероприятиях.
    Данные доступны всем авторизованным пользователям (администраторы и клиенты).
    """
    base_url = f"{RoutePathConstants.BasePathName}/ticketon"
    
    # GET /api/ticketon/shows - Получение данных о сеансах
    # Доступно администраторам и клиентам, так как это публичные данные о мероприятиях
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/shows",
        roles=[RoleRouteConstant.AdministratorTagName, RoleRouteConstant.ClientTagName],
    )
    
    # GET /api/ticketon/show/{show_id} - Получение подробной информации о сеансе
    # Доступно администраторам и клиентам для просмотра деталей конкретного сеанса
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/show/{{show_id}}",
        roles=[RoleRouteConstant.AdministratorTagName, RoleRouteConstant.ClientTagName],
    )