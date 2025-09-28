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

    # Administrator-only endpoints (full CRUD)
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
        path=f"{base_url}{RoutePathConstants.GetByValuePathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.DeleteByIdPathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )

    # Client endpoints - order creation for customers
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.CreatePathName}",
        roles=[RoleRouteConstant.ClientTagName],
    )