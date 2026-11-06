# FPTU EventHub: Custom Decorators for Role-Based Access Control (RBAC)
# Trien khai day du decorator phan quyen parameterized da hoc trong PWD301

from functools import wraps
from flask import abort, flash, redirect, url_for, current_app, request, jsonify
from flask_login import current_user


def role_required(*roles):
    """
    Decorator phân quyền theo vai trò (Parameterized Decorator chuẩn PWD301):
    - Chưa đăng nhập (anonymous) -> chuyển hướng tới trang đăng nhập
    - Đã đăng nhập nhưng không thuộc danh sách vai trò cho phép -> trả về 403 Forbidden
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                if request.is_json or request.path.startswith("/api/"):
                    return jsonify({"error": "Unauthorized. Please log in first."}), 401
                flash("Vui lòng đăng nhập để truy cập trang này.", "warning")
                return redirect(url_for("login", next=request.path))
            
            user_role = current_user.role.name if current_user.role else ""
            if user_role not in roles:
                if request.is_json or request.path.startswith("/api/"):
                    return jsonify({"error": f"Forbidden. Role '{user_role}' does not have access."}), 403
                flash(f"Bạn không có quyền truy cập vào chức năng này (Yêu cầu vai trò: {', '.join(roles)}).", "danger")
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def organizer_required(f):
    """Quyền truy cập dành cho Ban Tổ Chức (Organizer) và Cán bộ CTSV (Admin)."""
    return role_required("Organizer", "Admin")(f)


def admin_required(f):
    """Quyền truy cập độc quyền dành cho Cán bộ Quản trị Phòng CTSV (Admin)."""
    return role_required("Admin")(f)
