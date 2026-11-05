# FPTU EventHub: Main Application
# He thong Quan ly & Dang ky Su kien Sinh vien FPT University (events.fptu.vn)

import os
import csv
import io
import tempfile
import urllib.parse
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, flash, abort, jsonify, Response, send_from_directory
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, current_user, login_user, logout_user

from models import db, User, Role, Category, Event, Ticket, Review
from markdown_utils import render_safe_markdown
from decorators import organizer_required, admin_required
from forms import LoginForm, RegisterForm, EventCreateForm, CheckInManualForm, ReviewForm

app = Flask(__name__)
Bootstrap(app)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "fptu-eventhub-secret-key-2026")

# Database configuration linh hoat cho ca Localhost va Cloud (Vercel)
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


# Tu dong tao database va nap du lieu mau chuan FPT
@app.before_request
def auto_init_database():
    try:
        db.create_all()
        if User.query.count() < 10 or Event.query.count() < 5 or Ticket.query.count() < 30:
            from seed_events import seed_data_internal
            seed_data_internal()
    except Exception as e:
        db.session.rollback()
        print(f"Notice DB init: {e}")

@app.before_request
def require_fpt_login():
    # Bat buoc tat ca nguoi dung phai dang nhap FPT Mail truoc khi truy cap vao cong su kien
    if not request.endpoint:
        return None
    public_endpoints = ("login", "quick_login", "register", "static", "serve_static_fallback")
    if request.endpoint in public_endpoints:
        return None
    if not current_user.is_authenticated:
        return redirect(url_for("login"))


# --- Authentication Routes ---------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        ident = form.email.data.strip()
        if '@' in ident:
            if not (ident.lower().endswith('@fpt.edu.vn') or ident.lower().endswith('@fe.edu.vn')):
                flash('❌ Email không thuộc hệ thống Đại học FPT! Vui lòng sử dụng email trường cấp (@fpt.edu.vn / @fe.edu.vn) hoặc Mã SV (MSSV).', 'danger')
                return render_template('login.html', form=form)
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
                return redirect(next_page or url_for("home"))
            else:
                flash("Mật khẩu không chính xác. Vui lòng thử lại (mật khẩu mặc định: pass123).", "danger")
        else:
            # Auto-provision student account for valid FPT email domain (Zero Registration needed)
            if "@" in ident and (ident.lower().endswith("@fpt.edu.vn") or ident.lower().endswith("@fe.edu.vn")):
                email_clean = ident.lower()
                role_student = Role.query.filter_by(name="Student").first()
                # Trich xuat MSSV neu co (vi du: dungtcde200433@fpt.edu.vn -> DE200433)
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
    if rt == "student":
        user = User.query.filter(
            (User.email == "dungtcde200433@fpt.edu.vn") | 
            (User.student_id == "DE200433") |
            (User.role.has(name="Student"))
        ).first()
    elif rt in ("admin", "organizer"):
        user = User.query.filter(
            (User.email == "ctsv.admin@fpt.edu.vn") | 
            (User.student_id == "ADM001") |
            (User.role.has(name="Admin"))
        ).first()
    else:
        user = None

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
    flash("Bạn đã đăng xuất an toàn.", "info")
    return redirect(url_for("home"))


# --- Main Public Routes -----------------------------------------------------
@app.route("/")
def home():
    cat_slug = request.args.get("cat")
    search_q = request.args.get("q", "").strip()

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

    events = query.order_by(Event.start_time.asc()).all()
    categories = Category.query.order_by(Category.id).all()

    # Su kien noi bat sap dien ra nhat cho Countdown Timer
    featured_event = None
    upcoming_events = [e for e in events if e.start_time > datetime.utcnow() and not e.is_sold_out]
    if upcoming_events:
        featured_event = upcoming_events[0]
    elif events:
        featured_event = events[0]

    # Thong ke nhanh tren trang chu
    total_events = Event.query.count()
    total_tickets = Ticket.query.filter_by(status="REGISTERED").count()
    total_students = User.query.count()

    return render_template(
        "home.html",
        events=events,
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


# --- Event Reviews & Ratings ------------------------------------------------
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


# --- Ticket Registration & Cancellation (Atomic Transaction) ----------------
@app.route("/events/<int:event_id>/register", methods=["POST"])
@login_required
def register_ticket(event_id):
    event = Event.query.get_or_404(event_id)

    # 1. Kiem tra sinh vien da dang ky chua
    existing_ticket = Ticket.query.filter_by(
        user_id=current_user.id,
        event_id=event.id,
        status="REGISTERED"
    ).first()
    if existing_ticket:
        flash("Bạn đã đăng ký vé cho sự kiện này rồi! Xem vé trong mục 'Vé Của Tôi'.", "info")
        return redirect(url_for("my_tickets"))

    # 2. Kiem tra so luong slot ghe trong (Capacity constraint)
    if event.available_slots <= 0:
        flash("Rất tiếc, sự kiện này đã hết sạch chỗ (Sold Out)!", "danger")
        return redirect(url_for("event_detail", event_id=event.id))

    # 3. Thuc hien Transaction: Tru slot va Cap ve dien tu
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
        flash(f"🎉 Đăng ký vé thành công! Mã vé của bạn là: {ticket_code} (+{event.pdp_points} PDP sau khi điểm danh)", "success")
        return redirect(url_for("my_tickets"))
    except Exception as e:
        db.session.rollback()
        flash(f"Đã có lỗi xảy ra trong quá trình giữ chỗ: {str(e)}", "danger")
        return redirect(url_for("event_detail", event_id=event.id))


@app.route("/my-tickets")
@login_required
def my_tickets():
    tickets = Ticket.query.filter_by(user_id=current_user.id).order_by(Ticket.registered_at.desc()).all()
    # Tinh tong diem PDP
    total_pdp = current_user.total_pdp_points
    return render_template("my_tickets.html", tickets=tickets, total_pdp=total_pdp)


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
        # Hoan lai 1 slot ghe cho su kien
        ticket.status = "CANCELLED"
        ticket.event.available_slots += 1
        db.session.commit()
        flash(f"Đã hủy vé {ticket.ticket_code} thành công. Slot ghế đã được hoàn lại cho sinh viên khác.", "info")
    else:
        flash("Vé này không thể hủy do đã điểm danh hoặc đã hủy trước đó.", "warning")

    return redirect(url_for("my_tickets"))


# --- Organizer & Event Management -------------------------------------------
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
            pdp_points=form.pdp_points.data,
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
    # Header chuan phong CTSV FPT
    cw.writerow(["Mã Vé", "MSSV", "Họ và Tên", "Email", "Số Điện Thoại", "Thời Gian Đăng Ký", "Trạng Thái", "Thời Gian Điểm Danh", "Điểm PDP Nhận"])

    for t in tickets:
        pdp_earned = event.pdp_points if t.status == "CHECKED_IN" else 0
        cw.writerow([
            t.ticket_code,
            t.user.student_id or "",
            t.user.full_name,
            t.user.email,
            t.user.phone or "",
            t.registered_at.strftime("%Y-%m-%d %H:%M:%S") if t.registered_at else "",
            "Đã điểm danh" if t.status == "CHECKED_IN" else ("Đã đăng ký" if t.status == "REGISTERED" else "Đã hủy"),
            t.checked_in_at.strftime("%Y-%m-%d %H:%M:%S") if t.checked_in_at else "Chưa",
            pdp_earned
        ])

    # UTF-8 BOM giup Excel Windows hien thi dung tieng Viet khong loi font
    output = '\ufeff' + si.getvalue()
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
        # ho tro ca format parse tu QR
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
                "msg": f"✅ CHECK-IN THÀNH CÔNG cho sinh viên {ticket.user.full_name} ({ticket.user.student_id})! +{ticket.event.pdp_points} Điểm PDP",
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
        "msg": f"🎉 CHECK-IN THÀNH CÔNG: {ticket.user.full_name} ({ticket.user.student_id})! +{ticket.event.pdp_points} PDP",
        "type": "success",
        "ticket": {
            "code": ticket.ticket_code,
            "student_name": ticket.user.full_name,
            "student_id": ticket.user.student_id,
            "event_title": ticket.event.title,
            "pdp_points": ticket.event.pdp_points
        }
    })


@app.route("/organizer/tickets/<int:ticket_id>/toggle-checkin", methods=["POST"])
@organizer_required
def toggle_checkin(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.status == "REGISTERED":
        ticket.status = "CHECKED_IN"
        ticket.checked_in_at = datetime.utcnow()
        flash(f"Đã điểm danh vé {ticket.ticket_code} (+{ticket.event.pdp_points} PDP) thành công!", "success")
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


# --- Static Files Fallback for Serverless/Vercel Environments ---------------
@app.route("/static/<path:filename>")
def serve_static_fallback(filename):
    static_folder = os.path.join(app.root_path, "static")
    return send_from_directory(static_folder, filename)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
