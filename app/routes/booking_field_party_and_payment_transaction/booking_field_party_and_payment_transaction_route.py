from app.routes.base_route import assign_roles_to_route
from app.shared.role_route_constants import RoleRouteConstant
from app.shared.route_constants import RoutePathConstants


def assign_booking_field_party_and_payment_transaction_roles(app) -> None:
    """
    Назначает роли для эндпоинтов связей между бронированиями площадок и платежными транзакциями.
    Все эндпоинты доступны только администраторам.
    """
    base_url = f"{RoutePathConstants.BasePathName}/booking-field-party-and-payment-transaction"

    # Pagination endpoint - Admin only
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.IndexPathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )

    # Create endpoint - Admin only
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.CreatePathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )

    # Update endpoint - Admin only
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.UpdatePathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )

    # Get by ID endpoint - Admin only
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.GetByIdPathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )

    # Delete endpoint - Admin only
    assign_roles_to_route(
        app=app,
        path=f"{base_url}{RoutePathConstants.DeleteByIdPathName}",
        roles=[RoleRouteConstant.AdministratorTagName],
    )