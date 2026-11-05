# FPTU EventHub: Form Definitions (Flask-WTF)

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, IntegerField, SelectField, DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange, ValidationError

class LoginForm(FlaskForm):
    email = StringField("Email FPT hoặc Mã SV (MSSV)", validators=[DataRequired()])
    password = PasswordField("Mật khẩu", validators=[DataRequired()])
    remember_me = BooleanField("Ghi nhớ đăng nhập")

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
    password = PasswordField("Mật khẩu", validators=[DataRequired(), Length(min=6)])
    phone = StringField("Số điện thoại liên hệ", validators=[Optional(), Length(max=20)])

    def validate_email(self, field):
        email = field.data.strip().lower()
        if not (email.endswith("@fpt.edu.vn") or email.endswith("@fe.edu.vn")):
            raise ValidationError("Email không hợp lệ! Bạn phải sử dụng email do Đại học FPT cấp (@fpt.edu.vn hoặc @fe.edu.vn). Sinh viên trường khác không được phép đăng ký tài khoản.")

    def validate_student_id(self, field):
        sid = field.data.strip().upper()
        if len(sid) < 6:
            raise ValidationError("Mã số sinh viên không hợp lệ (ví dụ: DE200433, SE171234).")

class EventCreateForm(FlaskForm):
    title = StringField("Tiêu đề sự kiện", validators=[DataRequired(), Length(max=255)])
    category_id = SelectField("Danh mục sự kiện", coerce=int, validators=[DataRequired()])
    venue = StringField("Địa điểm tổ chức (Hội trường / Phòng Lab)", validators=[DataRequired()])
    start_time = DateTimeLocalField("Thời gian bắt đầu", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    end_time = DateTimeLocalField("Thời gian kết thúc", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    total_capacity = IntegerField("Tổng số ghế tham dự (Slot)", validators=[DataRequired(), NumberRange(min=5, max=1000)])
    pdp_points = IntegerField("Điểm rèn luyện PDP (+PDP)", default=10, validators=[DataRequired(), NumberRange(min=0, max=50)])
    speaker_name = StringField("Diễn giả / Khách mời", validators=[Optional()])
    speaker_title = StringField("Chức danh diễn giả", validators=[Optional()])
    banner_url = StringField("Đường dẫn ảnh Banner Poster", validators=[Optional()])
    description_md = TextAreaField("Mô tả chi tiết nội dung sự kiện (Hỗ trợ Markdown)", validators=[DataRequired()])

class CheckInManualForm(FlaskForm):
    ticket_code = StringField("Mã vé cần Check-in (Ví dụ: FU-2026-X89AD)", validators=[DataRequired(), Length(min=5, max=50)])

class ReviewForm(FlaskForm):
    rating = SelectField("Đánh giá sao", coerce=int, choices=[(5, "⭐⭐⭐⭐⭐ Xuất sắc (5 sao)"), (4, "⭐⭐⭐⭐ Rất tốt (4 sao)"), (3, "⭐⭐⭐ Bình thường (3 sao)"), (2, "⭐⭐ Cần cải thiện (2 sao)"), (1, "⭐ Chưa tốt (1 sao)")], default=5, validators=[DataRequired()])
    comment = TextAreaField("Cảm nhận của bạn về sự kiện", validators=[DataRequired(), Length(min=5, max=1000)])
