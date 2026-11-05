# FPTU EventHub: Database Seeder
# Nap du lieu mau chuan dai hoc FPT (events.fptu.vn)

import os
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

    # 1. Nguoi dung mau (Sinh vien, Ban to chuc CLB, Admin CTSV)
    student = User.query.filter_by(email="dungtcde200433@fpt.edu.vn").first()
    if student is None:
        student = User(
            student_id="DE200433",
            full_name="Trương Công Dũng",
            email="dungtcde200433@fpt.edu.vn",
            phone="0905123456",
            avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80",
            role=role_student
        )
        student.set_password("pass123")
        db.session.add(student)

    student2 = User.query.filter_by(email="anhnvse190111@fpt.edu.vn").first()
    if student2 is None:
        student2 = User(
            student_id="SE190111",
            full_name="Nguyễn Việt Anh",
            email="anhnvse190111@fpt.edu.vn",
            phone="0912345678",
            avatar_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=300&q=80",
            role=role_student
        )
        student2.set_password("pass123")
        db.session.add(student2)

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

    db.session.flush()

    # 2. Danh muc su kien FPT (Categories)
    cats_data = [
        {"name": "Công Nghệ & AI", "slug": "tech-ai", "icon": "fa-microchip", "color": "#2563eb", "desc": "Các hội thảo chuyên sâu về Trí tuệ nhân tạo, Phần mềm, Cloud Computing"},
        {"name": "Học Thuật & Hackathon", "slug": "academic-hackathon", "icon": "fa-code", "color": "#f26f21", "desc": "Đấu trường lập trình, cuộc thi học thuật và nghiên cứu khoa học"},
        {"name": "Kỹ Năng & Hướng Nghiệp", "slug": "career-skills", "icon": "fa-briefcase", "color": "#059669", "desc": "Giao lưu doanh nghiệp, phỏng vấn tuyển dụng OJT và kỹ năng mềm"},
        {"name": "Văn Hóa & Câu Lạc Bộ", "slug": "culture-clubs", "icon": "fa-guitar", "color": "#d97706", "desc": "Lễ hội giao lưu, chương trình âm nhạc, kịch nghệ và hoạt động CLB"},
        {"name": "Thể Thao & Rèn Luyện", "slug": "sports-pdp", "icon": "fa-dumbbell", "color": "#7c3aed", "desc": "Giải thi đấu Vovinam, bóng đá, cầu lông và tính điểm rèn luyện PDP"},
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
            db.session.flush()
        cats_map[c["slug"]] = cat_obj

    # 3. Su kien thuc te dai hoc FPT voi anh luu cuc bo trong /static/images/events/
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
            "available_slots": 28,
            "pdp_points": 10,
            "speaker_name": "TS. Nguyễn Hoàng Nam",
            "speaker_title": "Senior AI Architect tại FPT Software & Cựu SV FPT",
            "speaker_avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=200&q=80",
            "banner_url": "/static/images/events/workshop_ai.jpg",
            "desc_md": """### Khám phá kỷ nguyên lập trình tương lai với AI Agent
Workshop dành riêng cho sinh viên ngành CNTT ĐH FPT, mang đến cái nhìn sâu sắc về cách thức các mô hình ngôn ngữ lớn (LLM) và AI Agentic Assistants cách mạng hóa quy trình viết code:
- **Nội dung 1:** Tổng quan về kiến trúc Multi-Agent & Code Automation.
- **Nội dung 2:** Thực hành tích hợp Google Antigravity SDK vào ứng dụng Web.
- **Nội dung 3:** Hỏi đáp trực tiếp cùng các chuyên gia hàng đầu từ FPT Software.

*Lưu ý: Sinh viên tham dự đầy đủ sẽ được cấp chứng nhận và tích lũy **10 điểm rèn luyện PDP**!*"""
        },
        {
            "title": "F-Code Hackathon 2026: Xây Dựng Ứng Dụng Thông Minh",
            "slug": "f-code-hackathon-2026",
            "category": cats_map["academic-hackathon"],
            "venue": "Phòng Lab AI & Robotics (Tầng 4, Tòa nhà Gamma)",
            "start_time": now + timedelta(days=5, hours=8),
            "end_time": now + timedelta(days=6, hours=18),
            "total_capacity": 50,
            "available_slots": 6,
            "pdp_points": 15,
            "speaker_name": "Ban Chuyên Môn CLB F-Code",
            "speaker_title": "Đơn vị tổ chức cuộc thi học thuật ĐH FPT",
            "speaker_avatar": "/static/images/fpt_logo.jpg",
            "banner_url": "/static/images/events/hackathon.jpg",
            "desc_md": """### Cuộc thi lập trình 24 giờ liên tục tại FPT University
Thử thách bản thân trong môi trường áp lực cao để phát triển giải pháp công nghệ phục vụ cộng đồng:
- Tổng giá trị giải thưởng lên đến **50.000.000 VNĐ**.
- Được hỗ trợ Mentor 1-1 từ các công ty công nghệ đối tác.
- Tích lũy ngay **15 điểm rèn luyện PDP** cho các thành viên hoàn thành sản phẩm."""
        },
        {
            "title": "FPT Software Career Talk: Chinh Phục Kỳ Thực Tập OJT 2026",
            "slug": "fsoft-career-talk-ojt",
            "category": cats_map["career-skills"],
            "venue": "Hội trường Beta (Khu Giảng Đường B - FPTU)",
            "start_time": now + timedelta(days=3, hours=14),
            "end_time": now + timedelta(days=3, hours=17),
            "total_capacity": 150,
            "available_slots": 45,
            "pdp_points": 10,
            "speaker_name": "Chị Lê Thu Hà",
            "speaker_title": "Trưởng phòng Tuyển dụng & Đào tạo FPT Software",
            "speaker_avatar": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80",
            "banner_url": "/static/images/events/fsoft_career.jpg",
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
            "total_capacity": 300,
            "available_slots": 120,
            "pdp_points": 5,
            "speaker_name": "Ban Chấp Hành Đoàn Trường FPTU",
            "speaker_title": "Phòng CTSV phối hợp cùng 30 CLB FPTU",
            "speaker_avatar": "/static/images/fpt_logo.jpg",
            "banner_url": "/static/images/events/club_festival.jpg",
            "desc_md": """### Đêm nhạc hội bùng nổ sắc màu sinh viên FPT
- Gian hàng ẩm thực và trải nghiệm từ hơn 30 câu lạc bộ học thuật, nghệ thuật, thể thao.
- Sân khấu biểu diễn ca nhạc, nhảy hiện đại và DJ sôi động.
- Điểm danh tích lũy **5 điểm rèn luyện PDP**."""
        },
        {
            "title": "Giải Vô Địch Vovinam & Võ Thuật Học Đường FPTU",
            "slug": "vovinam-championship-fptu",
            "category": cats_map["sports-pdp"],
            "venue": "Nhà Thi Đấu Thể Thao Đa Năng FPT University",
            "start_time": now + timedelta(days=10, hours=7, minutes=30),
            "end_time": now + timedelta(days=10, hours=16),
            "total_capacity": 80,
            "available_slots": 12,
            "pdp_points": 10,
            "speaker_name": "Võ Sư Nguyễn Thanh Tùng",
            "speaker_title": "Trưởng Bộ môn Giáo dục Thể chất Vovinam FPTU",
            "speaker_avatar": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=200&q=80",
            "banner_url": "/static/images/events/vovinam.jpg",
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
            "total_capacity": 120,
            "available_slots": 0, # HET VE (Sold Out de demo nut vo hieu hoa)
            "pdp_points": 10,
            "speaker_name": "Thầy Võ Minh Trí",
            "speaker_title": "Giảng viên Xuất Sắc Bộ môn Kỹ năng Mềm FPTU",
            "speaker_avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=200&q=80",
            "banner_url": "/static/images/events/talkshow_skills.jpg",
            "desc_md": """### Vượt qua nỗi sợ đứng trước đám đông và lãnh đạo nhóm hiệu quả
Sự kiện đã nhận được sự quan tâm kỷ lục và **chính thức cháy vé (Sold Out)** trong vòng 2 giờ mở cổng:
- Nghệ thuật thiết kế Storytelling trong thuyết trình đồ án tốt nghiệp.
- Giải quyết mâu thuẫn nội bộ và phân chia deadline công bằng khi làm Capstone."""
        },
        {
            "title": "Hội Thảo An Toàn Thông Tin & Phòng Chống Tấn Công Mạng",
            "slug": "workshop-cyber-security-fpt",
            "category": cats_map["tech-ai"],
            "venue": "Phòng Hội Thảo 302 (Tòa Nhà Gamma - FPTU)",
            "start_time": now + timedelta(days=4, hours=13, minutes=30),
            "end_time": now + timedelta(days=4, hours=16),
            "total_capacity": 60,
            "available_slots": 15,
            "pdp_points": 10,
            "speaker_name": "Anh Phạm Quốc Bảo",
            "speaker_title": "Chuyên Gia Bảo Mật Cấp Cao FPT IS",
            "speaker_avatar": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=200&q=80",
            "banner_url": "/static/images/events/cyber_security.jpg",
            "desc_md": """### Phân tích các mối đe dọa an ninh mạng trong kỷ nguyên số
Thực hành trực tiếp tấn công và phòng thủ web (CTF mini challenge):
- Kỹ thuật phòng chống SQL Injection, Cross-Site Scripting (XSS).
- Quản lý khóa bảo mật API và cấu hình mạng an toàn cho doanh nghiệp."""
        },
        {
            "title": "Ngày Hội Hiến Máu Nhân Đạo: Giọt Hồng FPTU 2026",
            "slug": "blood-donation-fptu-2026",
            "category": cats_map["culture-clubs"],
            "venue": "Sảnh Tòa Nhà Alpha - FPTU",
            "start_time": now + timedelta(days=8, hours=7),
            "end_time": now + timedelta(days=8, hours=11),
            "total_capacity": 200,
            "available_slots": 88,
            "pdp_points": 15,
            "speaker_name": "Đội Tình Nguyện Sinh Viên FPTU",
            "speaker_title": "Phối hợp cùng Hội Chữ Thập Đỏ & Bệnh viện",
            "speaker_avatar": "/static/images/fpt_logo.jpg",
            "banner_url": "/static/images/events/blood_donation.jpg",
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
                pdp_points=ed["pdp_points"],
                description_md=ed["desc_md"],
                description_html=render_safe_markdown(ed["desc_md"]),
                category=ed["category"],
                organizer=organizer
            )
            db.session.add(ev)
        else:
            ev.title = ed["title"]
            ev.banner_url = ed["banner_url"]
            ev.venue = ed["venue"]
            ev.total_capacity = ed["total_capacity"]
            ev.available_slots = ed["available_slots"]
            ev.pdp_points = ed["pdp_points"]
            ev.speaker_name = ed["speaker_name"]
            ev.speaker_title = ed["speaker_title"]
            ev.speaker_avatar = ed["speaker_avatar"]
            ev.description_md = ed["desc_md"]
            ev.description_html = render_safe_markdown(ed["desc_md"])
        saved_events.append(ev)

    db.session.flush()

    # 4. Tao truoc 2 ve mau cho sinh vien Truong Cong Dung de demo
    # Ve 1: Workshop AI -> Da Check-in (Co ngay 10 PDP va Giay chung nhan E-Certificate de demo)
    # Ve 2: Hackathon -> Da dang ky (De demo huy ve hoac check-in bang QR scanner)
    if Ticket.query.first() is None and len(saved_events) >= 2:
        ticket1 = Ticket(
            ticket_code=Ticket.generate_ticket_code(),
            qr_url="https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=FU-2026-AIWORKSHOP-DE200433",
            event=saved_events[0], # Workshop AI
            user=student,
            status="CHECKED_IN",
            checked_in_at=datetime.utcnow() - timedelta(hours=2)
        )
        ticket2 = Ticket(
            ticket_code=Ticket.generate_ticket_code(),
            qr_url="https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=FU-2026-HACKATHON-DE200433",
            event=saved_events[1], # Hackathon
            user=student,
            status="REGISTERED"
        )
        db.session.add_all([ticket1, ticket2])

    # 5. Nap danh gia mau (Reviews)
    if Review.query.first() is None and len(saved_events) > 0:
        r1 = Review(
            event=saved_events[0],
            user=student,
            rating=5,
            comment="Workshop cực kỳ bổ ích! Diễn giả chia sẻ rất sâu về AI Agent và các công nghệ mới nhất. Rất mong trường tổ chức thêm nhiều buổi như này."
        )
        r2 = Review(
            event=saved_events[0],
            user=student2,
            rating=5,
            comment="Nội dung thực tế, được thực hành trực tiếp tại hội trường. Cảm ơn Ban tổ chức CLB F-Code!"
        )
        db.session.add_all([r1, r2])

    db.session.commit()
    print(f"Data seeded successfully! Total Events: {Event.query.count()}, Categories: {Category.query.count()}, Users: {User.query.count()}, Reviews: {Review.query.count()}")

def run():
    from app import app
    with app.app_context():
        seed_data_internal()

if __name__ == "__main__":
    run()
