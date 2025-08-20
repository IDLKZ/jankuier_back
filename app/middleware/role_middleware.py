from app.core.auth_core import check_authorized_user, role_checker
from app.shared.db_value_constants import DbValueConstants

check_club_admin = role_checker([DbValueConstants.AdminRoleConstantValue])


check_authorized = check_authorized_user()
