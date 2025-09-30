from app.routes.base_route import assign_roles_to_route
from app.shared.role_route_constants import RoleRouteConstant
from app.shared.route_constants import RoutePathConstants


def assign_product_order_roles(app) -> None:
    """
    Assigns role-based access control to ProductOrder API endpoints.

    Role assignments:
    - Administrator: Full CRUD access to all product order endpoints
    - Client: Access to create order endpoint for placing orders

    Args:
        app: FastAPI application instance
    """
    base_url = f"{RoutePathConstants.BasePathName}/product-order"

    # # Administrator-only endpoints (full CRUD)
    # assign_roles_to_route(
    #     app=app,
    #     path=f"{base_url}{RoutePathConstants.IndexPathName}",
    #     roles=[RoleRouteConstant.AdministratorTagName],
    # )
    # assign_roles_to_route(
    #     app=app,
    #     path=f"{base_url}{RoutePathConstants.AllPathName}",
    #     roles=[RoleRouteConstant.AdministratorTagName],
    # )
    # assign_roles_to_route(
    #     app=app,
    #     path=f"{base_url}{RoutePathConstants.UpdatePathName}",
    #     roles=[RoleRouteConstant.AdministratorTagName],
    # )
    # assign_roles_to_route(
    #     app=app,
    #     path=f"{base_url}{RoutePathConstants.GetByIdPathName}",
    #     roles=[RoleRouteConstant.AdministratorTagName],
    # )
    # assign_roles_to_route(
    #     app=app,
    #     path=f"{base_url}{RoutePathConstants.GetByValuePathName}",
    #     roles=[RoleRouteConstant.AdministratorTagName],
    # )
    # assign_roles_to_route(
    #     app=app,
    #     path=f"{base_url}{RoutePathConstants.DeleteByIdPathName}",
    #     roles=[RoleRouteConstant.AdministratorTagName],
    # )

    # Client endpoints - order creation and payment recreation for customers
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/create-order-from-cart",
        roles=[RoleRouteConstant.ClientTagName],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/recreate-payment/{{id}}",
        roles=[RoleRouteConstant.ClientTagName],
    )

    # Client endpoints - order viewing and management for customers
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/client-my-orders",
        roles=[RoleRouteConstant.ClientTagName],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/client-my-order/{{id}}",
        roles=[RoleRouteConstant.ClientTagName],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/client-my-order-items/{{id}}",
        roles=[RoleRouteConstant.ClientTagName],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/client-cancel-or-delete-order/{{id}}",
        roles=[RoleRouteConstant.ClientTagName],
    )

    # Common endpoint - payment callback from Alatau Pay (no authentication required)
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/accept-payment",
        roles=[RoleRouteConstant.CommonTagName],
    )

    # Client endpoint - cancel specific order item
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/client-cancel-order-item/{{order_item_id}}",
        roles=[RoleRouteConstant.ClientTagName],
    )