from flask import Blueprint
from flask_login import login_required

admin_bp = Blueprint("admin", __name__, template_folder="../../templates/admin")


@admin_bp.before_request
@login_required
def require_login():
    """Every admin route requires an authenticated session."""
    pass


from app.blueprints.admin import routes  # noqa: E402,F401
