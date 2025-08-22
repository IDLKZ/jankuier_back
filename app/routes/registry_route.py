from app.routes.assign_roles import assign_roles_to_all_routes
from app.routes.include_routes import include_routers


def enable_routes(app):
    include_routers(app)
    assign_roles_to_all_routes(app)
