# FPTU EventHub: Main Application
# Hệ thống Quản lý & Đăng ký Sự kiện Sinh viên FPT University (events.fptu.vn)
# Tích hợp ĐẦY ĐỦ 100% các hàm, phương thức, thư viện và kiến trúc đã học trong chương trình PWD301:
# - Flask Core, Routing, Error Handlers, Custom Jinja Filters, Context Processors, PRG Pattern
# - Flask-Login, Session Security, Open Redirect Prevention (is_safe_url)
# - Flask-WTF Forms, Custom Validators (Phone, MSSV, FPT Domain), CSRF Protection
# - SQLAlchemy ORM: 100% Model Querying, CRUD, Pagination, Relationships, Transactions & Rollback
# - Role-Based Access Control (RBAC): @role_required, @admin_required, @organizer_required
# - Full RESTful API v1 (GET, POST, PUT, DELETE) với HTTP Status Codes chuẩn (200, 201, 204, 400, 401, 403, 404, 422, 500)
# - XSS Protection (Bleach HTML Sanitizer) & Password Hashing (Werkzeug PBKDF2/SHA-256)

import os
import re
import csv
import io
import tempfile
import urllib.parse
from datetime import datetime, timedelta
from flask import (
    Flask, render_template, redirect, url_for, request, flash, 
    abort, jsonify, Response, send_from_directory, make_response
)
from flask_bootstrap import Bootstrap
from flask_login import (
    LoginManager, login_required, current_user, login_user, logout_user
)

from models import db, User, Role, Category, Event, Ticket, Review
from markdown_utils import render_safe_markdown
from decorators import role_required, organizer_required, admin_required
from forms import (
    LoginForm, RegisterForm, EventCreateForm, EventEditForm, 
    CategoryForm, ProfileForm, ChangePasswordForm, CheckInManualForm, ReviewForm
)

app = Flask(__name__)
Bootstrap(app)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "fptu-eventhub-secret-key-2026")

# Database configuration linh hoạt cho cả Localhost và Cloud (Vercel)
is_serverless = bool(
    os.environ.get("VERCEL") or 
    os.environ.get("VERCEL_ENV") or 
    os.environ.get("AWS_LAMBDA_FUNCTION_NAME") or 
    os.environ.get("LAMBDA_TASK_ROOT") or 
    os.path.exists("/var/task")
)

if is_serverless:
    db_path = os.path.join(tempfile.gettempdir(), "fptu_eventhub.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
elif os.environ.get("DATABASE_URL"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    try:
        import pyodbc
        DB_SERVER = os.environ.get("DB_SERVER", ".")
        DB_NAME = os.environ.get("DB_NAME", "FPTU_EventHub_DB")
        DB_DRIVER = os.environ.get("DB_DRIVER", "ODBC Driver 17 for SQL Server")
        test_conn = f"DRIVER={{{DB_DRIVER}}};SERVER={DB_SERVER};DATABASE={DB_NAME};Trusted_Connection=yes;TrustServerCertificate=yes;"
        with pyodbc.connect(test_conn, timeout=1):
            pass
        params = urllib.parse.quote_plus(test_conn)
        app.config["SQLALCHEMY_DATABASE_URI"] = f"mssql+pyodbc:///?odbc_connect={params}"
    except Exception:
        if is_serverless or not os.access(".", os.W_OK):
            db_path = os.path.join(tempfile.gettempdir(), "fptu_eventhub.db")
            app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
        else:
            app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fptu_eventhub.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "Vui lòng đăng nhập bằng tài khoản FPT để thực hiện thao tác."
login_manager.login_message_category = "warning"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except Exception:
        return None


# --- Helper: Phòng chống lỗ hổng Open Redirect (Bài Lab 6 PWD301) ------------
def is_safe_url(target):
    """Xác thực URL chuyển hướng nội bộ an toàn, ngăn chặn tấn công Open Redirect."""
    if not target:
        return False
    ref_url = urllib.parse.urlparse(request.host_url)
    test_url = urllib.parse.urlparse(urllib.parse.urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


# --- Custom Jinja2 Template Filters (Đã học trong PWD301) ---------------------
@app.template_filter("vnd")
def vnd_filter(value):
    """Bộ lọc định dạng tiền tệ Việt Nam Đồng (VND)."""
    if value is None or value == "":
        return "-"
    try:
        val_int = int(round(float(value)))
        return f"{val_int:,}".replace(",", ".") + " đ"
    except (ValueError, TypeError):
        return "-"

@app.template_filter("datetime_format")
def datetime_format_filter(value, fmt="%H:%M - %d/%m/%Y"):
    """Bộ lọc định dạng thời gian chuẩn Việt Nam."""
    if not value or not isinstance(value, datetime):
        return ""
    return value.strftime(fmt)

@app.template_filter("timeago")
def timeago_filter(value):
    """Bộ lọc hiển thị thời gian tương đối."""
    if not value or not isinstance(value, datetime):
        return ""
    now = datetime.utcnow()
    diff = value - now
    if diff.total_seconds() > 0:
        days = diff.days
        hours = int(diff.seconds // 3600)
        if days > 0:
            return f"Còn {days} ngày nữa"
        elif hours > 0:
            return f"Còn {hours} giờ nữa"
        return "Sắp diễn ra"
    else:
        past = now - value
        days = past.days
        if days == 0:
            return "Hôm nay"
        elif days == 1:
            return "Hôm qua"
        return f"{days} ngày trước"

@app.template_filter("truncate_words")
def truncate_words_filter(s, num=25):
    """Cắt ngắn chuỗi văn bản theo số từ."""
    if not s:
        return ""
    words = str(s).split()
    if len(words) <= num:
        return s
    return " ".join(words[:num]) + "..."


# --- Global Context Processor (Tiêm dữ liệu dùng chung vào toàn bộ Jinja2) ----
@app.context_processor
def inject_global_data():
    return {
        "current_year": datetime.utcnow().year,
        "is_safe_url": is_safe_url,
        "nav_categories": Category.query.order_by(Category.id.asc()).all
    }


# --- Custom Error Handlers (Hỗ trợ cả Giao diện HTML lẫn Phản hồi JSON) -------
@app.errorhandler(400)
def handle_bad_request(e):
    if request.is_json or request.path.startswith("/api/"):
        return jsonify({"error": "Bad Request", "message": getattr(e, "description", "Yêu cầu không hợp lệ.")}), 400
    return render_template("400.html"), 400

@app.errorhandler(403)
def handle_forbidden(e):
    if request.is_json or request.path.startswith("/api/"):
        return jsonify({"error": "Forbidden", "message": "Bạn không có quyền truy cập tài nguyên này."}), 403
    return render_template("403.html"), 403

@app.errorhandler(404)
def handle_not_found(e):
    if request.is_json or request.path.startswith("/api/"):
        return jsonify({"error": "Not Found", "message": "Không tìm thấy tài nguyên yêu cầu."}), 404
    return render_template("404.html"), 404

@app.errorhandler(500)
def handle_server_error(e):
    db.session.rollback()
    if request.is_json or request.path.startswith("/api/"):
        return jsonify({"error": "Internal Server Error", "message": "Lỗi máy chủ nội bộ."}), 500
    return render_template("500.html"), 500


# --- Database Auto-Init & Seed -----------------------------------------------
@app.before_request
def auto_init_database():
    if app.config.get("TESTING"):
        return
    try:
        db.create_all()
        if Role.query.first() is None:
            Role.insert_roles()
        if User.query.count() < 10 or Event.query.count() < 5 or Ticket.query.count() < 30:
            from seed_events import seed_data_internal
            seed_data_internal()
    except Exception as e:
        db.session.rollback()
        pass

@app.before_request
def require_fpt_login():
    # Bắt buộc đăng nhập trước khi xem cổng sự kiện
    if not request.endpoint:
        return None
    public_endpoints = (
        "login", "quick_login", "register", "static", "serve_static_fallback",
        "api_events_list", "api_event_detail", "api_categories", "api_stats", "api_auth_login"
    )
    if request.endpoint in public_endpoints:
        return None
    if not current_user.is_authenticated:
        return redirect(url_for("login"))


# --- Authentication Routes (Zero-SSO & Session Management) -------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        ident = form.email.data.strip()
        if "@" in ident:
            if not (ident.lower().endswith("@fpt.edu.vn") or ident.lower().endswith("@fe.edu.vn")):
                flash("❌ Email không thuộc hệ thống Đại học FPT! Vui lòng sử dụng email trường cấp (@fpt.edu.vn / @fe.edu.vn) hoặc Mã SV (MSSV).", "danger")
                return render_template("login.html", form=form)
        
        user = User.query.filter(
            (User.email.ilike(ident)) | 
            (User.student_id.ilike(ident))
        ).first()
        pwd = form.password.data.strip()
        
        if user:
            if user.check_password(pwd):
                login_user(user, remember=form.remember_me.data)
                flash(f"Chào mừng {user.full_name} ({user.role.name}) quay trở lại!", "success")
                next_page = request.args.get("next")
                if next_page and is_safe_url(next_page):
                    return redirect(next_page)
                return redirect(url_for("home"))
            else:
                flash("Mật khẩu không chính xác. Vui lòng thử lại (mật khẩu mặc định: pass123).", "danger")
        else:
            # Auto-provision student account for valid FPT email domain (Zero Registration needed)
            if "@" in ident and (ident.lower().endswith("@fpt.edu.vn") or ident.lower().endswith("@fe.edu.vn")):
                email_clean = ident.lower()
                role_student = Role.query.filter_by(name="Student").first()
                m = re.search(r"([a-zA-Z]{2}\d{6})", email_clean)
                mssv = m.group(1).upper() if m else f"FU{int(datetime.utcnow().timestamp()) % 1000000}"
                username_part = email_clean.split("@")[0]
                name_guess = username_part.replace(".", " ").title()

                new_user = User(
                    student_id=mssv,
                    full_name=name_guess,
                    email=email_clean,
                    role=role_student,
                    avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80"
                )
                new_user.set_password(pwd if len(pwd) >= 6 else "pass123")
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=form.remember_me.data)
                flash(f"🎉 Chào mừng sinh viên FPT {new_user.full_name} ({new_user.student_id}) đăng nhập thành công!", "success")
                return redirect(url_for("home"))
            else:
                flash("Không tìm thấy tài khoản FPT hoặc MSSV này. Vui lòng sử dụng đúng email trường cấp (@fpt.edu.vn).", "danger")
    return render_template("login.html", form=form)

@app.route("/login/quick/<role_type>")
def quick_login(role_type):
    auto_init_database()
    rt = role_type.lower().strip()
    user = None
    if rt == "student":
        user = User.query.filter(
            (User.email == "dungtcde200433@fpt.edu.vn") | 
            (User.student_id == "DE200433")
        ).first()
        if not user:
            role_student = Role.query.filter_by(name="Student").first()
            if not role_student:
                Role.insert_roles()
                role_student = Role.query.filter_by(name="Student").first()
            try:
                user = User(
                    student_id="DE200433",
                    full_name="Trương Công Dũng",
                    email="dungtcde200433@fpt.edu.vn",
                    phone="0905123456",
                    avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80",
                    role=role_student
                )
                user.set_password("pass123")
                db.session.add(user)
                db.session.commit()
            except Exception:
                db.session.rollback()
                user = User.query.filter((User.student_id == "DE200433") | (User.email == "dungtcde200433@fpt.edu.vn")).first()
                if not user:
                    user = User.query.filter(User.role.has(name="Student")).first()
    elif rt in ("admin", "organizer"):
        user = User.query.filter(
            (User.email == "ctsv.admin@fpt.edu.vn") | 
            (User.student_id == "ADM001")
        ).first()
        if not user:
            role_admin = Role.query.filter_by(name="Admin").first()
            if not role_admin:
                Role.insert_roles()
                role_admin = Role.query.filter_by(name="Admin").first()
            try:
                user = User(
                    student_id="ADM001",
                    full_name="Phòng Công Tác Sinh Viên (CTSV)",
                    email="ctsv.admin@fpt.edu.vn",
                    phone="02367300999",
                    avatar_url="/static/images/fpt_logo.jpg",
                    role=role_admin
                )
                user.set_password("pass123")
                db.session.add(user)
                db.session.commit()
            except Exception:
                db.session.rollback()
                user = User.query.filter((User.student_id == "ADM001") | (User.email == "ctsv.admin@fpt.edu.vn")).first()
                if not user:
                    user = User.query.filter(User.role.has(name="Admin")).first()

    # Fallback dự phòng tối cao: Nếu vẫn chưa có user, lấy bất kỳ user hợp lệ
    if not user:
        if rt == "student":
            user = User.query.filter(User.role.has(name="Student")).first()
        elif rt in ("admin", "organizer"):
            user = User.query.filter(User.role.has(name="Admin")).first() or User.query.first()

    if user:
        login_user(user, remember=True)
        flash(f"🎉 Đăng nhập thành công: {user.full_name} ({user.role.name})!", "success")
        if user.is_admin:
            return redirect(url_for("admin_dashboard"))
        elif user.is_organizer:
            return redirect(url_for("organizer_dashboard"))
        return redirect(url_for("home"))

    flash("Không tìm thấy tài khoản mẫu trong cơ sở dữ liệu.", "danger")
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    flash("🎓 Sinh viên & Cán bộ ĐH FPT không cần đăng ký tài khoản mới! Bạn chỉ cần đăng nhập bằng Email trường cấp (@fpt.edu.vn) hoặc Mã SV (MSSV).", "info")
    return redirect(url_for("login"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Bạn đã đăng xuất an toàn khỏi FPTU EventHub.", "info")
    return redirect(url_for("home"))


# --- User Profile & Password Change (Bài Lab 6 PWD301) ------------------------
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data.strip()
        current_user.phone = form.phone.data.strip() if form.phone.data else None
        if form.avatar_url.data:
            current_user.avatar_url = form.avatar_url.data.strip()
        db.session.commit()
        flash("Cập nhật thông tin cá nhân thành công!", "success")
        return redirect(url_for("profile"))
    return render_template("profile.html", form=form)

@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash("Mật khẩu hiện tại không đúng.", "danger")
            return render_template("change_password.html", form=form)
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash("Đổi mật khẩu thành công! Vui lòng ghi nhớ mật khẩu mới của bạn.", "success")
        return redirect(url_for("profile"))
    return render_template("change_password.html", form=form)


# --- Main Public Routes with Pagination (Phân Trang PWD301) ------------------
@app.route("/")
def home():
    cat_slug = request.args.get("cat")
    search_q = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 6

    query = Event.query
    if cat_slug:
        cat = Category.query.filter_by(slug=cat_slug).first()
        if cat:
            query = query.filter_by(category_id=cat.id)
    if search_q:
        query = query.filter(
            (Event.title.ilike(f"%{search_q}%")) | 
            (Event.venue.ilike(f"%{search_q}%")) |
            (Event.speaker_name.ilike(f"%{search_q}%"))
        )

    # Sử dụng phương thức paginate của SQLAlchemy ORM
    pagination = query.order_by(Event.start_time.asc()).paginate(page=page, per_page=per_page, error_out=False)
    events = pagination.items
    categories = Category.query.order_by(Category.id).all()

    # Sự kiện nổi bật sắp diễn ra nhất cho Countdown Timer
    featured_event = None
    all_events_for_feat = Event.query.filter(Event.start_time > datetime.utcnow(), Event.available_slots > 0).order_by(Event.start_time.asc()).all()
    if all_events_for_feat:
        featured_event = all_events_for_feat[0]
    elif events:
        featured_event = events[0]

    # Thống kê nhanh trên trang chủ
    total_events = Event.query.count()
    total_tickets = Ticket.query.filter_by(status="REGISTERED").count()
    total_students = User.query.count()

    return render_template(
        "home.html",
        events=events,
        pagination=pagination,
        categories=categories,
        active_cat=cat_slug,
        search_q=search_q,
        featured_event=featured_event,
        total_events=total_events,
        total_tickets=total_tickets,
        total_students=total_students
    )


@app.route("/events/<int:event_id>")
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    has_registered = False
    has_checked_in = False
    user_ticket = None
    user_review = None

    if current_user.is_authenticated:
        tickets = Ticket.query.filter_by(user_id=current_user.id, event_id=event.id).all()
        for t in tickets:
            if t.status == "REGISTERED":
                has_registered = True
                user_ticket = t
            elif t.status == "CHECKED_IN":
                has_checked_in = True
                user_ticket = t

        user_review = Review.query.filter_by(event_id=event.id, user_id=current_user.id).first()

    review_form = ReviewForm()

    related_events = Event.query.filter(
        Event.category_id == event.category_id,
        Event.id != event.id
    ).limit(3).all()

    # Google Calendar URL Generator
    gcal_start = event.start_time.strftime("%Y%m%dT%H%M%SZ")
    gcal_end = event.end_time.strftime("%Y%m%dT%H%M%SZ")
    speaker_txt = event.speaker_name or "FPTU"
    details_txt = f"Sự kiện FPT University: {event.title} - Diễn giả: {speaker_txt}"
    gcal_url = (
        f"https://calendar.google.com/calendar/render?action=TEMPLATE"
        f"&text={urllib.parse.quote(event.title)}"
        f"&dates={gcal_start}/{gcal_end}"
        f"&details={urllib.parse.quote(details_txt)}"
        f"&location={urllib.parse.quote(event.venue)}"
    )

    return render_template(
        "event_detail.html",
        event=event,
        has_registered=has_registered,
        has_checked_in=has_checked_in,
        user_ticket=user_ticket,
        user_review=user_review,
        review_form=review_form,
        gcal_url=gcal_url,
        related_events=related_events
    )


# --- Event Reviews & Ratings (Đánh Giá Sự Kiện) -----------------------------
@app.route("/events/<int:event_id>/review", methods=["POST"])
@login_required
def add_review(event_id):
    event = Event.query.get_or_404(event_id)
    form = ReviewForm()
    if form.validate_on_submit():
        existing = Review.query.filter_by(event_id=event.id, user_id=current_user.id).first()
        if existing:
            existing.rating = form.rating.data
            existing.comment = form.comment.data.strip()
            existing.created_at = datetime.utcnow()
            flash("Đã cập nhật đánh giá của bạn cho sự kiện!", "success")
        else:
            review = Review(
                event_id=event.id,
                user_id=current_user.id,
                rating=form.rating.data,
                comment=form.comment.data.strip()
            )
            db.session.add(review)
            flash("Cảm ơn bạn đã gửi đánh giá cho sự kiện!", "success")
        db.session.commit()
    else:
        flash("Vui lòng nhập đầy đủ nội dung đánh giá.", "warning")
    return redirect(url_for("event_detail", event_id=event.id))

@app.route("/events/<int:event_id>/review/delete", methods=["POST"])
@login_required
def delete_review(event_id):
    review = Review.query.filter_by(event_id=event_id, user_id=current_user.id).first_or_404()
    db.session.delete(review)
    db.session.commit()
    flash("Đã xóa đánh giá của bạn.", "info")
    return redirect(url_for("event_detail", event_id=event_id))


# --- Ticket Registration & Cancellation (Atomic Transaction) ----------------
@app.route("/events/<int:event_id>/register", methods=["POST"])
@login_required
def register_ticket(event_id):
    event = Event.query.get_or_404(event_id)

    # Cán bộ Phòng CTSV / Ban Tổ Chức chỉ quản lý, không đặt vé như sinh viên
    if current_user.is_admin or current_user.is_organizer:
        flash("Tài khoản Cán bộ Phòng CTSV là đơn vị tổ chức, quản lý và điều hành sự kiện — không áp dụng đăng ký giữ chỗ cá nhân!", "warning")
        return redirect(url_for("event_detail", event_id=event.id))

    # 1. Kiểm tra sinh viên đã đăng ký chưa
    existing_ticket = Ticket.query.filter_by(
        user_id=current_user.id,
        event_id=event.id,
        status="REGISTERED"
    ).first()
    if existing_ticket:
        flash("Bạn đã đăng ký vé cho sự kiện này rồi! Xem vé trong mục 'Vé Của Tôi'.", "info")
        return redirect(url_for("my_tickets"))

    # 2. Kiểm tra số lượng slot ghế trống (Capacity constraint)
    if event.available_slots <= 0:
        flash("Rất tiếc, sự kiện này đã hết sạch chỗ (Sold Out)!", "danger")
        return redirect(url_for("event_detail", event_id=event.id))

    # 3. Thực hiện Transaction: Trừ slot và Cấp vé điện tử
    try:
        event.available_slots -= 1
        ticket_code = Ticket.generate_ticket_code()
        qr_data = f"FPTU-TICKET|{ticket_code}|{current_user.student_id}|{event.id}"
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=280x280&data={urllib.parse.quote(qr_data)}"

        ticket = Ticket(
            ticket_code=ticket_code,
            qr_url=qr_url,
            event=event,
            user=current_user,
            status="REGISTERED"
        )
        db.session.add(ticket)
        db.session.commit()
        flash(f"🎉 Đăng ký vé thành công! Mã vé của bạn là: {ticket_code}", "success")
        return redirect(url_for("my_tickets"))
    except Exception as e:
        db.session.rollback()
        flash(f"Đã có lỗi xảy ra trong quá trình giữ chỗ: {str(e)}", "danger")
        return redirect(url_for("event_detail", event_id=event.id))


@app.route("/my-tickets")
@login_required
def my_tickets():
    tickets = Ticket.query.filter_by(user_id=current_user.id).order_by(Ticket.registered_at.desc()).all()
    return render_template("my_tickets.html", tickets=tickets)


@app.route("/tickets/<int:ticket_id>/certificate")
@login_required
def ticket_certificate(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.user_id != current_user.id and not current_user.is_organizer:
        flash("Bạn không có quyền xem giấy chứng nhận này.", "danger")
        return abort(403)
    if ticket.status != "CHECKED_IN":
        flash("Giấy chứng nhận chỉ được cấp sau khi bạn đã được điểm danh (Check-in) tại sự kiện!", "warning")
        return redirect(url_for("my_tickets"))
    return render_template("certificate.html", ticket=ticket)


@app.route("/tickets/<int:ticket_id>/cancel", methods=["POST"])
@login_required
def cancel_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.user_id != current_user.id:
        flash("Bạn không có quyền thực hiện thao tác này.", "danger")
        return abort(403)

    if ticket.status == "REGISTERED":
        # Hoàn lại 1 slot ghế cho sự kiện
        ticket.status = "CANCELLED"
        ticket.event.available_slots += 1
        db.session.commit()
        flash(f"Đã hủy vé {ticket.ticket_code} thành công. Slot ghế đã được hoàn lại cho sinh viên khác.", "info")
    else:
        flash("Vé này không thể hủy do đã điểm danh hoặc đã hủy trước đó.", "warning")

    return redirect(url_for("my_tickets"))


# --- Organizer & Event Management (CRUD Đầy Đủ) ------------------------------
@app.route("/organizer/dashboard")
@organizer_required
def organizer_dashboard():
    if current_user.is_admin:
        events = Event.query.order_by(Event.start_time.desc()).all()
    else:
        events = Event.query.filter_by(organizer_id=current_user.id).order_by(Event.start_time.desc()).all()

    total_created = len(events)
    total_registered = sum((e.total_capacity - e.available_slots) for e in events)
    total_capacity = sum(e.total_capacity for e in events) or 1
    avg_fill_rate = int((total_registered / total_capacity) * 100)

    return render_template(
        "organizer_dashboard.html",
        events=events,
        total_created=total_created,
        total_registered=total_registered,
        avg_fill_rate=avg_fill_rate
    )


@app.route("/organizer/events/new", methods=["GET", "POST"])
@organizer_required
def event_create():
    form = EventCreateForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.id).all()]

    if form.validate_on_submit():
        if form.end_time.data <= form.start_time.data:
            flash("Thời gian kết thúc sự kiện phải sau thời gian bắt đầu.", "danger")
            return render_template("event_create.html", form=form)

        banner = form.banner_url.data.strip() if form.banner_url.data else "/static/images/events/workshop_ai.jpg"
        slug_gen = f"event-{int(datetime.utcnow().timestamp())}"

        new_event = Event(
            title=form.title.data.strip(),
            slug=slug_gen,
            category_id=form.category_id.data,
            venue=form.venue.data.strip(),
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            total_capacity=form.total_capacity.data,
            available_slots=form.total_capacity.data,
            speaker_name=form.speaker_name.data.strip() if form.speaker_name.data else None,
            speaker_title=form.speaker_title.data.strip() if form.speaker_title.data else None,
            banner_url=banner,
            description_md=form.description_md.data,
            description_html=render_safe_markdown(form.description_md.data),
            organizer_id=current_user.id,
            status="OPEN"
        )
        db.session.add(new_event)
        db.session.commit()
        flash(f"Tạo sự kiện '{new_event.title}' thành công và đã mở cổng đăng ký!", "success")
        return redirect(url_for("organizer_dashboard"))

    return render_template("event_create.html", form=form)


@app.route("/organizer/events/<int:event_id>/edit", methods=["GET", "POST"])
@organizer_required
def event_edit(event_id):
    event = Event.query.get_or_404(event_id)
    if not current_user.is_admin and event.organizer_id != current_user.id:
        flash("Bạn không có quyền chỉnh sửa sự kiện này.", "danger")
        return abort(403)

    form = EventEditForm(obj=event)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.id).all()]

    if form.validate_on_submit():
        if form.end_time.data <= form.start_time.data:
            flash("Thời gian kết thúc sự kiện phải sau thời gian bắt đầu.", "danger")
            return render_template("event_edit.html", form=form, event=event)

        event.title = form.title.data.strip()
        event.category_id = form.category_id.data
        event.venue = form.venue.data.strip()
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.status = form.status.data
        event.speaker_name = form.speaker_name.data.strip() if form.speaker_name.data else None
        event.speaker_title = form.speaker_title.data.strip() if form.speaker_title.data else None
        if form.banner_url.data:
            event.banner_url = form.banner_url.data.strip()
        event.description_md = form.description_md.data
        event.description_html = render_safe_markdown(form.description_md.data)

        # Cập nhật số ghế nếu tăng/giảm capacity
        registered_count = event.total_capacity - event.available_slots
        new_total = form.total_capacity.data
        if new_total >= registered_count:
            event.total_capacity = new_total
            event.available_slots = new_total - registered_count
        else:
            flash(f"Không thể giảm tổng số ghế xuống dưới số lượng đã đăng ký ({registered_count} người).", "warning")

        db.session.commit()
        flash(f"Cập nhật sự kiện '{event.title}' thành công!", "success")
        return redirect(url_for("organizer_dashboard"))

    return render_template("event_edit.html", form=form, event=event)


@app.route("/organizer/events/<int:event_id>/delete", methods=["POST"])
@organizer_required
def event_delete(event_id):
    event = Event.query.get_or_404(event_id)
    if not current_user.is_admin and event.organizer_id != current_user.id:
        flash("Bạn không có quyền xóa sự kiện này.", "danger")
        return abort(403)

    event_title = event.title
    db.session.delete(event)
    db.session.commit()
    flash(f"Đã xóa hoàn toàn sự kiện '{event_title}' và các vé liên quan khỏi hệ thống.", "info")
    return redirect(url_for("organizer_dashboard"))


@app.route("/organizer/events/<int:event_id>/attendees")
@organizer_required
def event_attendees(event_id):
    event = Event.query.get_or_404(event_id)
    if not current_user.is_admin and event.organizer_id != current_user.id:
        flash("Bạn không có quyền quản lý người tham dự sự kiện này.", "danger")
        return abort(403)

    tickets = Ticket.query.filter_by(event_id=event.id).order_by(Ticket.registered_at.desc()).all()
    checked_in_count = sum(1 for t in tickets if t.status == "CHECKED_IN")

    return render_template(
        "attendees.html",
        event=event,
        tickets=tickets,
        checked_in_count=checked_in_count
    )


# --- Category Management CRUD (Chương 9 PWD301 REST API & Admin) --------------
@app.route("/admin/categories")
@admin_required
def category_list():
    categories = Category.query.order_by(Category.id.asc()).all()
    return render_template("category_list.html", categories=categories)


@app.route("/admin/categories/new", methods=["GET", "POST"])
@admin_required
def category_create():
    form = CategoryForm()
    if form.validate_on_submit():
        existing = Category.query.filter(
            (Category.name == form.name.data.strip()) | 
            (Category.slug == form.slug.data.strip())
        ).first()
        if existing:
            flash("Tên hoặc đường dẫn tĩnh (slug) của danh mục đã tồn tại.", "danger")
            return render_template("category_form.html", form=form, title="Thêm Danh Mục Mới")

        cat = Category(
            name=form.name.data.strip(),
            slug=form.slug.data.strip(),
            icon=form.icon.data.strip() if form.icon.data else "fa-calendar-star",
            color=form.color.data.strip() if form.color.data else "#f26f21",
            description=form.description.data.strip() if form.description.data else None
        )
        db.session.add(cat)
        db.session.commit()
        flash(f"Thêm danh mục '{cat.name}' thành công!", "success")
        return redirect(url_for("category_list"))

    return render_template("category_form.html", form=form, title="Thêm Danh Mục Mới")


@app.route("/admin/categories/<int:cat_id>/edit", methods=["GET", "POST"])
@admin_required
def category_edit(cat_id):
    cat = Category.query.get_or_404(cat_id)
    form = CategoryForm(obj=cat)
    if form.validate_on_submit():
        cat.name = form.name.data.strip()
        cat.slug = form.slug.data.strip()
        cat.icon = form.icon.data.strip() if form.icon.data else "fa-calendar-star"
        cat.color = form.color.data.strip() if form.color.data else "#f26f21"
        cat.description = form.description.data.strip() if form.description.data else None
        db.session.commit()
        flash(f"Cập nhật danh mục '{cat.name}' thành công!", "success")
        return redirect(url_for("category_list"))

    return render_template("category_form.html", form=form, title=f"Sửa Danh Mục: {cat.name}")


@app.route("/admin/categories/<int:cat_id>/delete", methods=["POST"])
@admin_required
def category_delete(cat_id):
    cat = Category.query.get_or_404(cat_id)
    if cat.events:
        flash(f"Không thể xóa danh mục '{cat.name}' vì đang có {len(cat.events)} sự kiện liên kết. Vui lòng chuyển hoặc xóa các sự kiện trước.", "danger")
        return redirect(url_for("category_list"))

    db.session.delete(cat)
    db.session.commit()
    flash(f"Đã xóa danh mục '{cat.name}' thành công.", "info")
    return redirect(url_for("category_list"))


# --- Export Attendees CSV for Organizer & Admin -----------------------------
@app.route("/organizer/events/<int:event_id>/export-csv")
@organizer_required
def export_attendees_csv(event_id):
    event = Event.query.get_or_404(event_id)
    if not current_user.is_admin and event.organizer_id != current_user.id:
        return abort(403)

    tickets = Ticket.query.filter_by(event_id=event.id).order_by(Ticket.registered_at.asc()).all()

    si = io.StringIO()
    cw = csv.writer(si)
    # Header chuẩn phòng CTSV FPT
    cw.writerow(["Mã Vé", "MSSV", "Họ và Tên", "Email", "Số Điện Thoại", "Thời Gian Đăng Ký", "Trạng Thái", "Thời Gian Điểm Danh"])

    for t in tickets:
        cw.writerow([
            t.ticket_code,
            t.user.student_id or "",
            t.user.full_name,
            t.user.email,
            t.user.phone or "",
            t.registered_at.strftime("%Y-%m-%d %H:%M:%S") if t.registered_at else "",
            "Đã điểm danh" if t.status == "CHECKED_IN" else ("Đã đăng ký" if t.status == "REGISTERED" else "Đã hủy"),
            t.checked_in_at.strftime("%Y-%m-%d %H:%M:%S") if t.checked_in_at else "Chưa",
        ])

    # UTF-8 BOM giúp Excel Windows hiển thị đúng tiếng Việt không lỗi font
    output = "\ufeff" + si.getvalue()
    filename = f"FPTU_DiemDanh_Event_{event.id}.csv"
    return Response(
        output,
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


# --- Check-in Desk (Manual & Camera QR Code Scanner) -----------------------
@app.route("/check-in", methods=["GET", "POST"])
@app.route("/organizer/check-in", methods=["GET", "POST"])
@login_required
def check_in():
    form = CheckInManualForm()
    check_result = None

    if form.validate_on_submit():
        code = form.ticket_code.data.strip().upper()
        if "|" in code:
            parts = code.split("|")
            if len(parts) >= 2:
                code = parts[1].strip()

        ticket = Ticket.query.filter_by(ticket_code=code).first()

        if ticket is None:
            check_result = {
                "success": False,
                "msg": f"❌ Không tìm thấy vé có mã '{code}' trong hệ thống FPTU!",
                "type": "danger"
            }
        elif ticket.status == "CANCELLED":
            check_result = {
                "success": False,
                "msg": f"⚠️ Vé '{code}' của sinh viên {ticket.user.full_name} đã bị HỦY trước đó!",
                "type": "warning"
            }
        elif ticket.status == "CHECKED_IN":
            check_result = {
                "success": False,
                "msg": f"⚠️ Vé này ĐÃ CHECK-IN vào lúc {ticket.checked_in_at.strftime('%H:%M - %d/%m/%Y')}!",
                "type": "warning",
                "ticket": ticket
            }
        else:
            ticket.status = "CHECKED_IN"
            ticket.checked_in_at = datetime.utcnow()
            db.session.commit()
            check_result = {
                "success": True,
                "msg": f"✅ CHECK-IN THÀNH CÔNG cho sinh viên {ticket.user.full_name} ({ticket.user.student_id})!",
                "type": "success",
                "ticket": ticket
            }

    return render_template("checkin.html", form=form, check_result=check_result)


@app.route("/api/check-in/scan", methods=["POST"])
@login_required
def api_scan_checkin():
    data = request.get_json() or {}
    raw_code = data.get("ticket_code", "").strip()

    code = raw_code
    if "|" in raw_code:
        parts = raw_code.split("|")
        if len(parts) >= 2:
            code = parts[1].strip()

    code = code.strip().upper()
    ticket = Ticket.query.filter_by(ticket_code=code).first()

    if not ticket:
        return jsonify({"success": False, "msg": f"❌ Không tìm thấy vé có mã '{code}' trong hệ thống!", "type": "danger"}), 404

    if ticket.status == "CANCELLED":
        return jsonify({"success": False, "msg": f"⚠️ Vé '{code}' của {ticket.user.full_name} đã bị HỦY!", "type": "warning"}), 400

    if ticket.status == "CHECKED_IN":
        return jsonify({
            "success": False,
            "msg": f"⚠️ Vé này ĐÃ CHECK-IN vào lúc {ticket.checked_in_at.strftime('%H:%M - %d/%m/%Y')}!",
            "type": "warning",
            "ticket": {
                "code": ticket.ticket_code,
                "student_name": ticket.user.full_name,
                "student_id": ticket.user.student_id,
                "event_title": ticket.event.title
            }
        }), 200

    ticket.status = "CHECKED_IN"
    ticket.checked_in_at = datetime.utcnow()
    db.session.commit()

    return jsonify({
        "success": True,
        "msg": f"🎉 CHECK-IN THÀNH CÔNG: {ticket.user.full_name} ({ticket.user.student_id})!",
        "type": "success",
        "ticket": {
            "code": ticket.ticket_code,
            "student_name": ticket.user.full_name,
            "student_id": ticket.user.student_id,
            "event_title": ticket.event.title
        }
    })


@app.route("/organizer/tickets/<int:ticket_id>/toggle-checkin", methods=["POST"])
@organizer_required
def toggle_checkin(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.status == "REGISTERED":
        ticket.status = "CHECKED_IN"
        ticket.checked_in_at = datetime.utcnow()
        flash(f"Đã điểm danh vé {ticket.ticket_code} thành công!", "success")
    elif ticket.status == "CHECKED_IN":
        ticket.status = "REGISTERED"
        ticket.checked_in_at = None
        flash(f"Đã hoàn tác điểm danh vé {ticket.ticket_code}.", "info")
    db.session.commit()
    return redirect(url_for("event_attendees", event_id=ticket.event_id))


# --- Admin Dashboard ---------------------------------------------------------
@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    total_users = User.query.count()
    total_events = Event.query.count()
    total_tickets = Ticket.query.count()
    checked_in_total = Ticket.query.filter_by(status="CHECKED_IN").count()
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    categories = Category.query.all()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_events=total_events,
        total_tickets=total_tickets,
        checked_in_total=checked_in_total,
        recent_users=recent_users,
        categories=categories
    )


# =============================================================================
# --- FULL RESTful API v1 (Chương 9 & Exam ParkTicket Chuẩn PWD301) ------------
# =============================================================================

@app.route("/api/v1/auth/login", methods=["POST"])
def api_auth_login():
    """REST API Login: Nhận JSON {"email": "...", "password": "..."} và trả về thông tin người dùng."""
    data = request.get_json() or {}
    email_or_mssv = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not email_or_mssv or not password:
        return jsonify({"error": "Thiếu email hoặc mật khẩu."}), 400

    user = User.query.filter(
        (User.email.ilike(email_or_mssv)) | 
        (User.student_id.ilike(email_or_mssv))
    ).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Email hoặc mật khẩu không chính xác."}), 401

    login_user(user, remember=True)
    return jsonify({
        "message": "Đăng nhập thành công.",
        "user": user.to_dict()
    }), 200


@app.route("/api/v1/events", methods=["GET"])
def api_events_list():
    """REST API: Danh sách sự kiện có phân trang, lọc theo danh mục và tìm kiếm từ khóa."""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    cat_slug = request.args.get("category")
    search = request.args.get("search", "").strip()

    query = Event.query
    if cat_slug:
        cat = Category.query.filter_by(slug=cat_slug).first()
        if cat:
            query = query.filter_by(category_id=cat.id)
    if search:
        query = query.filter(
            (Event.title.ilike(f"%{search}%")) |
            (Event.venue.ilike(f"%{search}%")) |
            (Event.speaker_name.ilike(f"%{search}%"))
        )

    pagination = query.order_by(Event.start_time.asc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
        "events": [e.to_dict() for e in pagination.items]
    }), 200


@app.route("/api/v1/events/<int:event_id>", methods=["GET"])
def api_event_detail(event_id):
    """REST API: Chi tiết một sự kiện theo ID."""
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Không tìm thấy sự kiện với ID tương ứng."}), 404
    return jsonify(event.to_dict()), 200


@app.route("/api/v1/events", methods=["POST"])
@organizer_required
def api_event_create():
    """REST API: Tạo sự kiện mới (Yêu cầu quyền Organizer hoặc Admin)."""
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    category_id = data.get("category_id")
    venue = data.get("venue", "").strip()
    start_str = data.get("start_time")
    end_str = data.get("end_time")
    capacity = data.get("total_capacity", 100)

    if not title or not category_id or not venue or not start_str or not end_str:
        return jsonify({"error": "Thiếu các thông tin bắt buộc (title, category_id, venue, start_time, end_time)."}), 400

    try:
        start_dt = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end_str.replace("Z", "+00:00"))
    except ValueError:
        return jsonify({"error": "Định dạng thời gian không hợp lệ (ISO 8601: YYYY-MM-DDTHH:MM:SS)."}), 400

    if end_dt <= start_dt:
        return jsonify({"error": "Thời gian kết thúc phải sau thời gian bắt đầu."}), 422

    ev = Event(
        title=title,
        slug=f"event-{int(datetime.utcnow().timestamp())}",
        category_id=category_id,
        venue=venue,
        start_time=start_dt,
        end_time=end_dt,
        total_capacity=int(capacity),
        available_slots=int(capacity),
        speaker_name=data.get("speaker_name"),
        speaker_title=data.get("speaker_title"),
        banner_url=data.get("banner_url", "/static/images/events/workshop_ai.jpg"),
        description_md=data.get("description", ""),
        description_html=render_safe_markdown(data.get("description", "")),
        organizer_id=current_user.id,
        status="OPEN"
    )
    db.session.add(ev)
    db.session.commit()

    return jsonify({"message": "Tạo sự kiện thành công.", "event": ev.to_dict()}), 201


@app.route("/api/v1/events/<int:event_id>", methods=["PUT"])
@organizer_required
def api_event_update(event_id):
    """REST API: Cập nhật sự kiện (Yêu cầu quyền Organizer hoặc Admin)."""
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Không tìm thấy sự kiện."}), 404
    if not current_user.is_admin and event.organizer_id != current_user.id:
        return jsonify({"error": "Bạn không có quyền sửa sự kiện này."}), 403

    data = request.get_json() or {}
    if "title" in data:
        event.title = data["title"].strip()
    if "venue" in data:
        event.venue = data["venue"].strip()
    if "speaker_name" in data:
        event.speaker_name = data["speaker_name"].strip()
    if "speaker_title" in data:
        event.speaker_title = data["speaker_title"].strip()
    if "banner_url" in data:
        event.banner_url = data["banner_url"].strip()
    if "status" in data:
        event.status = data["status"].strip()
    if "description" in data:
        event.description_md = data["description"]
        event.description_html = render_safe_markdown(data["description"])

    db.session.commit()
    return jsonify({"message": "Cập nhật sự kiện thành công.", "event": event.to_dict()}), 200


@app.route("/api/v1/events/<int:event_id>", methods=["DELETE"])
@organizer_required
def api_event_delete(event_id):
    """REST API: Xóa sự kiện theo ID."""
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Không tìm thấy sự kiện."}), 404
    if not current_user.is_admin and event.organizer_id != current_user.id:
        return jsonify({"error": "Bạn không có quyền xóa sự kiện này."}), 403

    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": f"Đã xóa sự kiện ID {event_id} thành công."}), 200


@app.route("/api/v1/categories", methods=["GET"])
def api_categories():
    """REST API: Danh sách danh mục sự kiện kèm số lượng sự kiện liên kết."""
    cats = Category.query.order_by(Category.id.asc()).all()
    return jsonify([c.to_dict() for c in cats]), 200


@app.route("/api/v1/tickets", methods=["GET"])
@login_required
def api_tickets():
    """REST API: Danh sách vé của sinh viên đang đăng nhập, hoặc toàn bộ vé nếu là Admin."""
    if current_user.is_admin:
        tickets = Ticket.query.order_by(Ticket.registered_at.desc()).limit(100).all()
    else:
        tickets = Ticket.query.filter_by(user_id=current_user.id).order_by(Ticket.registered_at.desc()).all()
    return jsonify([t.to_dict() for t in tickets]), 200


@app.route("/api/v1/stats", methods=["GET"])
def api_stats():
    """REST API: Thống kê tổng quan hệ thống."""
    return jsonify({
        "total_events": Event.query.count(),
        "total_users": User.query.count(),
        "total_tickets_booked": Ticket.query.filter_by(status="REGISTERED").count(),
        "total_checkins": Ticket.query.filter_by(status="CHECKED_IN").count(),
        "total_categories": Category.query.count()
    }), 200


# --- Static Files Fallback for Serverless/Vercel Environments ---------------
@app.route("/static/<path:filename>")
def serve_static_fallback(filename):
    static_folder = os.path.join(app.root_path, "static")
    return send_from_directory(static_folder, filename)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
