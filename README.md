# 🎓 FPTU EventHub — Cổng Quản Lý & Đăng Ký Sự Kiện Sinh Viên FPT University

> **Dự án Môn Học**: Phát Triển Ứng Dụng Web với Python (Course Project)  
> **Chủ đề**: Quản lý sự kiện, Hội thảo công nghệ, Workshop & Tích lũy điểm rèn luyện PDP  
> **Tham chiếu thực tế**: [events.fptu.vn](https://events.fptu.vn/)  
> **Công nghệ cốt lõi**: Python Flask, Flask-SQLAlchemy, Jinja2, Bootstrap, Bleach, HTML5 QR Scanner, Canvas Confetti  
> **Sinh viên thực hiện**: Trương Công Dũng (DE200433) cùng nhóm 5 thành viên  

---

## 📌 1. Giới Thiệu Dự Án (Project Overview)
Hàng tuần tại Đại học FPT diễn ra hàng chục sự kiện, workshop công nghệ, cuộc thi học thuật và chương trình văn hóa của hơn 30 CLB. Quy trình đăng ký truyền thống bằng Google Form bộc lộ nhiều điểm yếu:
- Không giới hạn số lượng slot ghế tự động, dễ xảy ra tình trạng đăng ký vượt quá sức chứa hội trường.
- Thiếu cơ chế cấp vé điện tử định danh và mã QR để điểm danh nhanh tại bàn đón tiếp.
- Khó thống kê danh sách sinh viên thực tế tham gia để chuyển giao cho Phòng CTSV cộng điểm rèn luyện PDP.

**FPTU EventHub** ra đời nhằm giải quyết toàn diện các vấn đề trên với giao diện hiện đại 2026 mang đậm nhận diện FPT, phân quyền chặt chẽ giữa Sinh viên, Ban tổ chức CLB và Cán bộ CTSV.

---

## 🚀 2. Điểm Nhấn Hiện Đại & Tính Năng Độc Đáo (Modern Highlights)
1. **Chế Độ Dark Mode / Light Mode**: Công tắc chuyển đổi giao diện sáng/tối chuẩn công nghệ cao với animation mượt mà, lưu trạng thái tự động vào `localStorage`.
2. **Đồng Hồ Đếm Ngược Trực Tiếp (Live Countdown Timer)**: Đếm ngược Ngày : Giờ : Phút : Giây đến sự kiện công nghệ/hackathon lớn sắp diễn ra ngay trên Hero banner.
3. **Bộ Lọc & Tìm Kiếm Tức Thì (Instant Live Filter)**: Gõ tìm kiếm tới đâu card sự kiện tự động lọc tức thì không cần tải lại trang.
4. **Quét Mã QR Check-in Bằng Camera**: Ban tổ chức dùng camera điện thoại/laptop quét trực tiếp mã QR trên vé của sinh viên, âm thanh beep và pháo hoa (Confetti) chúc mừng tức thì.
5. **Theo Dõi Điểm Rèn Luyện PDP & Cấp E-Certificate**: Tự động tích lũy điểm PDP sau khi check-in, xuất **Giấy Chứng Nhận Điện Tử (E-Certificate)** chuẩn FPT có thể in hoặc lưu file PDF (`window.print()`).
6. **Đồng Bộ Google Calendar**: Thêm lịch sự kiện vào Google Calendar với 1 cú click.
7. **Đánh Giá & Review 5 Sao**: Sinh viên chấm sao và chia sẻ cảm nhận sau sự kiện.
8. **Xuất Báo Cáo Ra Excel / CSV**: Organizer và Admin tải file CSV chuẩn UTF-8 BOM nộp trực tiếp cho phòng CTSV.

---

## 🛠️ 3. Công Nghệ & Công Cụ Sử Dụng (Tech Stack)
* **Backend**: Python 3.14 + Flask Micro-framework
* **ORM & Database**: Flask-SQLAlchemy
  - Hỗ trợ kiến trúc đa CSDL (Dual-database): Kết nối SQL Server trên Localhost qua `ODBC Driver 17`, tự động chuyển sang SQLite Serverless tại `/tmp` khi triển khai trên Cloud Vercel.
* **Authentication**: Flask-Login, Werkzeug Password Hashing (Băm mật khẩu an toàn SHA-256)
* **Bảo mật & Chống XSS**: `bleach` làm sạch nội dung bài viết Markdown
* **QR Scanner & Client FX**: `html5-qrcode` CDN (Camera scanning), `canvas-confetti` (Hiệu ứng pháo hoa), Web Audio API
* **Giao diện Frontend**: HTML5, CSS3 BEM Scoped (`.feh-...`), Bootstrap 3, FontAwesome 6, Google Fonts (*Plus Jakarta Sans*, *Cinzel*)
* **Triển khai & CI/CD**: Git, GitHub, Vercel Platform

---

## 🏛️ 4. Kiến Trúc Dự Án (Architecture & Database ERD)
Hệ thống được thiết kế theo mô hình **MVC (Model - View - Controller)** chuẩn mực:
```text
fptu_eventhub/
├── app.py                  # Controller & Routing Handlers, API QR Scan, Export CSV
├── models.py               # Data Models (Role, User, Category, Event, Ticket, Review)
├── forms.py                # Form Validation (Flask-WTF)
├── decorators.py           # Custom Decorators kiểm soát quyền (RBAC)
├── markdown_utils.py       # Bộ lọc an toàn Markdown chống Stored XSS
├── seed_events.py          # Seeder dữ liệu mẫu thực tế FPTU
├── static/
│   ├── css/style.css       # BEM-Scoped CSS, Dark Theme, Glassmorphism, Print CSS
│   ├── js/main.js          # Dark Mode, Countdown, Instant Filter & Confetti
│   └── images/events/      # 100% Ảnh thực tế ĐH FPT (daihoc.fpt.edu.vn & Wikimedia)
├── templates/              # Jinja2 Views kế thừa base.html
│   ├── certificate.html    # Mẫu Giấy Chứng Nhận Tham Gia E-Certificate in/lưu PDF
│   ├── checkin.html        # Bàn Check-in quét Camera trực tiếp
│   └── ...
├── test_eventhub.py        # Bộ kiểm thử tự động Unit Tests (7/7 Passed)
└── vercel.json             # Cấu hình triển khai Serverless
```

### Sơ đồ Thực thể Cơ sở dữ liệu (ERD):
1. **`roles`**: Phân quyền hệ thống (*Student*, *Organizer*, *Admin*).
2. **`users`**: Người dùng (`student_id` - MSSV, `full_name`, `email`, `password_hash`, `role_id`, `total_pdp_points`).
3. **`categories`**: Danh mục (*Công nghệ & AI*, *Học thuật & Hackathon*, *Kỹ năng mềm*, *Văn hóa CLB*, *Thể thao PDP*).
4. **`events`**: Sự kiện (`title`, `venue`, `start_time`, `end_time`, `total_capacity`, `available_slots`, `pdp_points`, `banner_url`, `average_rating`).
5. **`tickets`**: Vé điện tử (`ticket_code`, `qr_url`, `status`: *REGISTERED*, *CHECKED_IN*, *CANCELLED*, `checked_in_at`).
6. **`reviews`**: Đánh giá sự kiện (`rating` 1-5 sao, `comment`, `user_id`, `event_id`).

---

## 📋 5. Kịch Bản Thuyết Trình Nhóm 5 Người (45 - 50 Phút)

| STT | Thành viên phụ trách | Nội dung trình bày trên Slide & Demo | Thời gian |
| :---: | :--- | :--- | :---: |
| **1** | **Thành viên 1 (Leader)** | **Mục 1:** Giới thiệu bài toán thực tế FPTU + **Mục 2:** Tech Stack & Bộ ảnh thực tế ĐH FPT | 7 phút |
| **2** | **Thành viên 2** | **Mục 3:** Kiến trúc MVC, Dual-Database Switch & Thiết kế CSDL (ERD, PDP Points) | 8 phút |
| **3** | **Thành viên 3** | **Mục 4:** Phân tích Chức năng & Sơ đồ UseCase (Sinh viên, Organizer, CTSV) | 8 phút |
| **4** | **Thành viên 4** | **Demo Sinh Viên:** Bật/tắt Dark Mode, Countdown Timer, Tìm kiếm tức thì, Đăng ký vé, Thêm Google Calendar & Mở E-Certificate | 8 phút |
| **5** | **Thành viên 5** | **Demo Ban Tổ Chức:** Tạo sự kiện mới (+PDP), Bật Camera quét QR Check-in trực tiếp (Pháo hoa Confetti), Xuất file Excel báo cáo điểm danh | 8 phút |
| **Q&A**| **Cả nhóm** | Trả lời câu hỏi vấn đáp của Giảng viên (2 - 3 câu/người) | 10 - 12 phút |

---

## 🔑 Tài Khoản Dùng Thử Có Sẵn Trong Database:
- **Sinh viên:** `dungtcde200433@fpt.edu.vn` (Mật khẩu: `pass123` | MSSV: `DE200433` - Đã có sẵn 1 vé Workshop AI được check-in sẵn 10 điểm PDP để demo E-Certificate ngay).
- **Ban tổ chức:** `fcode.club@fpt.edu.vn` (Mật khẩu: `pass123` - CLB F-Code có quyền tạo sự kiện và mở bàn Check-in Camera).
- **Admin CTSV:** `ctsv.admin@fpt.edu.vn` (Mật khẩu: `pass123` - Quyền Quản trị viên cao nhất).
