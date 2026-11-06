# FPTU EventHub: Form Definitions (Flask-WTF)
# Bao gom day du cac custom validator, CSRF, cac loai Field da hoc trong PWD301

import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, IntegerField, SelectField, DateTimeLocalField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange, ValidationError, EqualTo


class LoginForm(FlaskForm):
    email = StringField("Email FPT hoặc Mã SV (MSSV)", validators=[DataRequired(message="Vui lòng nhập Email FPT hoặc MSSV.")])
    password = PasswordField("Mật khẩu", validators=[DataRequired(message="Vui lòng nhập mật khẩu.")])
    remember_me = BooleanField("Ghi nhớ đăng nhập")
    submit = SubmitField("Đăng Nhập")

    def validate_email(self, field):
        ident = field.data.strip()
        if "@" in ident:
            ident_lower = ident.lower()
            if not (ident_lower.endswith("@fpt.edu.vn") or ident_lower.endswith("@fe.edu.vn")):
                raise ValidationError("Chỉ chấp nhận email do Đại học FPT cấp (@fpt.edu.vn hoặc @fe.edu.vn) hoặc MSSV!")


class RegisterForm(FlaskForm):
    student_id = StringField("Mã số sinh viên (MSSV)", validators=[DataRequired(), Length(min=6, max=20)])
    full_name = StringField("Họ và tên", validators=[DataRequired(), Length(max=100)])
    email = StringField("Email trường cấp (@fpt.edu.vn)", validators=[DataRequired(), Email()])
    password = PasswordField("Mật khẩu", validators=[DataRequired(), Length(min=6, message="Mật khẩu phải từ 6 ký tự trở lên.")])
    phone = StringField("Số điện thoại liên hệ", validators=[Optional(), Length(max=20)])
    submit = SubmitField("Đăng Ký")

    def validate_email(self, field):
        email = field.data.strip().lower()
        if not (email.endswith("@fpt.edu.vn") or email.endswith("@fe.edu.vn")):
            raise ValidationError("Email không hợp lệ! Bạn phải sử dụng email do Đại học FPT cấp (@fpt.edu.vn hoặc @fe.edu.vn). Sinh viên trường khác không được phép đăng ký tài khoản.")

    def validate_student_id(self, field):
        sid = field.data.strip().upper()
        if len(sid) < 6:
            raise ValidationError("Mã số sinh viên không hợp lệ (ví dụ: DExxxxxx, SExxxxxx).")

    def validate_phone(self, field):
        """Custom Validator: Số điện thoại Việt Nam chuẩn 10 chữ số bắt đầu bằng 0 (Bài Lab 6)."""
        if field.data:
            p = field.data.strip()
            if not re.match(r"^0\d{9}$", p):
                raise ValidationError("Số điện thoại không hợp lệ! Phải gồm đúng 10 chữ số và bắt đầu bằng số 0.")


class ProfileForm(FlaskForm):
    full_name = StringField("Họ và tên", validators=[DataRequired(), Length(max=100)])
    phone = StringField("Số điện thoại", validators=[Optional()])
    avatar_url = StringField("Ảnh đại diện (URL)", validators=[Optional()])
    submit = SubmitField("Cập Nhật Thông Tin")

    def validate_phone(self, field):
        """Custom Validator: SĐT chuẩn 10 chữ số bắt đầu bằng số 0 (Lab 6)."""
        if field.data:
            p = field.data.strip()
            if not re.match(r"^0\d{9}$", p):
                raise ValidationError("Số điện thoại không hợp lệ! Phải gồm đúng 10 chữ số và bắt đầu bằng số 0.")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Mật khẩu hiện tại", validators=[DataRequired()])
    new_password = PasswordField("Mật khẩu mới", validators=[
        DataRequired(),
        Length(min=6, message="Mật khẩu mới phải dài ít nhất 6 ký tự.")
    ])
    confirm_password = PasswordField("Xác nhận mật khẩu mới", validators=[
        DataRequired(),
        EqualTo("new_password", message="Mật khẩu xác nhận không khớp.")
    ])
    submit = SubmitField("Đổi Mật Khẩu")


class EventCreateForm(FlaskForm):
    title = StringField("Tiêu đề sự kiện", validators=[DataRequired(), Length(max=255)])
    category_id = SelectField("Danh mục sự kiện", coerce=int, validators=[DataRequired()])
    venue = StringField("Địa điểm tổ chức (Hội trường / Phòng Lab)", validators=[DataRequired()])
    start_time = DateTimeLocalField("Thời gian bắt đầu", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    end_time = DateTimeLocalField("Thời gian kết thúc", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    total_capacity = IntegerField("Tổng số ghế tham dự (Slot)", validators=[DataRequired(), NumberRange(min=5, max=1000)])
    speaker_name = StringField("Diễn giả / Khách mời", validators=[Optional()])
    speaker_title = StringField("Chức danh diễn giả", validators=[Optional()])
    banner_url = StringField("Đường dẫn ảnh Banner Poster", validators=[Optional()])
    description_md = TextAreaField("Mô tả chi tiết nội dung sự kiện (Hỗ trợ Markdown)", validators=[DataRequired()])
    submit = SubmitField("Lưu Sự Kiện")


class EventEditForm(EventCreateForm):
    status = SelectField("Trạng thái sự kiện", choices=[
        ("OPEN", "Đang mở đăng ký (OPEN)"),
        ("FULL", "Đã đủ chỗ (FULL)"),
        ("COMPLETED", "Đã kết thúc (COMPLETED)"),
        ("CANCELLED", "Đã hủy (CANCELLED)")
    ], default="OPEN")


class CategoryForm(FlaskForm):
    name = StringField("Tên danh mục", validators=[DataRequired(), Length(max=100)])
    slug = StringField("Đường dẫn tĩnh (Slug)", validators=[DataRequired(), Length(max=100)])
    icon = StringField("Biểu tượng FontAwesome", default="fa-calendar-star", validators=[Optional()])
    color = StringField("Mã màu hiển thị (HEX)", default="#f26f21", validators=[Optional()])
    description = StringField("Mô tả ngắn", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Lưu Danh Mục")


class CheckInManualForm(FlaskForm):
    ticket_code = StringField("Mã vé cần Check-in (Ví dụ: FU-2026-X89AD)", validators=[DataRequired(), Length(min=5, max=50)])
    submit = SubmitField("Xác Nhận Check-in")


class ReviewForm(FlaskForm):
    rating = SelectField("Đánh giá sao", coerce=int, choices=[
        (5, "⭐⭐⭐⭐⭐ Xuất sắc (5 sao)"),
        (4, "⭐⭐⭐⭐ Rất tốt (4 sao)"),
        (3, "⭐⭐⭐ Bình thường (3 sao)"),
        (2, "⭐⭐ Cần cải thiện (2 sao)"),
        (1, "⭐ Chưa tốt (1 sao)")
    ], default=5, validators=[DataRequired()])
    comment = TextAreaField("Cảm nhận của bạn về sự kiện", validators=[DataRequired(), Length(min=5, max=1000)])
    submit = SubmitField("Gửi Đánh Giá")
