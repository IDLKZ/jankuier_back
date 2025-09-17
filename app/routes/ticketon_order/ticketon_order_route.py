from app.routes.base_route import assign_roles_to_route
from app.shared.role_route_constants import RoleRouteConstant
from app.shared.route_constants import RoutePathConstants


def assign_ticketon_order_roles(app) -> None:
    base_url = f"{RoutePathConstants.BasePathName}{RoutePathConstants.TicketonOrderPathName}"
    
    # Pagination endpoint - Admin only (read-only API)
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.IndexPathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )
    
    # All records endpoint - Admin only (read-only API)
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.AllPathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )
    
    # Get by ID endpoint - Admin only (read-only API)
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.GetByIdPathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )
    
    # Create sale endpoint - Public access (for ticket purchasing)
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/create-sale",
        roles=[RoleRouteConstant.ClientTagName],
    )
    
    # Recreate payment endpoint - Public access (for payment recreation)
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/recreate-payment/{{ticketon_order_id}}",
        roles=[RoleRouteConstant.ClientTagName],
    )
    
    # Confirm sale GET endpoint - Public access (for payment system callbacks)
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/confirm-sale-get",
        roles=[RoleRouteConstant.CommonTagName],
    )
    
    # Confirm sale POST endpoint - Public access (for payment system callbacks)
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/confirm-sale-post",
        roles=[RoleRouteConstant.CommonTagName],
    )
    
    # Refund sale endpoint - Client and Admin access (for ticket refunding)
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/refund-sale/{{sale}}",
        roles=[RoleRouteConstant.ClientTagName, RoleRouteConstant.AdministratorTagName],
    )

    # Check order endpoint - Client and Admin access (for order status checking)
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/check-order/{{ticketon_order_id}}",
        roles=[RoleRouteConstant.ClientTagName, RoleRouteConstant.AdministratorTagName],
    )

    # Check ticket endpoint - Client and Admin access (for ticket status checking)
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/check-ticket/{{ticketon_order_id}}/{{ticket_id}}",
        roles=[RoleRouteConstant.ClientTagName, RoleRouteConstant.AdministratorTagName],
    )

    # Client endpoints
    # Client my orders pagination - Client access only (authenticated users can view their own orders)
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/client/my-ticketon-orders",
        roles=[RoleRouteConstant.ClientTagName],
    )

    # Client get my order by ID - Client access only (authenticated users can view their own orders)
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/client/my-ticketon-order/{{id}}",
        roles=[RoleRouteConstant.ClientTagName],
    )