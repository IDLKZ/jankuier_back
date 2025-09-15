from app.routes.base_route import assign_roles_to_route
from app.shared.role_route_constants import RoleRouteConstant
from app.shared.route_constants import RoutePathConstants


def assign_user_cart_roles(app) -> None:
    """
    Назначает роли для API корзины пользователя.
    
    Права доступа:
    - Получение корзины: Клиенты и Администраторы
    - Добавление в корзину: Клиенты и Администраторы
    - Удаление из корзины: Клиенты и Администраторы  
    - Очистка корзины: Клиенты и Администраторы
    """
    base_url = f"{RoutePathConstants.BasePathName}{RoutePathConstants.UserCartPathName}"
    
    # GET /api/user-cart/get/{user_id} - Получить корзину пользователя
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/get",
        roles=[
            RoleRouteConstant.AdministratorTagName,
            RoleRouteConstant.ClientTagName,
        ],
    )
    
    # POST /api/user-cart/add/{user_id} - Добавить товар в корзину
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/add",
        roles=[
            RoleRouteConstant.AdministratorTagName,
            RoleRouteConstant.ClientTagName,
        ],
    )
    
    # POST /api/user-cart/remove/{user_id} - Удалить товар из корзины
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/remove",
        roles=[
            RoleRouteConstant.AdministratorTagName,
            RoleRouteConstant.ClientTagName,
        ],
    )
    
    # DELETE /api/user-cart/clear/{user_id} - Очистить корзину
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/clear",
        roles=[
            RoleRouteConstant.AdministratorTagName,
            RoleRouteConstant.ClientTagName,
        ],
    )