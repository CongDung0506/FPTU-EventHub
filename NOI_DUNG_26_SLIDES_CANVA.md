# TỔNG HỢP NỘI DUNG 26 SLIDES THUYẾT TRÌNH FPTU EVENTHUB (CANVA READY)
> **Dành cho:** Thiết kế trực tiếp trên Canva / PowerPoint  
> **Thời lượng:** 45 – 50 phút (Chia đều 5 thành viên, mỗi người 5 – 6 slides ~ 8 – 10 phút)  
> **Quy chuẩn:** Tối đa 3 – 4 dòng/thẻ, từ khóa in đậm, chỉ số KPI to, không đoạn văn dài, 0% nhắc đến điểm rèn luyện/PDP.

---

## 👤 PHẦN 1: GIỚI THIỆU DỰ ÁN & BỐI CẢNH (Thành viên 1: Trương Công Dũng - Lead)
*Thời lượng trình bày: ~9 - 10 phút (Slide 1 -> Slide 6)*

---

### 🔹 SLIDE 1: TIÊU ĐỀ DỰ ÁN (HERO COVER)
* **Bố cục đề xuất:** Chia 2 cột (Trái: Chữ & Huy hiệu | Phải: Ảnh Campus FPTU + 2 Huy hiệu nổi).
* **Nội dung đưa vào Slide:**
  * **Huy hiệu trên cùng:** `TRƯỜNG ĐẠI HỌC FPT — BẢO VỆ ĐỒ ÁN CHUYÊN NGÀNH SE`
  * **Tiêu đề lớn:** `FPTU EventHub`
  * **Tiêu đề phụ:** Nền Tảng Điều Hành & Đăng Ký Sự Kiện Sinh Viên Toàn Diện
  * **3 Điểm nổi bật (Icon check):**
    * `✓ Zero-SSO:` Đăng nhập 1-chạm bằng Email FPT / MSSV
    * `✓ Khóa Chỗ Atomic:` Chống quá tải, không bao giờ vỡ trận hội trường
    * `✓ Check-in Camera < 1s:` Quét mã QR trực tiếp qua trình duyệt web
  * **Huy hiệu thông tin:** `Nhóm 5 Thành Viên • Thời lượng: 45 - 50 Phút • Live: fptu-event-hub.vercel.app`
* **Gợi ý ảnh/icon:** Ảnh sảnh trường FPT University, Logo FPT Education, icon 🎓, ⚡, 🟢.

---

### 🔹 SLIDE 2: BỐI CẢNH & THỰC TRẠNG PHONG TRÀO FPTU
* **Bố cục đề xuất:** 3 Thẻ chỉ số lớn (KPI Cards) ở trên + 2 Hộp Bento ở dưới.
* **Nội dung đưa vào Slide:**
  * **3 Chỉ số KPI khổng lồ:**
    * **`30+ CLB`** — Phong trào hoạt động bùng nổ (Học thuật, công nghệ, nghệ thuật, thể thao)
    * **`100+ Buổi/Kỳ`** — Tần suất sự kiện liên tục (Workshop AI, Talkshow doanh nghiệp, Hackathon)
    * **`100 - 250 Chỗ`** — Sức chứa giới hạn của Hội trường Alpha/Beta và Lab máy tính
  * **Hộp 1: Thách Thức Không Gian**
    * **Áp lực sức chứa:** Không thể nhận dư người vì phòng máy và ghế có hạn.
    * **Thế hệ Gen Z:** Muốn thao tác 1-chạm trên điện thoại, có vé mã QR rõ ràng.
  * **Hộp 2: Nhu Cầu Quản Trị**
    * **Cán bộ CTSV:** Cần hệ thống số hóa tập trung thay cho hàng chục file Excel rời rạc.
* **Gợi ý ảnh/icon:** Ảnh sinh viên tham gia sự kiện CLB / Hội thảo, icon 🏫, 👥, 📍.

---

### 🔹 SLIDE 3: 4 THÁCH THỨC TỪ CỔNG CŨ & THỰC TẾ SỰ KIỆN FPTU
* **Bố cục đề xuất:** 4 Thẻ cảnh báo nền đỏ nhạt/viền đỏ (Grid 2x2).
* **Nội dung đưa vào Slide:**
  * **Thẻ 1: 🚨 Vỡ Trận Sức Chứa (Overbooking)**
    * Cổng cũ không khóa số lượng tự động theo thời gian thực khi sinh viên đăng ký dồn dập.
    * Hội trường chỉ có 100 chỗ nhưng lượng đăng ký vượt quá sức chứa, gây khó khăn cho ban tổ chức.
  * **Thẻ 2: 🎟️ Vấn Nạn "Ghế Ảo" (Đăng Ký Xong Không Đi)**
    * Tham gia sự kiện là hoàn toàn tự nguyện, đi hay không là tùy sinh viên.
    * Tuy nhiên, hệ thống cũ KHÔNG CÓ NÚT HỦY VÉ: Sinh viên bận đột xuất cứ thế bỏ qua, khiến hệ thống báo hết chỗ nhưng hội trường thực tế lại trống ghế, lãng phí cơ hội của bạn khác.
  * **Thẻ 3: 📱 Bất Tiện Cho Bạn Quản Lý Khi Quét Mã Check-in**
    * Khi đến sự kiện, có bạn quản lý đứng tại cửa quét mã vé để điểm danh sinh viên.
    * Hệ thống cũ yêu cầu cài đặt phần mềm/app riêng cồng kềnh, đối soát chậm khi sinh viên vào đông, và thiếu cảnh báo nếu vé bị quét trùng lặp (chụp màn hình quét hộ).
  * **Thẻ 4: 📊 Dữ Liệu Điểm Danh Không Đồng Bộ Tức Thì**
    * Cán bộ CTSV không theo dõi được ngay số lượng sinh viên thực tế đã có mặt tại hội trường.
    * Ban tổ chức phải chờ xuất và gộp dữ liệu thủ công sau sự kiện để báo cáo.

---

### 🔹 SLIDE 4: MỤC TIÊU & TẦM NHÌN ĐỘT PHÁ CỦA DỰ ÁN
* **Bố cục đề xuất:** 3 Chỉ số cam kết to bản + Hộp tóm tắt 3 Trụ cột.
* **Nội dung đưa vào Slide:**
  * **3 Chỉ số cam kết:**
    * **`0.1 Giây`** — Thời gian giữ chỗ thành công với Transaction nguyên tử
    * **`< 1 Giây`** — Tốc độ nhận diện và check-in mã QR qua camera WebRTC cho bạn quản lý
    * **`100%`** — Tự động hóa: Cấp vé QR, hủy vé nhả slot ngay, đồng bộ sĩ số CTSV
  * **3 Trụ Cột Đổi Mới:**
    * **Thời gian thực (Real-time):** Đồng bộ số vé còn lại tức thì, hết ghế tự ngắt đăng ký.
    * **Chấm dứt ghế ảo:** Sinh viên chủ động hủy vé trả lại slot cho bạn có nhu cầu.
    * **Bàn quét QR WebRTC tối ưu:** Bạn quản lý mở trình duyệt quét ngay trên điện thoại/laptop, không cần cài app, phát hiện vé quét trùng lặp tức thì.

---

### 🔹 SLIDE 5: BATTLE BOARD — SO SÁNH ĐỐI ĐẦU TRỰC QUAN
* **Bố cục đề xuất:** 2 Cột song song (Trái: Thẻ đỏ ❌ | Phải: Thẻ xanh ✅ | Giữa: Huy hiệu tròn VS).
* **Nội dung đưa vào Slide:**
  * **Cột Trái: ❌ CỔNG CŨ CỦA TRƯỜNG**
    * Không kiểm soát sức chứa thời gian thực, dễ quá tải số lượng đăng ký
    * Không có nút hủy vé: Sinh viên bận không nhường ghế được, gây ra "ghế ảo"
    * Bạn quản lý phải dùng app riêng hoặc thao tác đối soát quét mã cồng kềnh
    * Không cảnh báo tức thì khi mã vé bị quét lại lần 2 (nguy cơ quét hộ)
    * Dữ liệu điểm danh không đồng bộ thời gian thực cho Cán bộ CTSV
  * **Cột Phải: ✅ FPTU EVENTHUB ĐỘT PHÁ 2026**
    * Khóa chỗ tự động bằng Transaction CSDL: Hết ghế tự ngắt đăng ký tức thì
    * Hủy vé 1-chạm hoàn slot: Sinh viên chủ động trả vé, giải phóng ghế cho bạn khác
    * Bàn Check-in WebRTC tiện lợi: Bạn quản lý mở web quét mã camera trong 0.1s
    * Chống gian lận: Vé đã quét lập tức báo đỏ "Đã check-in", ngăn quét trùng
    * Đồng bộ Dashboard thời gian thực: Cán bộ CTSV thấy ngay sĩ số thực tế và xuất Excel 1-click
* **Gợi ý ảnh/icon:** Huy hiệu tròn `VS` màu cam FPT ở giữa, icon ❌ và ✅.

---

### 🔹 SLIDE 6: MÔ HÌNH ĐỊNH VỊ GIÁ TRỊ (3 TRỤ CỘT)
* **Bố cục đề xuất:** 3 Cột Bento đứng tương ứng 3 đối tượng thụ hưởng.
* **Nội dung đưa vào Slide:**
  * **Cột 1: 🎓 Dành Cho Sinh Viên**
    * Xem lịch sự kiện toàn trường tập trung, đăng ký bằng email FPT.
    * Sở hữu vé QR trên điện thoại, điểm danh không chạm.
    * Chủ động hủy vé khi có việc bận, xem lại toàn bộ lịch sử tham gia.
  * **Cột 2: 🛡️ Dành Cho CTSV & Ban Tổ Chức**
    * Không sợ quá tải hội trường nhờ cơ chế khóa sức chứa cứng.
    * Bàn quét camera quét liên tục, cảnh báo vé giả / vé đã dùng.
    * Xuất danh sách tham gia ra file Excel phục vụ lưu trữ chỉ với 1-click.
  * **Cột 3: 🏛️ Dành Cho Đại Học FPT**
    * Hiện đại hóa công tác chuyển đổi số phong trào sinh viên.
    * Tối ưu hóa 100% không gian cơ sở vật chất (hội trường, phòng máy).
    * Dữ liệu điểm danh minh bạch, không còn tình trạng gian lận.
* **Gợi ý ảnh/icon:** Icon sinh viên 🎓, icon quản trị 🛡️, icon trường đại học 🏛️.

---

## 👤 PHẦN 2: PHÂN CÔNG NHIỆM VỤ & QUẢN TRỊ DỰ ÁN (Thành viên 2: Nguyễn Việt Anh - PM)
*Thời lượng trình bày: ~8 - 9 phút (Slide 7 -> Slide 10)*

---

### 🔹 SLIDE 7: CHÂN DUNG & PHÂN CÔNG 5 THÀNH VIÊN
* **Bố cục đề xuất:** 5 Thẻ Persona đặt nằm ngang (Mỗi thẻ 1 màu nhấn riêng).
* **Nội dung đưa vào Slide:**
  * **Thẻ 1: Trương Công Dũng (DE200433) — Trưởng Nhóm & System Architect**
    * Thiết kế kiến trúc tổng thể MVC, giải thuật khóa vé Atomic, điều phối nhóm.
    * `⭐ Đóng góp: 20%`
  * **Thẻ 2: Nguyễn Việt Anh (SE190111) — PM & Scrum Master**
    * Quản lý tiến độ 4 Sprint Jira, mô hình hóa quan hệ CSDL, quy chuẩn Gitflow.
    * `⭐ Đóng góp: 20%`
  * **Thẻ 3: Lê Hoàng Long (SE190222) — Security & Backend Lead**
    * 4 Lá chắn bảo mật OWASP, mã hóa băm mật khẩu, thuật toán Token QR.
    * `⭐ Đóng góp: 20%`
  * **Thẻ 4: Trần Minh Quang (SE190333) — Fullstack & UI/UX Lead**
    * Thiết kế giao diện Responsive, tích hợp camera WebRTC, kịch bản Demo.
    * `⭐ Đóng góp: 20%`
  * **Thẻ 5: Phạm Đức Trọng (SE190444) — QA & Test Lead**
    * Thiết kế 15 Unit Tests tự động, kiểm thử tải đồng thời, tối ưu Vercel.
    * `⭐ Đóng góp: 20%`
* **Gợi ý ảnh/icon:** Icon lập trình viên 👨‍💻, huy hiệu sao ⭐.

---

### 🔹 SLIDE 8: CÔNG CỤ QUẢN LÝ DỰ ÁN & CỘNG TÁC
* **Bố cục đề xuất:** 4 Thẻ vuông (Grid 2x2).
* **Nội dung đưa vào Slide:**
  * **Thẻ 1: 📋 Jira & Trello (Quản trị Agile/Scrum)**
    * Phân rã User Stories thành 24 Tasks, gán Story Points rõ ràng.
    * Bảng Kanban 4 cột (To Do -> In Progress -> Code Review -> Done).
  * **Thẻ 2: 🐙 GitHub Enterprise (Quản lý mã nguồn)**
    * Phân chia nhánh Gitflow, bắt buộc tạo Pull Request có review chéo.
    * Tích hợp CI/CD tự động kiểm tra code trước khi merge.
  * **Thẻ 3: 🎨 Figma (Thiết kế UI/UX)**
    * Wireframe & Prototype giao diện chuẩn Responsive (Mobile & Laptop).
    * Thiết kế luồng thao tác bàn quét QR tối ưu cho điện thoại.
  * **Thẻ 4: 💬 Discord & Slack (Giao tiếp nhóm)**
    * Họp Daily Standup 15 phút mỗi ngày, thông báo Webhook tự động khi có code mới.
* **Gợi ý ảnh/icon:** Logo Jira, GitHub, Figma, Discord.

---

### 🔹 SLIDE 9: KẾ HOẠCH TRIỂN KHAI 4 SPRINT AGILE
* **Bố cục đề xuất:** Lộ trình 4 cột mũi tên từ trái sang phải.
* **Nội dung đưa vào Slide:**
  * **Sprint 1 (Tuần 1 - 2): Khởi Tạo & Khảo Sát**
    * Khảo sát thực trạng events.fptu.vn, lấy ý kiến sinh viên và CTSV.
    * Thiết kế CSDL 6 bảng quan hệ, phác thảo giao diện trên Figma.
  * **Sprint 2 (Tuần 3 - 4): Tính Năng Cốt Lõi**
    * Phân quyền RBAC (Sinh viên / CTSV), đặt vé giữ chỗ 1-click.
    * Cơ chế khóa vé Atomic, sinh mã QR động kèm Token bảo mật.
  * **Sprint 3 (Tuần 5 - 6): Bàn Quét QR & Quản Trị**
    * Tích hợp WebRTC Camera Scanner quét trực tiếp trên trình duyệt.
    * Xây dựng Dashboard quản trị CTSV và module xuất báo cáo Excel.
  * **Sprint 4 (Tuần 7 - 8): Kiểm Thử & Đóng Gói**
    * Viết 15 Unit Tests tự động, kiểm thử tải đồng thời.
    * Triển khai lên máy chủ Vercel Serverless, hoàn thiện tài liệu bảo vệ.
* **Gợi ý ảnh/icon:** Icon mũi tên lộ trình ➡️, mốc thời gian 📅.

---

### 🔹 SLIDE 10: QUY TRÌNH GITFLOW & CỔNG KIỂM SOÁT CODE
* **Bố cục đề xuất:** 2 Hộp lớn (Trái: Nhánh Gitflow | Phải: 4 Bước Quality Gate).
* **Nội dung đưa vào Slide:**
  * **Hộp Trái: Cấu Trúc Nhánh Gitflow**
    * `main`: Nhánh ổn định tuyệt đối, tự động deploy lên Vercel.
    * `develop`: Nhánh tích hợp các tính năng đã kiểm thử.
    * `feature/*`: Nhánh làm việc riêng của từng thành viên.
    * `hotfix/*`: Vá lỗi khẩn cấp trực tiếp khi có sự cố.
  * **Hộp Phải: 4 Cổng Kiểm Soát Chất Lượng (Quality Gate)**
    * `Bước 1:` Lập trình viên chạy `pytest` kiểm tra cục bộ trước khi push.
    * `Bước 2:` Tạo Pull Request mô tả chi tiết kèm ảnh kết quả test.
    * `Bước 3:` Ít nhất 1 thành viên khác (Lead/Architect) review code.
    * `Bước 4:` Hợp nhất vào develop/main, hệ thống Vercel tự build trong 45s.
* **Gợi ý ảnh/icon:** Sơ đồ phân nhánh cây Git, icon 🌳, 🛡️.

---

## 👤 PHẦN 3: KIẾN TRÚC PHẦN MỀM & CÔNG NGHỆ (Thành viên 3: Lê Hoàng Long - Architect)
*Thời lượng trình bày: ~9 - 10 phút (Slide 11 -> Slide 15)*

---

### 🔹 SLIDE 11: TỔNG QUAN TECH STACK HIỆN ĐẠI
* **Bố cục đề xuất:** 4 Cột Bento đứng tương ứng 4 mảng công nghệ.
* **Nội dung đưa vào Slide:**
  * **Cột 1: 🎨 Frontend (Giao diện)**
    * HTML5, CSS3, Bootstrap 5: Responsive trên mọi thiết bị.
    * Vanilla JavaScript: Tương tác nhanh, nhẹ, không cồng kềnh.
    * HTML5-QRCode: Giải mã camera WebRTC trực tiếp.
  * **Cột 2: ⚙️ Backend (Nghiệp vụ)**
    * Python 3.11: Xử lý hiệu năng cao, cú pháp trong sáng.
    * Flask Framework: Nhẹ, linh hoạt, tối ưu cho Serverless.
    * Werkzeug Security: Băm mật khẩu chuẩn PBKDF2/SHA-256.
  * **Cột 3: 🗄️ Database (Lưu trữ)**
    * SQLAlchemy ORM: Truy vấn an toàn, chống SQL Injection 100%.
    * SQLite (Local) & PostgreSQL (Cloud Ready): ACID Transactions.
  * **Cột 4: 🚀 Infrastructure (Hạ tầng)**
    * Vercel Serverless: Tự động co giãn theo tải, HTTPS bảo mật.
    * GitHub Actions: CI/CD tự động kiểm thử và triển khai.
* **Gợi ý ảnh/icon:** Logo Python, Flask, HTML5, Bootstrap, SQLite, Vercel.

---

### 🔹 SLIDE 12: KIẾN TRÚC PHẦN MỀM MVC 3 TẦNG
* **Bố cục đề xuất:** 3 Khối tầng xếp chồng từ trên xuống dưới (View -> Controller -> Model).
* **Nội dung đưa vào Slide:**
  * **TẦNG 1: VIEW (Giao Diện & Tương Tác)**
    * Jinja2 Templates: Render giao diện linh hoạt theo vai trò người dùng.
    * WebRTC Camera: Thu nhận khung hình video từ camera để quét mã QR.
    * Fetch API: Giao tiếp dữ liệu bất đồng bộ với Backend không cần tải lại trang.
  * **TẦNG 2: CONTROLLER (Điều Khiển & Nghiệp Vụ)**
    * Flask Blueprints: Chia nhỏ module (Auth, Events, Admin, Scanner).
    * Session Guard: Kiểm tra quyền hạn `@login_required`, `@admin_required`.
    * Transaction Controller: Quản lý nghiệp vụ khóa vé và xác thực Token.
  * **TẦNG 3: MODEL (Cơ Sở Dữ Liệu & ORM)**
    * SQLAlchemy Models: Định nghĩa 6 thực thể và quan hệ bảng.
    * ACID Transaction: Đảm bảo tính nhất quán dữ liệu khi xảy ra lỗi.
* **Gợi ý ảnh/icon:** Sơ đồ khối 3 tầng có mũi tên 2 chiều, icon 🏗️, 📦.

---

### 🔹 SLIDE 13: MÔ HÌNH CƠ SỞ DỮ LIỆU 6 BẢNG CHUẨN HÓA
* **Bố cục đề xuất:** Lưới 6 thẻ bảng CSDL (Grid 3x2).
* **Nội dung đưa vào Slide:**
  * **`User` (Tài khoản):** `id`, `email`, `mssv`, `full_name`, `password_hash`, `role` (Student / Admin CTSV).
  * **`Event` (Sự kiện):** `id`, `title`, `location`, `start_time`, `max_slots` (sức chứa), `registered_count`, `status`.
  * **`Ticket` (Vé điện tử):** `id`, `user_id` (FK), `event_id` (FK), `ticket_code` (mã QR), `status`, `checkin_time`.
  * **`Category` (Danh mục):** `id`, `name`, `description`, `icon` (Công nghệ, Học thuật, Kỹ năng, Thể thao...).
  * **`AuditLog` (Nhật ký):** `id`, `user_id`, `action`, `ip_address`, `timestamp` (Lưu vết hành động nhạy cảm).
  * **`SecurityToken` (Khóa bảo mật):** `id`, `ticket_id`, `secret_hash`, `expires_at` (Chống vé giả).
* **Gợi ý ảnh/icon:** Biểu tượng bảng dữ liệu CSDL 🗄️, sơ đồ thực thể ERD.

---

### 🔹 SLIDE 14: 4 LÁ CHẮN AN TOÀN THÔNG TIN OWASP
* **Bố cục đề xuất:** 4 Thẻ hình khiên bảo vệ (Grid 2x2).
* **Nội dung đưa vào Slide:**
  * **Lá Chắn 1: 🔒 Chống Giả Mạo CSRF Token**
    * Tự động sinh mã Token ngẫu nhiên cho mọi biểu mẫu gửi dữ liệu.
    * Chặn đứng kẻ xấu gửi yêu cầu đặt vé trái ý muốn của người dùng.
  * **Lá Chắn 2: 🔑 Băm Mật Khẩu Werkzeug PBKDF2**
    * Tuyệt đối không lưu mật khẩu thô, mã hóa qua hàng nghìn vòng băm.
    * Kèm muối ngẫu nhiên (Salt), vô hiệu hóa hoàn toàn bảng Rainbow.
  * **Lá Chắn 3: 👤 Phân Quyền Vai Trò RBAC Ngặt Nghèo**
    * Sinh viên không thể xem hay gọi các URL quản trị của CTSV.
    * Decorator kiểm tra phiên làm việc trên từng hàm route xử lý.
  * **Lá Chắn 4: ⚡ Khóa Dữ Liệu Đồng Thời (Concurrency Lock)**
    * Giao dịch nguyên tử: Khóa dòng sự kiện khi có yêu cầu đặt chỗ.
    * Ngăn ngừa tình trạng 2 sinh viên cùng nhận được chiếc vé cuối cùng.
* **Gợi ý ảnh/icon:** Icon khiên bảo vệ 🛡️, khóa 🔒, chìa khóa 🔑.

---

### 🔹 SLIDE 15: CƠ CHẾ KHÓA VÉ CHỐNG OVERBOOKING
* **Bố cục đề xuất:** 3 Chỉ số tình huống ở trên + Quy trình xử lý chi tiết ở dưới.
* **Nội dung đưa vào Slide:**
  * **3 Chỉ số tình huống:**
    * **`1 Vé Cuối Cùng`** — Tình huống hội trường chỉ còn đúng 1 slot ghế trống
    * **`50 Sinh Viên`** — Số lượng sinh viên cùng bấm nút đăng ký tại cùng một giây
    * **`Đúng 1 Người Trúng`** — Hệ thống cấp vé chính xác, không bao giờ nhận thừa
  * **Quy Trình Xử Lý Giao Dịch Nguyên Tử (Atomic Transaction):**
    * `1. Bắt đầu (BEGIN):` Mở phiên làm việc độc lập với cơ sở dữ liệu.
    * `2. Khóa dòng (LOCK):` Tạm khóa dòng sự kiện trong CSDL để đối soát.
    * `3. Kiểm tra (CHECK):` Đảm bảo số vé đã cấp < sức chứa tối đa.
    * `4. Tăng đếm & Cấp vé:` Ghi nhận vé cho người đến trước mili-giây.
    * `5. Xác nhận (COMMIT):` Lưu vĩnh viễn và báo 'Hết chỗ' cho 49 người sau.
* **Gợi ý ảnh/icon:** Sơ đồ luồng dữ liệu Concurrency, icon ⚡, 🎯, 🔄.

---

## 👤 PHẦN 4: TÍNH NĂNG CHÍNH & LIVE DEMO (Thành viên 4: Trần Minh Quang - Fullstack)
*Thời lượng trình bày: ~11 - 12 phút (Slide 16 -> Slide 21, gồm 8 phút Live Demo)*

---

### 🔹 SLIDE 16: PHÂN HỆ DÀNH CHO SINH VIÊN
* **Bố cục đề xuất:** Chia 2 cột (Trái: Danh sách 4 tính năng | Phải: Ảnh chụp giao diện/poster sự kiện).
* **Nội dung đưa vào Slide:**
  * **Tiêu đề khối:** Trải Nghiệm Đăng Ký Sự Kiện 1-Chạm
  * **4 Tính năng cốt lõi:**
    * **1. Khám phá sự kiện:** Lọc sự kiện theo danh mục (AI, Kỹ năng, Hackathon, CLB).
    * **2. Đăng ký giữ chỗ 1-Click:** Nhấn đăng ký bằng Email FPT, xác nhận tức thì.
    * **3. Vé điện tử QR cá nhân:** Lưu trong mục 'Vé Của Tôi', chứa mã Token độc bản.
    * **4. Hủy vé hoàn slot tự động:** Bận việc đột xuất có thể hủy vé để nhường ghế cho bạn khác.
* **Gợi ý ảnh/icon:** Ảnh Workshop AI hoặc giao diện vé điện tử trên điện thoại, icon 🎓, 📱, 🎟️.

---

### 🔹 SLIDE 17: PHÂN HỆ DÀNH CHO CÁN BỘ CTSV
* **Bố cục đề xuất:** Chia 2 cột (Trái: 4 Tính năng quản trị | Phải: Ảnh chụp Dashboard CTSV).
* **Nội dung đưa vào Slide:**
  * **Tiêu đề khối:** Trung Tâm Điều Hành & Duyệt Sự Kiện Toàn Trường
  * **4 Tính năng cốt lõi:**
    * **1. Dashboard thống kê tổng thể:** Theo dõi số sự kiện, tổng lượt vé, số người đã đến.
    * **2. Khởi tạo & Quản lý sự kiện:** Cài đặt sức chứa tối đa, địa điểm, thời gian.
    * **3. Bàn quét QR điểm danh WebRTC:** Mở camera máy tính/điện thoại quét mã vé tại cửa.
    * **4. Xuất báo cáo Excel 1-click:** Tải file danh sách sinh viên tham dự chuẩn xác.
* **Gợi ý ảnh/icon:** Ảnh màn hình Dashboard quản trị CTSV, icon 🛡️, 📊, 💻.

---

### 🔹 SLIDE 18: CÔNG NGHỆ BÀN QUÉT QR CAMERA WEBRTC
* **Bố cục đề xuất:** 3 Chỉ số lớn ở trên + 2 Hộp xử lý kỹ thuật ở dưới.
* **Nội dung đưa vào Slide:**
  * **3 Chỉ số vượt trội:**
    * **`0.1 Giây`** — Tốc độ giải mã khung hình camera WebRTC
    * **`0 Cài Đặt`** — Chạy trực tiếp trên trình duyệt, không cần cài App
    * **`1 Lần Dùng`** — Vé đã điểm danh lập tức bị vô hiệu hóa, chống quét lại
  * **3 Tình Huống Xử Lý Thực Tế Tại Cửa:**
    * `Vé Hợp Lệ (Xanh lá):` Hiện Tên + MSSV -> 'Check-in thành công'.
    * `Vé Đã Sử Dụng (Đỏ):` Cảnh báo 'Vé này đã điểm danh lúc 16:30!', chống gian lận.
    * `Vé Không Hợp Lệ (Vàng):` Báo lỗi 'Mã vé không tồn tại trên hệ thống'.
* **Gợi ý ảnh/icon:** Icon ống kính camera 📷, mã QR, màn hình báo xanh/đỏ.

---

### 🔹 SLIDE 19: KỊCH BẢN LIVE DEMO P1 — HÀNH TRÌNH SINH VIÊN
* **Bố cục đề xuất:** Thanh giả lập trình duyệt `🔴 🟡 🟢 https://fptu-event-hub.vercel.app` + 3 Bước thao tác.
* **Nội dung đưa vào Slide:**
  * **Thanh địa chỉ:** `https://fptu-event-hub.vercel.app/events`
  * **Bước 1: Đăng nhập 1-Click**
    * Chọn tài khoản sinh viên: Trương Công Dũng (DE200433).
    * Vào trang chủ xem danh sách các sự kiện đang mở đăng ký.
  * **Bước 2: Đăng ký vé sự kiện**
    * Chọn 'Workshop AI & Google Antigravity', xem thanh tiến độ số chỗ còn lại.
    * Nhấn nút 'ĐĂNG KÝ GIỮ CHỖ NGAY'.
  * **Bước 3: Nhận & Quản lý vé điện tử**
    * Màn hình hiển thị vé QR cá nhân độc bản.
    * Thử nghiệm tính năng 'Hủy vé' để chứng minh số chỗ trống lập tức được hoàn lại.
* **Gợi ý ảnh/icon:** Mockup cửa sổ trình duyệt, icon 🎬, 1️⃣, 2️⃣, 3️⃣.

---

### 🔹 SLIDE 20: KỊCH BẢN LIVE DEMO P2 — ĐIỀU HÀNH CÁN BỘ CTSV
* **Bố cục đề xuất:** Thanh giả lập trình duyệt `🔴 🟡 🟢 https://fptu-event-hub.vercel.app/admin` + 3 Bước thao tác.
* **Nội dung đưa vào Slide:**
  * **Thanh địa chỉ:** `https://fptu-event-hub.vercel.app/admin/dashboard`
  * **Bước 1: Truy cập Trung tâm CTSV**
    * Đăng nhập bằng tài khoản Quản trị: Phòng Công Tác Sinh Viên (CTSV).
    * Giao diện quản trị riêng biệt: Xem tổng số vé, tỷ lệ check-in thực tế.
  * **Bước 2: Bật Bàn Quét Mã QR Camera**
    * Bấm 'Bàn Check-in', camera kích hoạt tức thì.
    * Đưa mã QR trên điện thoại của sinh viên vào quét -> Hệ thống nhận diện < 0.1s.
  * **Bước 3: Xuất báo cáo danh sách Excel**
    * Bấm nút 'Xuất Danh Sách Excel', mở file vừa tải về chứng minh dữ liệu chuẩn xác 100%.
* **Gợi ý ảnh/icon:** Mockup cửa sổ trình duyệt quản trị, icon 🎬, 📷, 📊.

---

### 🔹 SLIDE 21: KẾT QUẢ VẬN HÀNH THỰC TẾ
* **Bố cục đề xuất:** 3 Thẻ chỉ số thành tựu + Hộp tổng kết giá trị mang lại.
* **Nội dung đưa vào Slide:**
  * **3 Chỉ số thành tựu:**
    * **`0 Phút Chờ`** — Sinh viên qua cửa điểm danh chỉ trong 1 giây quét mã
    * **`100% Khớp Ghế`** — Không xảy ra tình trạng thiếu chỗ hay dư thừa người
    * **`1-Click`** — Thời gian tổng hợp và xuất báo cáo hoàn chỉnh cho CTSV
  * **Giá Trị Thực Tế Đạt Được:**
    * Xây dựng văn hóa sự kiện chuyên nghiệp, có trách nhiệm giữ chỗ.
    * Dữ liệu minh bạch phục vụ công tác thống kê phong trào của nhà trường.
    * Sẵn sàng phục vụ các sự kiện quy mô lớn: Ngày hội việc làm, Chung kết Hackathon.
* **Gợi ý ảnh/icon:** Ảnh Ngày hội việc làm FPTU / Hội thao Vovinam, icon 🏆, 📈.

---

## 👤 PHẦN 5: KIỂM THỬ, TƯƠNG LAI & TỔNG KẾT (Thành viên 5: Phạm Đức Trọng - QA Lead)
*Thời lượng trình bày: ~8 - 9 phút (Slide 22 -> Slide 26)*

---

### 🔹 SLIDE 22: CHIẾN LƯỢC KIỂM THỬ TOÀN DIỆN
* **Bố cục đề xuất:** Kim tự tháp 3 tầng kiểm thử (Unit -> Integration -> Performance).
* **Nội dung đưa vào Slide:**
  * **TẦNG 1: UNIT TESTING (Kiểm thử đơn vị)**
    * Kiểm tra độc lập hàm băm mật khẩu `generate_password_hash` & `check_password_hash`.
    * Kiểm tra tính duy nhất tuyệt đối của chuỗi mã vé QR ngẫu nhiên.
    * Kiểm tra logic ràng buộc số lượng vé đăng ký không được vượt quá sức chứa.
  * **TẦNG 2: INTEGRATION TESTING (Kiểm thử tích hợp)**
    * Luồng Đăng ký vé -> Tạo bản ghi Ticket -> Cập nhật số đếm trong Event.
    * Luồng Quét QR -> Giải mã Token -> Ghi nhận thời gian Check-in thực tế.
    * Kiểm tra Decorator chặn sinh viên truy cập vào API của CTSV.
  * **TẦNG 3: PERFORMANCE & LOAD (Kiểm thử hiệu năng)**
    * Giả lập 50 sinh viên cùng bấm nút tranh chiếc vé cuối cùng (Concurrency).
    * Đo độ trễ API và khả năng tương thích của camera trên điện thoại di động.
* **Gợi ý ảnh/icon:** Mô hình kim tự tháp kiểm thử phần mềm, icon 🧪, 🎯.

---

### 🔹 SLIDE 23: BÁO CÁO KẾT QUẢ KIỂM THỬ TỰ ĐỘNG
* **Bố cục đề xuất:** Thẻ điểm xanh khổng lồ ở trên + 2 Hộp phân tích ca test.
* **Nội dung đưa vào Slide:**
  * **Bảng Điểm Xanh Tuyệt Đối:**
    * **`15 / 15 Tests Passed`** — Đạt tỷ lệ thành công 100% kịch bản kiểm thử
    * **`0 Failures / 0 Errors`** — Không có lỗi hồi quy logic
    * **`7.28 Giây`** — Toàn bộ bộ test chạy hoàn tất tự động bằng `pytest`
  * **Phân Bổ 15 Ca Kiểm Thử Đã Chạy:**
    * Xác thực người dùng (3 tests): Đăng nhập thành công, sai mật khẩu, tài khoản rỗng.
    * Quản lý sự kiện (3 tests): Tạo sự kiện, đổi sức chứa, đóng sự kiện.
    * Nghiệp vụ vé (4 tests): Đặt vé thành công, chặn đặt trùng, sự kiện hết chỗ, hủy vé.
    * Bàn quét QR (3 tests): Quét vé hợp lệ, chặn quét vé lần 2, chặn vé giả mạo.
    * An toàn thông tin (2 tests): Chặn quyền sinh viên vào trang CTSV, kiểm tra CSRF.
* **Gợi ý ảnh/icon:** Biểu tượng Passed màu xanh lục ✅, huy hiệu 100%, icon 📋.

---

### 🔹 SLIDE 24: BÁO CÁO HIỆU NĂNG & CHỊU TẢI TRÊN CLOUD
* **Bố cục đề xuất:** 3 Chỉ số đo đạc thực tế + 2 Hộp kỹ thuật tối ưu.
* **Nội dung đưa vào Slide:**
  * **3 Chỉ số đo đạc:**
    * **`< 1 Giây`** — Tốc độ phản hồi trung bình của toàn bộ các trang web
    * **`0.1 Giây`** — Thời gian xử lý giải mã hình ảnh camera WebRTC
    * **`1.2 Giây`** — Thời gian khởi động lạnh (Cold Start) trên máy chủ Vercel Serverless
  * **Kỹ Thuật Tối Ưu Đã Áp Dụng:**
    * Đánh chỉ mục Database Indexing trên cột `ticket_code`, `email`, `mssv`.
    * Nén toàn bộ tài nguyên ảnh và CSS/JS tĩnh xuống dưới 200KB.
    * Tự động co giãn theo tải (Serverless Auto-scale) phục vụ hơn 1,000 sinh viên.
* **Gợi ý ảnh/icon:** Biểu đồ đồng hồ đo tốc độ ⚡, biểu đồ hiệu năng 📊.

---

### 🔹 SLIDE 25: LỘ TRÌNH NÂNG CẤP TƯƠNG LAI
* **Bố cục đề xuất:** 4 Thẻ công nghệ tương lai (Grid 2x2).
* **Nội dung đưa vào Slide:**
  * **Giai Đoạn 1: 🤖 Tích Hợp AI Gợi Ý Sự Kiện Thông Minh**
    * Phân tích lịch sử tham gia để gợi ý sự kiện phù hợp cho từng sinh viên.
    * Tự động tóm tắt nội dung hội thảo bằng mô hình ngôn ngữ lớn (LLM).
  * **Giai Đoạn 2: 📲 Tự Động Hóa Thông Báo Zalo & Telegram**
    * Gửi vé QR trực tiếp về tin nhắn điện thoại.
    * Tự động gửi tin nhắn nhắc nhở 2 tiếng trước giờ diễn ra sự kiện.
  * **Giai Đoạn 3: 👁️ Nhận Diện Khuôn Mặt (FaceID Check-in)**
    * Điểm danh không chạm: Sinh viên bước qua cửa camera tự nhận diện.
    * Rút ngắn thời gian xuống 0.05s, bảo mật sinh trắc học tuyệt đối.
  * **Giai Đoạn 4: 📱 Ứng Dụng Di Động Native (Flutter)**
    * Xây dựng App chạy mượt mà trên cả iOS và Android.
    * Tích hợp lưu vé vào Apple Wallet / Google Wallet trên điện thoại.
* **Gợi ý ảnh/icon:** Icon AI 🤖, icon tin nhắn 📲, icon FaceID 👁️, icon Flutter 📱.

---

### 🔹 SLIDE 26: LỜI CẢM ƠN & BẮT ĐẦU VẤN ĐÁP Q&A
* **Bố cục đề xuất:** Thẻ Card Trung Tâm Lớn (Hero Card) trang trọng, tinh tế.
* **Nội dung đưa vào Slide:**
  * **Dòng trên cùng:** `TRƯỜNG ĐẠI HỌC FPT — BẢO VỆ ĐỒ ÁN CHUYÊN NGÀNH CNTT`
  * **Tiêu đề lớn:** `XIN CHÂN THÀNH CẢM ƠN HỘI ĐỒNG!`
  * **Tiêu đề phụ:** Hệ Thống FPTU EventHub Sẵn Sàng Cho Phần Vấn Đáp (Q&A)
  * **Thông tin đối soát trực tiếp:**
    * `🌐 Website Live Production:` https://fptu-event-hub.vercel.app/
    * `🐙 Kho Lưu Trữ GitHub:` https://github.com/CongDung0506/FPTU-EventHub
    * `👥 Nhóm thực hiện:` Trương Công Dũng (Lead) & 4 Thành Viên
  * **Dòng thông điệp cuối:** `KÍNH MỜI THẦY CÔ TRONG HỘI ĐỒNG ĐẶT CÂU HỎI & ĐÓNG GÓP Ý KIẾN`
* **Gợi ý ảnh/icon:** Mã QR link web, logo FPT Education, icon 🎓, 💬, 👏.
