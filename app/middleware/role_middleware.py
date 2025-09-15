from app.core.auth_core import check_authorized_user, role_checker
from app.shared.db_value_constants import DbValueConstants

check_admin = role_checker([DbValueConstants.AdminRoleConstantValue],is_admin=True)
check_client = role_checker([DbValueConstants.ClientRoleConstantValue],is_admin=True)


check_authorized = check_authorized_user()
