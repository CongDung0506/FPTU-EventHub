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
            "Student": "Sinh viên tham dự sự kiện",
            "Organizer": "Ban tổ chức CLB / Giảng viên tổ chức workshop",
            "Admin": "Cán bộ quản trị Phòng Công tác sinh viên (CTSV)",
        }
        for name, desc in roles.items():
            role = Role.query.filter_by(name=name).first()
            if role is None:
                role = Role(name=name, description=desc)
                db.session.add(role)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

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

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "avatar_url": self.avatar_url,
            "role": self.role.name if self.role else None,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
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

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "icon": self.icon,
            "color": self.color,
            "description": self.description,
            "events_count": len(self.events) if self.events else 0
        }

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

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "venue": self.venue,
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S") if self.start_time else None,
            "end_time": self.end_time.strftime("%Y-%m-%d %H:%M:%S") if self.end_time else None,
            "total_capacity": self.total_capacity,
            "available_slots": self.available_slots,
            "speaker_name": self.speaker_name,
            "speaker_title": self.speaker_title,
            "banner_url": self.banner_url,
            "category": self.category.name if self.category else None,
            "category_id": self.category_id,
            "organizer": self.organizer.full_name if self.organizer else None,
            "status": self.status,
            "is_sold_out": self.is_sold_out,
            "average_rating": self.average_rating,
            "review_count": self.review_count,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }

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

    def to_dict(self):
        return {
            "id": self.id,
            "ticket_code": self.ticket_code,
            "status": self.status,
            "registered_at": self.registered_at.strftime("%Y-%m-%d %H:%M:%S") if self.registered_at else None,
            "checked_in_at": self.checked_in_at.strftime("%Y-%m-%d %H:%M:%S") if self.checked_in_at else None,
            "event_id": self.event_id,
            "event_title": self.event.title if self.event else None,
            "student_id": self.user.student_id if self.user else None,
            "student_name": self.user.full_name if self.user else None,
            "student_email": self.user.email if self.user else None
        }

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

    def to_dict(self):
        return {
            "id": self.id,
            "rating": self.rating,
            "comment": self.comment,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "event_id": self.event_id,
            "user_id": self.user_id,
            "user_name": self.user.full_name if self.user else None
        }

    def __repr__(self):
        return f"<Review {self.rating}* by {self.user.email} for Event {self.event_id}>"
