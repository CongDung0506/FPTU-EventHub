# 🎓 FPTU EventHub — Cổng Quản Lý & Đăng Ký Sự Kiện Sinh Viên FPT University

> **Dự án Môn Học**: Phát Triển Ứng Dụng Web với Python (Course Project)  
> **Chủ đề**: Quản lý sự kiện, Hội thảo công nghệ, Workshop & Tích lũy điểm rèn luyện PDP  
> **Tham chiếu thực tế**: [events.fptu.vn](https://events.fptu.vn/)  
> **Công nghệ cốt lõi**: Python Flask, Flask-SQLAlchemy, Jinja2, Bootstrap, Bleach, Vercel Serverless  
> **Sinh viên thực hiện**: Trương Công Dũng (DE200433) cùng nhóm 5 thành viên  

---

## 📌 1. Giới Thiệu Dự Án (Project Overview)
Hàng tuần tại Đại học FPT diễn ra hàng chục sự kiện, workshop công nghệ, cuộc thi học thuật và chương trình văn hóa của hơn 30 CLB. Quy trình đăng ký truyền thống bằng Google Form bộc lộ nhiều điểm yếu:
- Không giới hạn số lượng slot ghế tự động, dễ xảy ra tình trạng đăng ký vượt quá sức chứa hội trường.
- Thiếu cơ chế cấp vé điện tử định danh và mã QR để điểm danh nhanh tại bàn đón tiếp.
- Khó thống kê danh sách sinh viên thực tế tham gia để chuyển giao cho Phòng CTSV cộng điểm rèn luyện PDP.

**FPTU EventHub** ra đời nhằm giải quyết toàn diện các vấn đề trên với giao diện hiện đại mang đậm nhận diện FPT, phân quyền chặt chẽ giữa Sinh viên, Ban tổ chức CLB và Cán bộ CTSV.

---

## 🛠️ 2. Công Nghệ & Công Cụ Sử Dụng (Tech Stack)
* **Backend**: Python 3.14 + Flask Micro-framework
* **ORM & Database**: Flask-SQLAlchemy
  - Hỗ trợ kiến trúc đa CSDL (Dual-database): Kết nối SQL Server trên Localhost qua `ODBC Driver 17`, tự động chuyển sang SQLite Serverless tại `/tmp` khi triển khai trên Cloud Vercel.
* **Authentication**: Flask-Login, Werkzeug Password Hashing (Băm mật khẩu an toàn SHA-256)
* **Bảo mật & Chống XSS**: `bleach` làm sạch nội dung bài viết Markdown
* **Mã Vé & QR Code**: Thư viện QR Code Serverless, tự động sinh mã vé duy nhất `FU-2026-XXXXXX`
* **Giao diện Frontend**: HTML5, CSS3 BEM Scoped (`.feh-...`), Bootstrap 3, FontAwesome 6, Google Fonts (*Plus Jakarta Sans*)
* **Triển khai & CI/CD**: Git, GitHub, Vercel Platform

---

## 🏛️ 3. Kiến Trúc Dự Án (Architecture & Database ERD)
Hệ thống được thiết kế theo mô hình **MVC (Model - View - Controller)** chuẩn mực:
```text
fptu_eventhub/
├── app.py                  # Controller & Routing Handlers
├── models.py               # Data Models (Role, User, Category, Event, Ticket)
├── forms.py                # Form Validation (Flask-WTF)
├── decorators.py           # Custom Decorators kiểm soát quyền (RBAC)
├── markdown_utils.py       # Bộ lọc an toàn Markdown chống Stored XSS
├── seed_events.py          # Seeder dữ liệu mẫu thực tế FPTU
├── static/
│   └── css/style.css       # BEM-Scoped CSS, độc bản, không xung đột class
├── templates/              # Jinja2 Views kế thừa base.html
├── test_eventhub.py        # Bộ kiểm thử tự động Unit Tests (6/6 Passed)
└── vercel.json             # Cấu hình triển khai Serverless
```

### Sơ đồ Thực thể Cơ sở dữ liệu (ERD):
1. **`roles`**: Phân quyền hệ thống (*Student*, *Organizer*, *Admin*).
2. **`users`**: Thông tin người dùng (`student_id` - MSSV, `full_name`, `email`, `password_hash`, `role_id`).
3. **`categories`**: Danh mục (*Công nghệ & AI*, *Học thuật & Hackathon*, *Kỹ năng mềm*, *Văn hóa CLB*, *Thể thao PDP*).
4. **`events`**: Sự kiện (`title`, `venue`, `start_time`, `end_time`, `total_capacity`, `available_slots`, `speaker_name`, `banner_url`, `description_html`).
5. **`tickets`**: Vé điện tử (`ticket_code`, `qr_url`, `status`: *REGISTERED*, *CHECKED_IN*, *CANCELLED*, `checked_in_at`).

---

## 🎯 4. Chức Năng Chính (Use Cases)
* **Actor 1: Sinh viên (Student)**
  - UC01: Xem & Tìm kiếm sự kiện theo từ khóa, lọc theo danh mục.
  - UC02: Xem chi tiết sự kiện, tiến độ lấp đầy chỗ ngồi (`Còn X/Y chỗ`).
  - UC03: Đăng ký vé 1-Click (Tự động trừ 1 slot trong Transaction).
  - UC04: Quản lý "Vé Của Tôi", hiển thị mã QR Check-in.
  - UC05: Hủy vé tham dự (Hệ thống tự động hoàn lại 1 slot trống cho người khác).
* **Actor 2: Ban Tổ Chức (Organizer)**
  - UC06: Tạo mới sự kiện, cấu hình sức chứa hội trường.
  - UC07: Dashboard thống kê tỷ lệ lấp đầy ghế (Fill rate %).
  - UC08: Xem danh sách sinh viên tham dự & Điểm danh tại bàn đón tiếp.
  - UC09: Tra cứu & Quét mã vé check-in, chống check-in trùng lặp.
* **Actor 3: Quản trị viên CTSV (Admin)**
  - UC10: Giám sát toàn bộ hoạt động phong trào và quản lý danh mục.

---

## 📋 5. Kịch Bản Thuyết Trình Nhóm 5 Người (45 - 50 Phút)

| STT | Thành viên phụ trách | Nội dung trình bày trên Slide | Thời gian |
| :---: | :--- | :--- | :---: |
| **1** | **Thành viên 1 (Leader)** | **Mục 1:** Giới thiệu dự án FPTU EventHub + **Mục 2:** Công nghệ & Tools | 7 phút |
| **2** | **Thành viên 2** | **Mục 3:** Kiến trúc MVC, Dual-Database Switch & Thiết kế CSDL ERD | 8 phút |
| **3** | **Thành viên 3** | **Mục 4:** Phân tích Chức năng & Sơ đồ UseCase (4 Luồng chính) | 8 phút |
| **4** | **Thành viên 4** | **Mục 5.1:** Live Demo Trải nghiệm Sinh viên (Tìm kiếm, Đăng ký vé & QR code) | 8 phút |
| **5** | **Thành viên 5** | **Mục 5.2:** Live Demo Ban tổ chức & Admin (Tạo sự kiện, Bàn Check-in điểm danh) | 8 phút |
| **Q&A**| **Cả nhóm** | Trả lời câu hỏi vấn đáp của Giảng viên (2 - 3 câu/người) | 10 - 12 phút |

---

## 🔑 Tài Khoản Dùng Thử Có Sẵn Trong Database:
- **Sinh viên:** `dungtcde200433@fpt.edu.vn` (Mật khẩu: `pass123` | MSSV: `DE200433`)
- **Ban tổ chức:** `fcode.club@fpt.edu.vn` (Mật khẩu: `pass123`)
- **Admin CTSV:** `ctsv.admin@fpt.edu.vn` (Mật khẩu: `pass123`)
