# FPTU EventHub: Database Models
# He thong Quan ly & Dang ky Su kien Sinh vien FPT University (events.fptu.vn)

import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    users = db.relationship("User", back_populates="role", lazy="select")

    @staticmethod
    def insert_roles():
        roles = {
            "Student": "Sinh viên tham dự sự kiện và tích lũy điểm PDP",
            "Organizer": "Ban tổ chức CLB / Giảng viên tổ chức workshop",
            "Admin": "Cán bộ quản trị Phòng Công tác sinh viên (CTSV)",
        }
        for name, desc in roles.items():
            role = Role.query.filter_by(name=name).first()
            if role is None:
                role = Role(name=name, description=desc)
                db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return f"<Role {self.name}>"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=True, index=True) # MSSV: e.g. DE200433
    full_name = db.Column(db.Unicode(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    avatar_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    role = db.relationship("Role", back_populates="users")

    # Quan he voi Events, Tickets, Reviews
    organized_events = db.relationship("Event", back_populates="organizer", lazy="select")
    tickets = db.relationship("Ticket", back_populates="user", lazy="select")
    reviews = db.relationship("Review", back_populates="user", lazy="select")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_organizer(self):
        return self.role and self.role.name in ("Organizer", "Admin")

    @property
    def is_admin(self):
        return self.role and self.role.name == "Admin"

    def has_registered(self, event_id):
        return Ticket.query.filter_by(
            user_id=self.id, 
            event_id=event_id, 
            status="REGISTERED"
        ).first() is not None

    @property
    def total_pdp_points(self):
        # Tinh tong diem PDP da tich luy qua cac su kien da check-in
        checked_tickets = Ticket.query.filter_by(user_id=self.id, status="CHECKED_IN").all()
        return sum(t.event.pdp_points for t in checked_tickets if t.event and t.event.pdp_points)

    @property
    def pdp_rank(self):
        pts = self.total_pdp_points
        if pts >= 30:
            return {
                "title": "Huyền Thoại Cóc Vàng",
                "icon": "🥇",
                "badge_class": "feh-rank-gold",
                "color": "#f59e0b",
                "next_rank": None,
                "pts_to_next": 0,
                "progress_percent": 100
            }
        elif pts >= 15:
            return {
                "title": "Chiến Binh Năng Nổ",
                "icon": "🥈",
                "badge_class": "feh-rank-warrior",
                "color": "#3b82f6",
                "next_rank": "Huyền Thoại Cóc Vàng (30 PDP)",
                "pts_to_next": 30 - pts,
                "progress_percent": min(100, int((pts / 30) * 100))
            }
        else:
            return {
                "title": "Tân Binh Trường F",
                "icon": "🥉",
                "badge_class": "feh-rank-recruit",
                "color": "#10b981",
                "next_rank": "Chiến Binh Năng Nổ (15 PDP)",
                "pts_to_next": 15 - pts,
                "progress_percent": min(100, int((pts / 15) * 100))
            }


    def __repr__(self):
        return f"<User {self.email} ({self.student_id})>"


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    icon = db.Column(db.String(50), default="fa-calendar-star")
    color = db.Column(db.String(20), default="#f26f21")
    description = db.Column(db.Unicode(255), nullable=True)

    events = db.relationship("Event", back_populates="category", lazy="select")

    def __repr__(self):
        return f"<Category {self.name}>"


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(255), nullable=False, index=True)
    slug = db.Column(db.String(255), nullable=True)
    banner_url = db.Column(db.String(500), nullable=True)
    speaker_name = db.Column(db.Unicode(120), nullable=True)
    speaker_title = db.Column(db.Unicode(200), nullable=True)
    speaker_avatar = db.Column(db.String(500), nullable=True)
    venue = db.Column(db.Unicode(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    total_capacity = db.Column(db.Integer, nullable=False, default=100) # Tong so cho ngoi
    available_slots = db.Column(db.Integer, nullable=False, default=100) # So cho con lai
    pdp_points = db.Column(db.Integer, nullable=False, default=10) # Diem ren luyen PDP (FPT)

    description_md = db.Column(db.UnicodeText, nullable=True)
    description_html = db.Column(db.UnicodeText, nullable=True)
    status = db.Column(db.String(20), default="OPEN") # OPEN, FULL, COMPLETED, CANCELLED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Khoa ngoai
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    category = db.relationship("Category", back_populates="events")

    organizer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    organizer = db.relationship("User", back_populates="organized_events")

    tickets = db.relationship("Ticket", back_populates="event", cascade="all, delete-orphan", lazy="select")
    reviews = db.relationship("Review", back_populates="event", cascade="all, delete-orphan", lazy="select")

    @property
    def is_sold_out(self):
        return self.available_slots <= 0

    @property
    def filled_percentage(self):
        if self.total_capacity <= 0:
            return 100
        registered = self.total_capacity - self.available_slots
        return int((registered / self.total_capacity) * 100)

    @property
    def average_rating(self):
        if not self.reviews:
            return 5.0
        return round(sum(r.rating for r in self.reviews) / len(self.reviews), 1)

    @property
    def review_count(self):
        return len(self.reviews)

    def __repr__(self):
        return f"<Event {self.title}>"


class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    ticket_code = db.Column(db.String(50), unique=True, nullable=False, index=True) # e.g. FU-2026-X89AD
    qr_url = db.Column(db.String(500), nullable=True)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="REGISTERED") # REGISTERED, CHECKED_IN, CANCELLED
    checked_in_at = db.Column(db.DateTime, nullable=True)

    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    event = db.relationship("Event", back_populates="tickets")

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="tickets")

    @staticmethod
    def generate_ticket_code():
        rand_str = uuid.uuid4().hex[:6].upper()
        return f"FU-{datetime.now().year}-{rand_str}"

    def __repr__(self):
        return f"<Ticket {self.ticket_code} for {self.user.email}>"


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False, default=5) # 1 - 5 sao
    comment = db.Column(db.UnicodeText, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    event = db.relationship("Event", back_populates="reviews")

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="reviews")

    def __repr__(self):
        return f"<Review {self.rating}* by {self.user.email} for Event {self.event_id}>"
