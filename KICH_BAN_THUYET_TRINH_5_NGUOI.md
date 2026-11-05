# 🎓 KỊCH BẢN THUYẾT TRÌNH & CẨM NANG VẤN ĐÁP BẢO VỆ ĐỒ ÁN (45 - 50 PHÚT)
## Dự Án: FPTU EventHub — Cổng Quản Lý & Đăng Ký Sự Kiện Sinh Viên FPT University

---

## ⏱️ PHÂN BỔ THỜI GIAN TỔNG THỂ (45 - 50 PHÚT)
* **Phần 1 (Thành viên 1 - Leader Trương Công Dũng):** Giới thiệu đề tài, bối cảnh thực tế ĐH FPT & Mục tiêu giải pháp (8 phút)
* **Phần 2 (Thành viên 2):** Các công nghệ, thư viện & giải pháp kỹ thuật bảo mật (8 phút)
* **Phần 3 (Thành viên 3):** Kiến trúc dự án MVC, Dual-Database Switch & Thiết kế CSDL ERD (8 phút)
* **Phần 4 (Thành viên 4):** Phân tích UseCase & Live Demo Luồng Sinh Viên (8 phút)
* **Phần 5 (Thành viên 5):** Phân tích UseCase & Live Demo Luồng Ban Tổ Chức / CTSV + Kết luận (9 phút)
* **Phần Q&A Vấn Đáp (Cả nhóm):** Giảng viên đặt 2–3 câu hỏi cho từng thành viên để chấm điểm cá nhân (10 phút)

---

## 👤 THÀNH VIÊN 1: TRƯƠNG CÔNG DŨNG (NHÓM TRƯỞNG)
### 🎯 Nội dung trình bày trên Slide (Slide 1 → Slide 5):
1. **Lời mở đầu & Giới thiệu thành viên nhóm**:
   - Chào cô và cả lớp. Nêu tên nhóm, đề tài: *"FPTU EventHub — Cổng Quản lý & Đăng ký sự kiện sinh viên Đại học FPT"*.
2. **Bối cảnh thực tế tại FPT University**:
   - FPTU có hơn 30 CLB học thuật, nghệ thuật, thể thao và hàng tuần diễn ra rất nhiều Workshop công nghệ, Talkshow kỹ năng mềm, giải đấu Vovinam.
   - Tham chiếu cổng thông tin thực tế: `events.fptu.vn`.
3. **Bài toán đặt ra (Pain Points của phương pháp cũ)**:
   - Các CLB trước đây dùng **Google Form** để đăng ký vé → Dễ bị quá tải chỗ ngồi (vượt sức chứa hội trường 100 chỗ nhưng Form nhận 200 người).
   - Điểm danh thủ công bằng giấy hoặc dò Excel rất chậm, dễ gian lận điểm danh hộ.
   - Sinh viên không có vé điện tử định danh và khó theo dõi điểm rèn luyện PDP (Personal Development Program).
4. **Mục tiêu & Giải pháp của FPTU EventHub**:
   - Tự động hóa giữ chỗ theo thời gian thực (hết chỗ tự động khóa nút đăng ký).
   - Cấp vé điện tử có mã QR định danh duy nhất (`FU-2026-XXXXXX`).
   - Tích hợp số hóa điểm PDP và cấp Giấy Chứng Nhận Điện Tử (E-Certificate).

### ❓ 3 Câu hỏi vấn đáp thường gặp & Trả lời mẫu:
* **Câu 1: Tại sao không dùng Google Forms cho nhanh?**  
  *Trả lời:* Google Forms không giới hạn được số chỗ tự động theo thời gian thực (dễ vỡ trận hội trường), không sinh được vé mã QR định danh riêng cho từng sinh viên, và không có hệ thống phân quyền liên kết với MSSV để tích lũy điểm PDP.
* **Câu 2: Hệ thống phân quyền như thế nào?**  
  *Trả lời:* Dùng mô hình RBAC chuẩn gồm 3 Role: Sinh viên (tìm kiếm, đăng ký, in chứng nhận), Ban tổ chức CLB (đăng sự kiện, bật camera quét QR điểm danh, xuất Excel) và Cán bộ CTSV (quản trị toàn diện).
* **Câu 3: Quy trình từ đăng ký đến khi có điểm PDP?**  
  *Trả lời:* Đăng ký vé (trừ 1 slot & nhận mã QR) → Đến hội trường xuất trình vé → Ban tổ chức dùng camera quét QR thành công → Tự động cộng điểm PDP và mở khóa Giấy chứng nhận E-Certificate.

---

## 👤 THÀNH VIÊN 2: CÔNG NGHỆ & BẢO MẬT (TECH STACK)
### 🎯 Nội dung trình bày trên Slide (Slide 6 → Slide 10):
1. **Backend Framework**: Python 3.14 + Flask Micro-framework (tốc độ cao, linh hoạt).
2. **Authentication & Security**:
   - Flask-Login quản lý session phiên làm việc.
   - Werkzeug băm mật khẩu với thuật toán PBKDF2/SHA-256 kèm Salt ngẫu nhiên.
   - Flask-WTF bảo vệ chống tấn công CSRF (Cross-Site Request Forgery).
3. **Phòng chống XSS (Stored XSS Protection)**:
   - Thư viện `bleach` kiểm duyệt mã nguồn Markdown, loại bỏ 100% các thẻ độc hại `<script>`, `<iframe onerror=...>` trước khi render.
4. **Frontend & Hiệu ứng 2026**:
   - BEM CSS Scoped (`.feh-...`), Dark Mode toggle lưu vào `localStorage`.
   - `html5-qrcode` xử lý camera trực tiếp trên WebRTC.
   - `canvas-confetti` tạo hiệu ứng pháo hoa chúc mừng khi check-in.

### ❓ 3 Câu hỏi vấn đáp thường gặp & Trả lời mẫu:
* **Câu 1: Mật khẩu người dùng được bảo vệ thế nào?**  
  *Trả lời:* Tuyệt đối không lưu plaintext. Dùng hàm `generate_password_hash()` băm một chiều và `check_password_hash()` để so sánh chuỗi băm khi đăng nhập, an toàn trước nguy cơ rò rỉ CSDL.
* **Câu 2: Tác dụng của thư viện `bleach`?**  
  *Trả lời:* Lọc sạch nội dung HTML/Markdown do người dùng nhập vào, chỉ giữ lại các thẻ định dạng an toàn như in đậm, in nghiêng, gạch đầu dòng và tiêu diệt các đoạn mã độc JavaScript gây lỗ hổng Stored XSS.
* **Câu 3: Camera quét QR hoạt động bằng cơ chế gì?**  
  *Trả lời:* Dùng WebRTC `navigator.mediaDevices.getUserMedia` thông qua thư viện `html5-qrcode`, chụp luồng video 10 FPS để giải mã barcode ngay trên trình duyệt và gửi request ngầm (fetch API) về server.

---

## 👤 THÀNH VIÊN 3: KIẾN TRÚC DỰ ÁN & CƠ SỞ DỮ LIỆU (ERD)
### 🎯 Nội dung trình bày trên Slide (Slide 11 → Slide 16):
1. **Kiến trúc MVC (Model - View - Controller)**:
   - Model: `models.py` (6 bảng: Roles, Users, Categories, Events, Tickets, Reviews).
   - View: `templates/` (Jinja2 Templates) & `static/` (CSS/JS/Images).
   - Controller: `app.py` định tuyến request, xử lý logic và transaction.
2. **Cơ chế Dual-Database Switch**:
   - Chạy Local: Kết nối Microsoft SQL Server (`ODBC Driver 17`). Nếu chưa bật SQL Server thì tự chuyển sang SQLite cục bộ.
   - Chạy Cloud (Vercel): Tự động dùng SQLite Serverless tại thư mục `/tmp` tạm thời.
3. **Sơ đồ ERD & Ràng buộc toàn vẹn**:
   - Quan hệ 1-N giữa `Role` và `User`, `Category` và `Event`, `User` và `Ticket`.
   - Thuộc tính `cascade="all, delete-orphan"` đảm bảo tính toàn vẹn khi xóa sự kiện.
   - Bảng `Review` tính điểm đánh giá trung bình 1-5 sao cho từng sự kiện.

### ❓ 3 Câu hỏi vấn đáp thường gặp & Trả lời mẫu:
* **Câu 1: Làm sao chặn 1 sinh viên đăng ký 2 vé cho 1 sự kiện?**  
  *Trả lời:* Kiểm tra ở cả tầng Backend (`Ticket.query.filter_by(user_id=..., event_id=..., status='REGISTERED')`) và ẩn nút đăng ký ở tầng Frontend khi sinh viên đã sở hữu vé.
* **Câu 2: Cơ chế trừ và hoàn trả slot ghế hoạt động ra sao?**  
  *Trả lời:* Sử dụng Database Transaction trong khối `try...except`. Khi đăng ký: `available_slots -= 1` và commit; nếu lỗi thì rollback. Khi sinh viên hủy vé: chuyển trạng thái `CANCELLED` và `available_slots += 1` để nhường ghế cho người khác.
* **Câu 3: Tại sao lại áp dụng Dual-Database Switch?**  
  *Trả lời:* Để vừa đáp ứng yêu cầu môn học về Microsoft SQL Server trên môi trường máy trường, vừa tương thích 100% với môi trường điện toán đám mây Serverless của Vercel trên Internet.

---

## 👤 THÀNH VIÊN 4: USECASE & LIVE DEMO LUỒNG SINH VIÊN
### 🎯 Nội dung trình bày trên Slide & Thao tác Demo (Slide 17 → Slide 22):
1. **Sơ đồ UseCase Sinh Viên**: Tìm kiếm, Xem chi tiết, Đặt vé, Quản lý vé, In E-Certificate, Đánh giá 5 sao.
2. **Các bước Live Demo thực tế**:
   - **Bước 1:** Bật/tắt nút **Dark Mode** trên thanh Menu để cô giáo thấy hiệu ứng chuyển đổi giao diện sáng/tối chuẩn công nghệ cao.
   - **Bước 2:** Chỉ vào **Đồng hồ đếm ngược (Countdown Timer)** đang đếm lùi thời gian thực tới sự kiện tiếp theo.
   - **Bước 3:** Gõ vào ô **Tìm kiếm tức thì** chữ *"AI"* hoặc bấm thẻ danh mục &rarr; Danh sách sự kiện lọc ngay tức khắc.
   - **Bước 4:** Đăng nhập tài khoản sinh viên `dungtcde200433@fpt.edu.vn` (Pass: `pass123`).
   - **Bước 5:** Vào sự kiện Hackathon &rarr; Bấm **"Đăng Ký Giữ Chỗ Ngay"** &rarr; Thông báo thành công và chuyển sang **"Vé Của Tôi"**.
   - **Bước 6:** Bấm **"Thêm vào Google Calendar"** &rarr; Tự động đồng bộ lịch vào điện thoại.
   - **Bước 7:** Bấm **"Xem & In Giấy Chứng Nhận"** của sự kiện đã check-in &rarr; Mở Giấy Chứng Nhận E-Certificate sang trọng (+10 PDP) và bấm in PDF.

### ❓ 3 Câu hỏi vấn đáp thường gặp & Trả lời mẫu:
* **Câu 1: Khi sự kiện hết vé (Sold Out), sinh viên có hack đăng ký được không?**  
  *Trả lời:* Không thể. Nút đăng ký trên giao diện đã bị khóa disabled và ở tầng Backend có lệnh `if event.available_slots <= 0` chặn đứng mọi request can thiệp trái phép.
* **Câu 2: Tính năng Live Search hoạt động như thế nào mà không cần tải lại trang?**  
  *Trả lời:* Xử lý bằng Client-side JavaScript. Các thẻ sự kiện mang sẵn các thuộc tính `data-title`, `data-venue`. Khi người dùng gõ phím, sự kiện `input` sẽ so sánh chuỗi và ẩn đi các card không khớp bằng CSS `display: none` ngay lập tức.
* **Câu 3: Giấy chứng nhận E-Certificate được cấp khi nào?**  
  *Trả lời:* Chỉ khi vé đạt trạng thái `CHECKED_IN` (Ban tổ chức đã quét mã xác nhận tại cửa). Nếu chưa check-in hoặc đã hủy vé thì không thể truy cập chứng nhận này.

---

## 👤 THÀNH VIÊN 5: USECASE & LIVE DEMO BAN TỔ CHỨC / ADMIN
### 🎯 Nội dung trình bày trên Slide & Thao tác Demo (Slide 23 → Slide 28):
1. **Sơ đồ UseCase Ban Tổ Chức & Admin CTSV**: Tạo sự kiện, Bàn check-in Camera, Xuất Excel, Quản trị CTSV.
2. **Các bước Live Demo thực tế**:
   - **Bước 1:** Đăng nhập tài khoản CLB: `fcode.club@fpt.edu.vn` (Pass: `pass123`).
   - **Bước 2:** Vào **"Dashboard Ban tổ chức"** &rarr; Xem thống kê tỷ lệ lấp đầy ghế (Fill rate %).
   - **Bước 3:** Bấm **"Đăng sự kiện mới"** &rarr; Thiết lập số ghế (100) và Điểm PDP (+10) &rarr; Tạo thành công.
   - **Bước 4 (Điểm nhấn đỉnh cao):** Vào **"Bàn Check-in"**:
     - Bấm **"Bật Camera Quét Mã QR"**.
     - Đưa mã QR của vé sinh viên trước camera &rarr; **Ting! Âm thanh vang lên + Pháo hoa Confetti bắn rực rỡ** kèm thông báo điểm danh thành công +10 PDP.
     - Quét lại mã đó lần nữa &rarr; Cảnh báo màu vàng: *"Vé này ĐÃ CHECK-IN lúc ...!"* chứng minh tính năng chống gian lận.
   - **Bước 5:** Vào danh sách người tham dự &rarr; Bấm **"Xuất File CSV / Excel"** &rarr; Tải về file danh sách điểm danh mở lên tiếng Việt hoàn hảo.
   - **Bước 6:** Đăng nhập Admin `ctsv.admin@fpt.edu.vn` (Pass: `pass123`) &rarr; Xem bảng điều khiển quản trị CTSV.
   - **Tổng kết:** Cảm ơn cô giáo và hội đồng phản biện.

### ❓ 3 Câu hỏi vấn đáp thường gặp & Trả lời mẫu:
* **Câu 1: Nếu camera hỏng hoặc mạng chập chờn thì điểm danh bằng cách nào?**  
  *Trả lời:* Hệ thống có sẵn tab 'Nhập mã thủ công'. Sinh viên chỉ cần đọc mã vé hoặc MSSV, ban tổ chức gõ vào ô và bấm Xác nhận là hoàn tất trong 2 giây.
* **Câu 2: Làm sao để file CSV xuất ra không bao giờ bị lỗi font tiếng Việt trên Windows?**  
  *Trả lời:* Thêm tiền tố BOM (Byte Order Mark `\ufeff`) vào đầu file CSV trong hàm xử lý của Python và khai báo header `mimetype='text/csv; charset=utf-8'`, giúp Excel trên Windows tự nhận diện Unicode tiếng Việt 100%.
* **Câu 3: Dự án có thể tích hợp vào hệ thống cổng trường FAP/myFPT không?**  
  *Trả lời:* Có thể tích hợp dễ dàng nhờ kiến trúc chuẩn RESTful API. Chỉ cần đấu nối với hệ thống SSO của trường và gọi Webhook đồng bộ điểm danh sang phòng CTSV để cập nhật điểm rèn luyện PDP tự động sau mỗi kỳ học.

---

## 🏆 KINH NGHIỆM ĐẠT ĐIỂM 10 CỦA GIẢNG VIÊN:
1. **Đồng bộ trang phục**: Cả nhóm mặc áo cam FPT hoặc sơ mi trắng đồng bộ.
2. **Phối hợp nhịp nhàng**: Khi thành viên này nói, thành viên kia thao tác chuột sẵn sàng trên màn hình chiếu.
3. **Tự tin trả lời vấn đáp**: Bắt đầu bằng *"Dạ em cảm ơn câu hỏi rất hay của cô..."* và trả lời gãy gọn theo các câu trả lời mẫu ở trên.
