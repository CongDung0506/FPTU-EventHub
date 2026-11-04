# FPTU EventHub: Custom Decorators for Role-Based Access Control (RBAC)

from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user

def organizer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Vui lòng đăng nhập để truy cập trang này.", "warning")
            return redirect(url_for("login"))
        if not current_user.is_organizer:
            flash("Bạn không có quyền truy cập vào phân hệ Ban Tổ Chức.", "danger")
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Vui lòng đăng nhập để truy cập trang này.", "warning")
            return redirect(url_for("login"))
        if not current_user.is_admin:
            flash("Yêu cầu quyền Quản trị viên Phòng CTSV.", "danger")
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function
