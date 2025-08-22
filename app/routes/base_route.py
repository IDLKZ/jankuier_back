def assign_roles_to_route(app, path, roles) -> None:
    """
    Назначает роли для конкретного маршрута приложения.
    Если маршрут уже содержит список ролей, то добавляет новые роли к существующим.
    Если список ролей отсутствует, он создаётся.
    Args:
        app: Приложение FastAPI, в котором находятся маршруты.
        path: Путь маршрута, для которого назначаются роли.
        roles: Список ролей, которые необходимо назначить маршруту.
    Returns:
        None
    """
    for route in app.routes:
        if route.path == path:
            if hasattr(route, "roles"):
                route.roles.extend(roles)
            else:
                route.roles = roles
            return
