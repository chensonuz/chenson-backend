from app.admin.auth import RoleChecker
from app.user.models import UserRole

is_admin = RoleChecker([UserRole.Admin])
