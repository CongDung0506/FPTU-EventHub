# FPTU EventHub: Database Seeder
# Nap du lieu mau chuan dai hoc FPT (events.fptu.vn)

import os
import uuid
from datetime import datetime, timedelta
from models import db, Role, User, Category, Event, Ticket, Review
from markdown_utils import render_safe_markdown

def seed_data_internal():
    db.create_all()

    if Role.query.first() is None:
        Role.insert_roles()

    role_student = Role.query.filter_by(name="Student").first()
    role_organizer = Role.query.filter_by(name="Organizer").first()
    role_admin = Role.query.filter_by(name="Admin").first()

    # 1. Tai khoan Quan tri vien (CTSV) va Ban to chuc
    admin = User.query.filter_by(email="ctsv.admin@fpt.edu.vn").first()
    if admin is None:
        admin = User(
            student_id="ADM001",
            full_name="Phòng Công Tác Sinh Viên (CTSV)",
            email="ctsv.admin@fpt.edu.vn",
            phone="02367300999",
            avatar_url="/static/images/fpt_logo.jpg",
            role=role_admin
        )
        admin.set_password("pass123")
        db.session.add(admin)
    else:
        admin.student_id = "ADM001"
        admin.full_name = "Phòng Công Tác Sinh Viên (CTSV)"
        admin.role = role_admin

    organizer = User.query.filter_by(email="fcode.club@fpt.edu.vn").first()
    if organizer is None:
        organizer = User(
            student_id="ORG001",
            full_name="CLB Lập Trình F-Code FPTU",
            email="fcode.club@fpt.edu.vn",
            phone="0914888999",
            avatar_url="/static/images/fpt_logo.jpg",
            role=role_organizer
        )
        organizer.set_password("pass123")
        db.session.add(organizer)

    # 2. Danh sach sinh vien FPT phong phu (Ho ten, MSSV, Nganh hoc SE/DE/IA/SS/GD/MC)
    students_roster = [
        {"sid": "DE200433", "name": "Trương Công Dũng", "email": "dungtcde200433@fpt.edu.vn", "phone": "0905123456", "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80"},
        {"sid": "SE190111", "name": "Cao Chí Trung", "email": "trungccse190111@fpt.edu.vn", "phone": "0912345678", "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=300&q=80"},
        {"sid": "SE190222", "name": "Dương Thanh Viên", "email": "vientdse190222@fpt.edu.vn", "phone": "0981123456", "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=300&q=80"},
        {"sid": "SE190333", "name": "Nguyễn Đặng Đình Nam", "email": "namnddse190333@fpt.edu.vn", "phone": "0972234567", "avatar": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?auto=format&fit=crop&w=300&q=80"},
        {"sid": "SE190444", "name": "Lê Anh Tuấn", "email": "tuanlase190444@fpt.edu.vn", "phone": "0963345678", "avatar": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=300&q=80"},
        {"sid": "GD190456", "name": "Huỳnh Bảo Ngọc", "email": "ngochbgd190456@fpt.edu.vn", "phone": "0914456789", "avatar": "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=300&q=80"},
        {"sid": "SE200123", "name": "Võ Quốc Huy", "email": "huyvqse200123@fpt.edu.vn", "phone": "0905567890", "avatar": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=300&q=80"},
        {"sid": "DE190876", "name": "Đỗ Mai Phương", "email": "phuongdmde190876@fpt.edu.vn", "phone": "0986678901", "avatar": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=300&q=80"},
        {"sid": "MC190342", "name": "Nguyễn Khánh Linh", "email": "linhnkmc190342@fpt.edu.vn", "phone": "0977789012", "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80"},
        {"sid": "SE180999", "name": "Bùi Đức Trọng", "email": "trongbdse180999@fpt.edu.vn", "phone": "0968890123", "avatar": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?auto=format&fit=crop&w=300&q=80"},
        {"sid": "IA200145", "name": "Phạm Tuấn Kiệt", "email": "kietptia200145@fpt.edu.vn", "phone": "0919901234", "avatar": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=300&q=80"},
        {"sid": "SE190888", "name": "Hoàng Thảo Nhi", "email": "nhihtse190888@fpt.edu.vn", "phone": "0901012345", "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=300&q=80"},
        {"sid": "SS190777", "name": "Đinh Gia Bảo", "email": "baodgss190777@fpt.edu.vn", "phone": "0982123456", "avatar": "https://images.unsplash.com/photo-1501196354995-cbb51c65aaea?auto=format&fit=crop&w=300&q=80"},
        {"sid": "GD200333", "name": "Trịnh Minh Châu", "email": "chautmgd200333@fpt.edu.vn", "phone": "0973234567", "avatar": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=300&q=80"},
        {"sid": "SE181234", "name": "Vũ Anh Khoa", "email": "khoavase181234@fpt.edu.vn", "phone": "0964345678", "avatar": "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?auto=format&fit=crop&w=300&q=80"},
        {"sid": "DE180555", "name": "Hà Thanh Tùng", "email": "tunghtde180555@fpt.edu.vn", "phone": "0915456789", "avatar": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?auto=format&fit=crop&w=300&q=80"},
        {"sid": "MC190882", "name": "Ngô Phương Thảo", "email": "thaonpmc190882@fpt.edu.vn", "phone": "0906567890", "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=300&q=80"},
        {"sid": "SE190332", "name": "Lâm Gia Hưng", "email": "hunglgse190332@fpt.edu.vn", "phone": "0987678901", "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=300&q=80"},
        {"sid": "IA190221", "name": "Dương Hoài Nam", "email": "namdhyia190221@fpt.edu.vn", "phone": "0978789012", "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=300&q=80"},
        {"sid": "SS180912", "name": "Tạ Thị Thùy Dung", "email": "dungtttss180912@fpt.edu.vn", "phone": "0969890123", "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80"},
        {"sid": "DE200115", "name": "Châu Nhật Minh", "email": "minhcnde200115@fpt.edu.vn", "phone": "0910901234", "avatar": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=300&q=80"},
        {"sid": "SE190445", "name": "Đoàn Quốc Đạt", "email": "datdqse190445@fpt.edu.vn", "phone": "0901023456", "avatar": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?auto=format&fit=crop&w=300&q=80"},
        {"sid": "GD190223", "name": "Lương Bích Trâm", "email": "tramlbgd190223@fpt.edu.vn", "phone": "0982134567", "avatar": "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=300&q=80"},
        {"sid": "IA200889", "name": "Phùng Thế Anh", "email": "anhptia200889@fpt.edu.vn", "phone": "0973245678", "avatar": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=300&q=80"},
        {"sid": "SE180776", "name": "Cao Văn Sơn", "email": "soncvse180776@fpt.edu.vn", "phone": "0964356789", "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=300&q=80"},
        {"sid": "MC200129", "name": "Mai Tuyết Mai", "email": "maimtpmc200129@fpt.edu.vn", "phone": "0915467890", "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=300&q=80"},
        {"sid": "DE190334", "name": "Lưu Vĩnh Phát", "email": "phatlvde190334@fpt.edu.vn", "phone": "0906578901", "avatar": "https://images.unsplash.com/photo-1501196354995-cbb51c65aaea?auto=format&fit=crop&w=300&q=80"},
        {"sid": "SE190667", "name": "Hồ Tấn Tài", "email": "taihtse190667@fpt.edu.vn", "phone": "0987689012", "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=300&q=80"},
        {"sid": "SS190112", "name": "Tống Mỹ Duyên", "email": "duyentmss190112@fpt.edu.vn", "phone": "0978790123", "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=300&q=80"},
        {"sid": "IA180443", "name": "Diệp Gia Tuấn", "email": "tuandgia180443@fpt.edu.vn", "phone": "0969801234", "avatar": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?auto=format&fit=crop&w=300&q=80"},
        {"sid": "SE200554", "name": "Nhan Quốc Khánh", "email": "khanhnqse200554@fpt.edu.vn", "phone": "0910912345", "avatar": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=300&q=80"},
        {"sid": "GD180998", "name": "Quách Ánh Tuyết", "email": "tuyetqagd180998@fpt.edu.vn", "phone": "0901034567", "avatar": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=300&q=80"}
    ]

    student_objs = []
    for s_info in students_roster:
        u = User.query.filter((User.student_id == s_info["sid"]) | (User.email == s_info["email"])).first()
        if u is None:
            u = User(
                student_id=s_info["sid"],
                full_name=s_info["name"],
                email=s_info["email"],
                phone=s_info["phone"],
                avatar_url=s_info["avatar"],
                role=role_student
            )
            u.set_password("pass123")
            db.session.add(u)
        else:
            u.student_id = s_info["sid"]
            u.full_name = s_info["name"]
            u.email = s_info["email"]
            u.phone = s_info["phone"]
            u.avatar_url = s_info["avatar"]
            u.role = role_student
        student_objs.append(u)

    db.session.flush()
    student_main = student_objs[0] # Truong Cong Dung

    # 3. Danh muc su kien FPT (Categories)
    cats_data = [
        {"name": "Công Nghệ & AI", "slug": "tech-ai", "icon": "fa-microchip", "color": "#2563eb", "desc": "Các hội thảo chuyên sâu về Trí tuệ nhân tạo, Phần mềm, Cloud Computing"},
        {"name": "Học Thuật & Hackathon", "slug": "academic-hackathon", "icon": "fa-code", "color": "#f26f21", "desc": "Đấu trường lập trình, cuộc thi học thuật và nghiên cứu khoa học"},
        {"name": "Kỹ Năng & Hướng Nghiệp", "slug": "career-skills", "icon": "fa-briefcase", "color": "#059669", "desc": "Giao lưu doanh nghiệp, phỏng vấn tuyển dụng OJT và kỹ năng mềm"},
        {"name": "Văn Hóa & Câu Lạc Bộ", "slug": "culture-clubs", "icon": "fa-guitar", "color": "#d97706", "desc": "Lễ hội giao lưu, chương trình âm nhạc, kịch nghệ và hoạt động CLB"},
        {"name": "Thể Thao & Phong Trào", "slug": "sports-activities", "icon": "fa-dumbbell", "color": "#7c3aed", "desc": "Giải thi đấu Vovinam, bóng đá, cầu lông và rèn luyện thể chất sinh viên"},
    ]

    cats_map = {}
    for c in cats_data:
        cat_obj = Category.query.filter_by(slug=c["slug"]).first()
        if cat_obj is None:
            cat_obj = Category(
                name=c["name"],
                slug=c["slug"],
                icon=c["icon"],
                color=c["color"],
                description=c["desc"]
            )
            db.session.add(cat_obj)
        cats_map[c["slug"]] = cat_obj

    # 4. Su kien thuc te dai hoc FPT (Co phong kin cho het ve, phong dong sinh vien)
    now = datetime.now()
    events_data = [
        {
            "title": "Workshop: Làm Chủ AI Agentic Coding & Google Antigravity",
            "slug": "workshop-ai-agentic-coding",
            "category": cats_map["tech-ai"],
            "venue": "Hội trường A (Tòa nhà Alpha - FPTU)",
            "start_time": now + timedelta(days=2, hours=9),
            "end_time": now + timedelta(days=2, hours=11, minutes=30),
            "total_capacity": 100,
            "available_slots": 75,
            "speaker_name": "TS. Nguyễn Hoàng Nam",
            "speaker_title": "Senior AI Architect tại FPT Software & Cựu SV FPT",
            "speaker_avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=200&q=80",
            "banner_url": "/static/images/events/workshop_ai.jpg",
            "status": "OPEN",
            "desc_md": """### Khám phá kỷ nguyên lập trình tương lai với AI Agent
Workshop dành riêng cho sinh viên ngành CNTT ĐH FPT, mang đến cái nhìn sâu sắc về cách thức các mô hình ngôn ngữ lớn (LLM) và AI Agentic Assistants cách mạng hóa quy trình viết code:
- **Nội dung 1:** Tổng quan về kiến trúc Multi-Agent & Code Automation.
- **Nội dung 2:** Thực hành tích hợp Google Antigravity SDK vào ứng dụng Web.
- **Nội dung 3:** Hỏi đáp trực tiếp cùng các chuyên gia hàng đầu từ FPT Software.

*Lưu ý: Sinh viên tham dự đầy đủ sẽ được cấp chứng nhận và nhận chứng nhận tham gia sự kiện!*"""
        },
        {
            "title": "F-Code Hackathon 2026: Xây Dựng Ứng Dụng Thông Minh",
            "slug": "f-code-hackathon-2026",
            "category": cats_map["academic-hackathon"],
            "venue": "Phòng Lab AI & Robotics (Tầng 4, Tòa nhà Gamma)",
            "start_time": now + timedelta(days=5, hours=8),
            "end_time": now + timedelta(days=6, hours=18),
            "total_capacity": 20,
            "available_slots": 0, # HET VE - Phong Lab AI kin cho!
            "status": "FULL",
            "speaker_name": "Ban Chuyên Môn CLB F-Code",
            "speaker_title": "Đơn vị tổ chức cuộc thi học thuật ĐH FPT",
            "speaker_avatar": "/static/images/fpt_logo.jpg",
            "banner_url": "/static/images/events/hackathon.jpg",
            "desc_md": """### Cuộc thi lập trình 24 giờ liên tục tại FPT University
Thử thách bản thân trong môi trường áp lực cao để phát triển giải pháp công nghệ phục vụ cộng đồng:
- Tổng giá trị giải thưởng lên đến **50.000.000 VNĐ**.
- Được hỗ trợ Mentor 1-1 từ các công ty công nghệ đối tác.
- Nhận ngay giấy chứng nhận cho các thành viên hoàn thành sản phẩm.
- **Tình trạng:** Phòng thi đấu Lab AI đã đủ số lượng 20 thí sinh (Hết chỗ đăng ký)."""
        },
        {
            "title": "FPT Software Career Talk: Chinh Phục Kỳ Thực Tập OJT 2026",
            "slug": "fsoft-career-talk-ojt",
            "category": cats_map["career-skills"],
            "venue": "Hội trường Beta (Khu Giảng Đường B - FPTU)",
            "start_time": now + timedelta(days=3, hours=14),
            "end_time": now + timedelta(days=3, hours=17),
            "total_capacity": 120,
            "available_slots": 92,
            "speaker_name": "Chị Lê Thu Hà",
            "speaker_title": "Trưởng phòng Tuyển dụng & Đào tạo FPT Software",
            "speaker_avatar": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80",
            "banner_url": "/static/images/events/fsoft_career.jpg",
            "status": "OPEN",
            "desc_md": """### Bước đệm vững chắc chuyển tiếp từ giảng đường ra doanh nghiệp
Dành cho sinh viên từ kỳ 4 trở lên chuẩn bị bước vào kỳ On-the-Job Training (OJT):
- Bí quyết viết CV công nghệ ấn tượng lọt mắt xanh nhà tuyển dụng.
- Mô phỏng phỏng vấn kỹ thuật trực tiếp (Live Mock Interview) trên sân khấu.
- Trao ngay 20 suất thực tập có lương tại các dự án trọng điểm toàn cầu của FSOFT."""
        },
        {
            "title": "Lễ Hội Văn Hóa CLB: Chào Đón Tân Sinh Viên K20 FPTU",
            "slug": "club-festival-welcome-k20",
            "category": cats_map["culture-clubs"],
            "venue": "Sảnh Trung Tâm Tòa Nhà Alpha & Hồ Sen FPTU",
            "start_time": now + timedelta(days=7, hours=17, minutes=30),
            "end_time": now + timedelta(days=7, hours=22),
            "total_capacity": 250,
            "available_slots": 222,
            "speaker_name": "Ban Chấp Hành Đoàn Trường FPTU",
            "speaker_title": "Phòng CTSV phối hợp cùng 30 CLB FPTU",
            "speaker_avatar": "/static/images/fpt_logo.jpg",
            "banner_url": "/static/images/events/club_festival.jpg",
            "status": "OPEN",
            "desc_md": """### Đêm nhạc hội bùng nổ sắc màu sinh viên FPT
- Gian hàng ẩm thực và trải nghiệm từ hơn 30 câu lạc bộ học thuật, nghệ thuật, thể thao.
- Sân khấu biểu diễn ca nhạc, nhảy hiện đại và DJ sôi động.
- Điểm danh nhận vé tham dự và quà lưu niệm CLB."""
        },
        {
            "title": "Giải Vô Địch Vovinam & Võ Thuật Học Đường FPTU",
            "slug": "vovinam-championship-fptu",
            "category": cats_map["sports-activities"],
            "venue": "Nhà Thi Đấu Thể Thao Đa Năng FPT University",
            "start_time": now + timedelta(days=10, hours=7, minutes=30),
            "end_time": now + timedelta(days=10, hours=16),
            "total_capacity": 80,
            "available_slots": 62,
            "speaker_name": "Võ Sư Nguyễn Thanh Tùng",
            "speaker_title": "Trưởng Bộ môn Giáo dục Thể chất Vovinam FPTU",
            "speaker_avatar": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=200&q=80",
            "banner_url": "/static/images/events/vovinam.jpg",
            "status": "OPEN",
            "desc_md": """### Tinh thần thượng võ 'Bàn tay thép đặt lên trái tim từ ái'
- Thi đấu đối kháng các hạng cân nam nữ và biểu diễn quyền đồng đội.
- Cổ vũ nhiệt tình cho các võ sinh FPT tranh tài cúp vô địch năm 2026."""
        },
        {
            "title": "Talkshow: Nghệ Thuật Thuyết Trình & Làm Việc Nhóm Đỉnh Cao",
            "slug": "talkshow-presentation-teamwork",
            "category": cats_map["career-skills"],
            "venue": "Hội trường A (Tòa nhà Alpha)",
            "start_time": now + timedelta(days=1, hours=15),
            "end_time": now + timedelta(days=1, hours=17),
            "total_capacity": 30,
            "available_slots": 0, # HET VE - Chay ve toan bo!
            "status": "FULL",
            "speaker_name": "Thầy Võ Minh Trí",
            "speaker_title": "Giảng viên Xuất Sắc Bộ môn Kỹ năng Mềm FPTU",
            "speaker_avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=200&q=80",
            "banner_url": "/static/images/events/talkshow_skills.jpg",
            "desc_md": """### Vượt qua nỗi sợ đứng trước đám đông và lãnh đạo nhóm hiệu quả
Sự kiện đã nhận được sự quan tâm kỷ lục và **chính thức cháy vé (Sold Out)** trong vòng 2 giờ mở cổng:
- Nghệ thuật thiết kế Storytelling trong thuyết trình đồ án tốt nghiệp.
- Giải quyết mâu thuẫn nội bộ và phân chia deadline công bằng khi làm Capstone.
- **Tình trạng:** Hội trường 30 chỗ đã kín toàn bộ sinh viên đăng ký giữ chỗ."""
        },
        {
            "title": "Hội Thảo An Toàn Thông Tin & Phòng Chống Tấn Công Mạng",
            "slug": "workshop-cyber-security-fpt",
            "category": cats_map["tech-ai"],
            "venue": "Phòng Hội Thảo 302 (Tòa Nhà Gamma - FPTU)",
            "start_time": now + timedelta(days=4, hours=13, minutes=30),
            "end_time": now + timedelta(days=4, hours=16),
            "total_capacity": 15,
            "available_slots": 0, # HET VE - Phong hoi thao 302 kin cho!
            "status": "FULL",
            "speaker_name": "Anh Phạm Quốc Bảo",
            "speaker_title": "Chuyên Gia Bảo Mật Cấp Cao FPT IS",
            "speaker_avatar": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=200&q=80",
            "banner_url": "/static/images/events/cyber_security.jpg",
            "desc_md": """### Phân tích các mối đe dọa an ninh mạng trong kỷ nguyên số
Thực hành trực tiếp tấn công và phòng thủ web (CTF mini challenge):
- Kỹ thuật phòng chống SQL Injection, Cross-Site Scripting (XSS).
- Quản lý khóa bảo mật API và cấu hình mạng an toàn cho doanh nghiệp.
- **Tình trạng:** Phòng hội thảo 302 (15 slot) đã được sinh viên ngành An toàn thông tin đăng ký kín."""
        },
        {
            "title": "Ngày Hội Hiến Máu Nhân Đạo: Giọt Hồng FPTU 2026",
            "slug": "blood-donation-fptu-2026",
            "category": cats_map["culture-clubs"],
            "venue": "Sảnh Tòa Nhà Alpha - FPTU",
            "start_time": now + timedelta(days=8, hours=7),
            "end_time": now + timedelta(days=8, hours=11),
            "total_capacity": 150,
            "available_slots": 124,
            "speaker_name": "Đội Tình Nguyện Sinh Viên FPTU",
            "speaker_title": "Phối hợp cùng Hội Chữ Thập Đỏ & Bệnh viện",
            "speaker_avatar": "/static/images/fpt_logo.jpg",
            "banner_url": "/static/images/events/blood_donation.jpg",
            "status": "OPEN",
            "desc_md": """### Mỗi giọt máu cho đi, một cuộc đời ở lại
Chương trình thiện nguyện truyền thống thường niên của sinh viên FPT:
- Được kiểm tra sức khỏe và xét nghiệm máu miễn phí.
- Nhận giấy chứng nhận hiến máu tình nguyện và quà tặng hỗ trợ bồi dưỡng."""
        }
    ]

    saved_events = []
    for ed in events_data:
        ev = Event.query.filter_by(slug=ed["slug"]).first()
        if ev is None:
            ev = Event(
                title=ed["title"],
                slug=ed["slug"],
                banner_url=ed["banner_url"],
                speaker_name=ed["speaker_name"],
                speaker_title=ed["speaker_title"],
                speaker_avatar=ed["speaker_avatar"],
                venue=ed["venue"],
                start_time=ed["start_time"],
                end_time=ed["end_time"],
                total_capacity=ed["total_capacity"],
                available_slots=ed["available_slots"],
                status=ed.get("status", "OPEN"),
                description_md=ed["desc_md"],
                description_html=render_safe_markdown(ed["desc_md"]),
                category=ed["category"],
                organizer=organizer
            )
            db.session.add(ev)
        else:
            ev.total_capacity = ed["total_capacity"]
            ev.available_slots = ed["available_slots"]
            ev.status = ed.get("status", "OPEN")
            ev.venue = ed["venue"]
            ev.speaker_name = ed["speaker_name"]
            ev.speaker_title = ed["speaker_title"]
            ev.speaker_avatar = ed["speaker_avatar"]
            ev.description_md = ed["desc_md"]
            ev.description_html = render_safe_markdown(ed["desc_md"])
        saved_events.append(ev)

    db.session.flush()

    # 5. Tao Danh Sach Nguoi Tham Gia (Tickets) day du cho tat ca su kien
    # Bao gom ca cac su kien HET VE (Lab AI 20/20, Talkshow 30/30, Hoi thao 15/15)
    # va cac su kien co nhieu sinh vien tham du khac
    if Ticket.query.count() < 30 and len(saved_events) >= 8:
        # Xoa ve cu de nap lai danh sach hoan chinh dong bo
        Ticket.query.delete()
        db.session.flush()

        # Event 0: Workshop AI (100 slot, 25 da dang ky, 18 da check-in)
        # Trong do Truong Cong Dung da check-in (nhan 10 PDP va chung nhan)
        ev0 = saved_events[0]
        t0_main = Ticket(
            ticket_code="FU-2026-AI001",
            qr_url=f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=FU-2026-AI001",
            event=ev0,
            user=student_main,
            status="CHECKED_IN",
            checked_in_at=datetime.utcnow() - timedelta(hours=3),
            registered_at=datetime.utcnow() - timedelta(days=2)
        )
        db.session.add(t0_main)

        for i, s_usr in enumerate(student_objs[1:25], start=2):
            status = "CHECKED_IN" if i <= 18 else "REGISTERED"
            check_time = datetime.utcnow() - timedelta(hours=i % 4 + 1) if status == "CHECKED_IN" else None
            t = Ticket(
                ticket_code=f"FU-2026-AI{i:03d}",
                qr_url=f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=FU-2026-AI{i:03d}",
                event=ev0,
                user=s_usr,
                status=status,
                checked_in_at=check_time,
                registered_at=datetime.utcnow() - timedelta(days=1, hours=i)
            )
            db.session.add(t)

        # Event 1: F-Code Hackathon (20/20 SLOTS - FULL / HET VE)
        ev1 = saved_events[1]
        for i, s_usr in enumerate(student_objs[0:20], start=1):
            status = "CHECKED_IN" if i <= 14 else "REGISTERED"
            check_time = datetime.utcnow() - timedelta(hours=i % 3 + 1) if status == "CHECKED_IN" else None
            t = Ticket(
                ticket_code=f"FU-2026-HACK{i:03d}",
                qr_url=f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=FU-2026-HACK{i:03d}",
                event=ev1,
                user=s_usr,
                status=status,
                checked_in_at=check_time,
                registered_at=datetime.utcnow() - timedelta(days=3, hours=i)
            )
            db.session.add(t)

        # Event 2: Career Talk FSOFT (120 slot, 28 da dang ky, 18 check-in)
        ev2 = saved_events[2]
        for i, s_usr in enumerate(student_objs[2:30], start=1):
            status = "CHECKED_IN" if i <= 18 else "REGISTERED"
            check_time = datetime.utcnow() - timedelta(hours=i % 5 + 1) if status == "CHECKED_IN" else None
            t = Ticket(
                ticket_code=f"FU-2026-FSOFT{i:03d}",
                qr_url=f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=FU-2026-FSOFT{i:03d}",
                event=ev2,
                user=s_usr,
                status=status,
                checked_in_at=check_time,
                registered_at=datetime.utcnow() - timedelta(days=2, hours=i)
            )
            db.session.add(t)

        # Event 3: Lễ Hội Văn Hóa CLB (250 slot, 28 da dang ky)
        ev3 = saved_events[3]
        t3_main = Ticket(
            ticket_code="FU-2026-CLB001",
            qr_url=f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=FU-2026-CLB001",
            event=ev3,
            user=student_main,
            status="REGISTERED",
            registered_at=datetime.utcnow() - timedelta(days=1)
        )
        db.session.add(t3_main)
        for i, s_usr in enumerate(student_objs[4:31], start=2):
            status = "CHECKED_IN" if i <= 15 else "REGISTERED"
            check_time = datetime.utcnow() - timedelta(hours=i % 4 + 1) if status == "CHECKED_IN" else None
            t = Ticket(
                ticket_code=f"FU-2026-CLB{i:03d}",
                qr_url=f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=FU-2026-CLB{i:03d}",
                event=ev3,
                user=s_usr,
                status=status,
                checked_in_at=check_time,
                registered_at=datetime.utcnow() - timedelta(days=1, hours=i)
            )
            db.session.add(t)

        # Event 4: Vovinam (80 slot, 18 da dang ky, 12 check-in)
        ev4 = saved_events[4]
        for i, s_usr in enumerate(student_objs[6:24], start=1):
            status = "CHECKED_IN" if i <= 12 else "REGISTERED"
            check_time = datetime.utcnow() - timedelta(hours=i % 3 + 1) if status == "CHECKED_IN" else None
            t = Ticket(
                ticket_code=f"FU-2026-VOV{i:03d}",
                qr_url=f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=FU-2026-VOV{i:03d}",
                event=ev4,
                user=s_usr,
                status=status,
                checked_in_at=check_time,
                registered_at=datetime.utcnow() - timedelta(days=3, hours=i)
            )
            db.session.add(t)

        # Event 5: Talkshow Ky Nang Mem (30/30 SLOTS - FULL / HET VE)
        ev5 = saved_events[5]
        for i, s_usr in enumerate(student_objs[0:30], start=1):
            status = "CHECKED_IN" if i <= 22 else "REGISTERED"
            check_time = datetime.utcnow() - timedelta(hours=i % 4 + 1) if status == "CHECKED_IN" else None
            t = Ticket(
                ticket_code=f"FU-2026-TALK{i:03d}",
                qr_url=f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=FU-2026-TALK{i:03d}",
                event=ev5,
                user=s_usr,
                status=status,
                checked_in_at=check_time,
                registered_at=datetime.utcnow() - timedelta(days=4, hours=i)
            )
            db.session.add(t)

        # Event 6: An Toan Thong Tin (15/15 SLOTS - FULL / HET VE)
        ev6 = saved_events[6]
        for i, s_usr in enumerate(student_objs[3:18], start=1):
            status = "CHECKED_IN" if i <= 11 else "REGISTERED"
            check_time = datetime.utcnow() - timedelta(hours=i % 2 + 1) if status == "CHECKED_IN" else None
            t = Ticket(
                ticket_code=f"FU-2026-SEC{i:03d}",
                qr_url=f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=FU-2026-SEC{i:03d}",
                event=ev6,
                user=s_usr,
                status=status,
                checked_in_at=check_time,
                registered_at=datetime.utcnow() - timedelta(days=2, hours=i)
            )
            db.session.add(t)

        # Event 7: Hien Mau Nhan Dao (150 slot, 26 da dang ky, 16 check-in)
        ev7 = saved_events[7]
        t7_main = Ticket(
            ticket_code="FU-2026-BLOOD001",
            qr_url=f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=FU-2026-BLOOD001",
            event=ev7,
            user=student_main,
            status="REGISTERED",
            registered_at=datetime.utcnow() - timedelta(days=1)
        )
        db.session.add(t7_main)
        for i, s_usr in enumerate(student_objs[5:30], start=2):
            status = "CHECKED_IN" if i <= 16 else "REGISTERED"
            check_time = datetime.utcnow() - timedelta(hours=i % 4 + 1) if status == "CHECKED_IN" else None
            t = Ticket(
                ticket_code=f"FU-2026-BLOOD{i:03d}",
                qr_url=f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=FU-2026-BLOOD{i:03d}",
                event=ev7,
                user=s_usr,
                status=status,
                checked_in_at=check_time,
                registered_at=datetime.utcnow() - timedelta(days=2, hours=i)
            )
            db.session.add(t)

    # 6. Reviews mau
    if Review.query.first() is None and len(saved_events) > 0:
        r1 = Review(
            event=saved_events[0],
            user=student_main,
            rating=5,
            comment="Workshop cực kỳ bổ ích! Diễn giả chia sẻ rất sâu về AI Agent và các công nghệ mới nhất. Rất mong trường tổ chức thêm nhiều buổi như này."
        )
        r2 = Review(
            event=saved_events[0],
            user=student_objs[1],
            rating=5,
            comment="Nội dung thực tế, được thực hành trực tiếp tại hội trường. Cảm ơn Ban tổ chức CLB F-Code!"
        )
        db.session.add_all([r1, r2])

    db.session.commit()
    print(f"Data seeded successfully! Total Events: {Event.query.count()}, Categories: {Category.query.count()}, Users: {User.query.count()}, Tickets: {Ticket.query.count()}")

def run():
    from app import app
    with app.app_context():
        seed_data_internal()

if __name__ == "__main__":
    run()
