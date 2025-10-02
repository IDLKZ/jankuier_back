from app.routes.base_route import assign_roles_to_route
from app.shared.role_route_constants import RoleRouteConstant
from app.shared.route_constants import RoutePathConstants


def assign_booking_field_party_request_roles(app) -> None:
    """
    Назначает роли для эндпоинтов бронирования площадок.
    - Администраторы: полный доступ ко всем эндпоинтам
    - Клиенты: доступ к просмотру своих бронирований и созданию новых заявок
    """
    base_url = f"{RoutePathConstants.BasePathName}/booking-field-party-request"

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

    # Client Create endpoint - Client only
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/client/create",
        roles=[RoleRouteConstant.ClientTagName],
    )

    # Client Recreate endpoint - Client only
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/client/recreate/{{id}}",
        roles=[RoleRouteConstant.ClientTagName],
    )

    # Accept Payment endpoint - Common (no auth, verified by signature)
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/accept-payment",
        roles=[RoleRouteConstant.CommonTagName],
    )

    # Client My Bookings - Pagination - Client only
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/client/my",
        roles=[RoleRouteConstant.ClientTagName],
    )

    # Client My Booking by ID (GET) - Client only
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/client/my/{{id}}",
        roles=[RoleRouteConstant.ClientTagName],
    )

    # Client My Booking by ID (DELETE) - Client only
    assign_roles_to_route(
        app=app,
        path=f"{base_url}/client/my/delete/{{id}}",
        roles=[RoleRouteConstant.ClientTagName],
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