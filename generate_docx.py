# -*- coding: utf-8 -*-
"""
Script to generate the comprehensive 45-50 minute 5-person Presentation Script & Q&A Defense Guide
in Microsoft Word (.docx) format for FPTU EventHub.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_presentation_document(output_path):
    doc = Document()

    # Set page margins (1 inch all sides)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)

    # Style colors
    PRIMARY = RGBColor(242, 111, 33)   # FPT Orange
    NAVY = RGBColor(0, 75, 145)        # FPT Navy
    TEXT_MAIN = RGBColor(30, 41, 59)   # Slate 800
    MUTED = RGBColor(100, 116, 139)    # Slate 500
    SUCCESS = RGBColor(22, 163, 74)    # Green 600

    # Base Normal Style
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Segoe UI'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = TEXT_MAIN
    style_normal.paragraph_format.line_spacing = 1.25
    style_normal.paragraph_format.space_after = Pt(4)

    # Header Title Banner
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = title_p.add_run("TRƯỜNG ĐẠI HỌC FPT — BẢO VỆ ĐỒ ÁN MÔN HỌC CHUYÊN NGÀNH CNTT\n")
    run_sub.font.size = Pt(11)
    run_sub.font.bold = True
    run_sub.font.color.rgb = NAVY

    run_title = title_p.add_run("KỊCH BẢN THUYẾT TRÌNH & CẨM NANG VẤN ĐÁP BẢO VỆ ĐỒ ÁN\n(THỜI LƯỢNG: 45 – 50 PHÚT — PHÂN CHIA 5 THÀNH VIÊN)\n")
    run_title.font.size = Pt(18)
    run_title.font.bold = True
    run_title.font.color.rgb = PRIMARY

    run_proj = title_p.add_run("DỰ ÁN: FPTU EVENTHUB — HỆ THỐNG QUẢN LÝ & ĐĂNG KÝ SỰ KIỆN NỘI BỘ FPT UNIVERSITY")
    run_proj.font.size = Pt(13)
    run_proj.font.bold = True
    run_proj.font.color.rgb = NAVY

    # Meta Info Box Table
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False

    meta_data = [
        ("Cổng web trực tuyến (Vercel):", "https://fptu-event-hub.vercel.app/"),
        ("Kho lưu trữ mã nguồn (GitHub):", "https://github.com/CongDung0506/FPTU-EventHub"),
        ("Công nghệ cốt lõi áp dụng:", "Python 3.14, Flask, HTML5/CSS (BEM), WebRTC Camera QR, Microsoft SQL Server & SQLite"),
        ("Phân quyền hệ thống (RBAC):", "Sinh viên (Student) & Phòng Công Tác Sinh Viên (Admin/CTSV)"),
        ("Đối tượng tham gia thuyết trình:", "Nhóm 5 thành viên (Mỗi thành viên phụ trách 8 - 10 phút)")
    ]

    for idx, (label, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width = Inches(2.5)
        cell_val.width = Inches(4.5)

        set_cell_background(cell_lbl, "F8FAFC")
        set_cell_background(cell_val, "FFFFFF")
        set_cell_margins(cell_lbl, 80, 80, 120, 120)
        set_cell_margins(cell_val, 80, 80, 120, 120)

        p0 = cell_lbl.paragraphs[0]
        p0.add_run(label).font.bold = True
        p0.runs[0].font.size = Pt(10)
        p0.runs[0].font.color.rgb = NAVY

        p1 = cell_val.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.size = Pt(10)
        if "http" in val:
            r1.font.color.rgb = PRIMARY
            r1.font.underline = True

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 1. Timeline Table
    h1 = doc.add_paragraph()
    r_h1 = h1.add_run("I. PHÂN CHIA THỜI LƯỢNG TỔNG THỂ (45 – 50 PHÚT)")
    r_h1.font.size = Pt(14)
    r_h1.font.bold = True
    r_h1.font.color.rgb = NAVY
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)

    desc_p = doc.add_paragraph()
    desc_p.add_run("Buổi bảo vệ đồ án được thiết kế chuẩn khoa học với 5 phần trình bày nối tiếp nhau. Mỗi thành viên có đủ đất diễn (từ 8 đến 10 phút) để hội đồng chấm điểm công bằng và đánh giá năng lực cá nhân một cách khách quan nhất:")

    time_table = doc.add_table(rows=7, cols=4)
    time_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Thời Lượng", "Thành Viên Phụ Trách", "Nội Dung Thuyết Trình Chính", "Phần Mềm & Slide Cần Mở"]

    for col_idx, h_text in enumerate(headers):
        cell = time_table.rows[0].cells[col_idx]
        set_cell_background(cell, "004B91")
        set_cell_margins(cell, 100, 100, 120, 120)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(10)

    time_rows = [
        ("Phút 00:00 – 09:30\n(9.5 phút)", "Thành Viên 1 (Nhóm Trưởng)\nTrương Công Dũng", "Đặt vấn đề, Bối cảnh FPTU, Pain Points cổng events.fptu.vn, Mục tiêu & Bảng so sánh đột phá", "Slide 1 &rarr; 5\nTrang chủ EventHub"),
        ("Phút 09:30 – 18:30\n(9.0 phút)", "Thành Viên 2\nKỹ Thuật & Bảo Mật", "Tech Stack (Python/Flask, Bleach XSS, WebRTC Camera QR, Bcrypt/PBKDF2, CSS Scoped BEM, Zero-SSO)", "Slide 6 &rarr; 10\nVS Code (Code bảo mật)"),
        ("Phút 18:30 – 27:00\n(8.5 phút)", "Thành Viên 3\nKiến Trúc & Database", "Mô hình MVC, Sơ đồ quan hệ ERD, Cơ chế Dual-Database (SQL Server Local + SQLite Serverless trên Vercel)", "Slide 11 &rarr; 16\nDiagram ERD, DB Browser"),
        ("Phút 27:00 – 36:30\n(9.5 phút)", "Thành Viên 4\nLive Demo Sinh Viên", "Usecase Sinh viên, Live Search tức thì, Đặt vé giữ chỗ real-time, Vé QR, Hủy vé, Google Calendar, Nhận E-Cert", "Slide 17 &rarr; 22\nTrình duyệt Tab 1 (Sinh viên)"),
        ("Phút 36:30 – 45:30\n(9.0 phút)", "Thành Viên 5\nLive Demo CTSV & Kết Luận", "Usecase CTSV, Bảng điều hành sự kiện, Quét QR Check-in bằng Camera laptop/điện thoại, Xuất Excel/CSV, Tổng kết", "Slide 23 &rarr; 28\nTrình duyệt Tab 2 (Cán bộ CTSV)"),
        ("Phút 45:30 – 50:00+\n(5 - 10 phút)", "Cả 5 Thành Viên\nPhần Q&A Vấn Đáp", "Giảng viên đặt 2–3 câu hỏi phản biện chuyên sâu cho từng thành viên để chấm điểm kỹ năng và đồ án", "Tất cả slide, mã nguồn sẵn sàng")
    ]

    for row_idx, r_data in enumerate(time_rows, start=1):
        row = time_table.rows[row_idx]
        bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(r_data):
            cell = row.cells[col_idx]
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9.5)
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = PRIMARY
            elif col_idx == 1:
                r.font.bold = True

    # 2. Comparison Table with events.fptu.vn
    h2 = doc.add_paragraph()
    r_h2 = h2.add_run("II. BẢNG SO SÁNH ĐỘT PHÁ VỚI CỔNG SỰ KIỆN HIỆN TẠI (events.fptu.vn)")
    r_h2.font.size = Pt(14)
    r_h2.font.bold = True
    r_h2.font.color.rgb = NAVY
    h2.paragraph_format.space_before = Pt(16)
    h2.paragraph_format.space_after = Pt(6)

    comp_table = doc.add_table(rows=9, cols=3)
    comp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    comp_headers = ["Tiêu Chí Nghiệp Vụ", "Cổng Cũ Của Trường (events.fptu.vn)", "FPTU EventHub (Web Của Nhóm)"]

    for col_idx, h_text in enumerate(comp_headers):
        cell = comp_table.rows[0].cells[col_idx]
        set_cell_background(cell, "F26F21" if col_idx == 2 else "004B91")
        set_cell_margins(cell, 100, 100, 120, 120)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(10)

    comp_rows = [
        ("Mô hình hoạt động", "Trang tin tức tĩnh / blog thông báo sự kiện, không tương tác đặt chỗ nội bộ.", "Nền tảng quản trị và vận hành sự kiện trực tuyến khép kín (Full-lifecycle event portal)."),
        ("Cơ chế đặt vé (Ticket Booking)", "Chuyển hướng ra ngoài điền Google Form thủ công, không có mã vé định danh.", "Sinh vé điện tử tức thì (mã dạng FU-2026-XXXXX), lưu vào Ví vé cá nhân có mã QR riêng."),
        ("Quy trình Check-in Hội trường", "In danh sách giấy hoặc dò file Excel thủ công, dễ ùn tắc kéo dài tại cửa phòng.", "Tích hợp Bàn Check-in bằng Camera điện thoại/laptop (WebRTC), quét QR xong trong 1 giây."),
        ("Chứng nhận tham gia (E-Cert)", "Chờ cán bộ thiết kế gửi email sau nhiều tuần (hoặc không có giấy chứng nhận).", "Hệ thống tự động phát hành Giấy Chứng Nhận Điện Tử có mã số xác thực ngay khi check-in."),
        ("Kiểm soát sức chứa (Capacity)", "Không đếm số ghế trống real-time, sinh viên đăng ký quá tải gây vỡ trận hội trường.", "Thanh sức chứa trực quan; tự động khóa nút và gắn mác ĐÃ HẾT VÉ (SOLD OUT) khi kín chỗ."),
        ("Hủy vé & Nhượng chỗ", "Sinh viên bận không có cách nào hủy vé, dẫn đến đặt chỗ ảo nhưng hội trường vắng ngắt.", "Sinh viên hủy vé 1-click, hệ thống tự động hoàn lại slot ghế trống cho bạn khác."),
        ("Phân quyền người dùng (RBAC)", "Chung một giao diện người xem, không có trang nghiệp vụ cho cán bộ CTSV.", "Tách biệt tuyệt đối 2 luồng: Sinh viên (đặt vé, QR) & Phòng CTSV (điều hành, điểm danh, xuất CSV)."),
        ("Công nghệ & Giao diện", "Tìm kiếm phải tải lại trang (reload); không có chế độ Dark Mode bảo vệ mắt.", "Live Search tức thì không cần reload trang; hỗ trợ Dark/Light Theme 1-click; đồng hồ đếm ngược.")
    ]

    for row_idx, r_data in enumerate(comp_rows, start=1):
        row = comp_table.rows[row_idx]
        bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(r_data):
            cell = row.cells[col_idx]
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9.5)
            if col_idx == 0:
                r.font.bold = True
            elif col_idx == 2:
                r.font.color.rgb = RGBColor(15, 23, 42)

    # 3. Detailed Member Scripts
    members = [
        {
            "num": "THÀNH VIÊN 1",
            "name": "TRƯƠNG CÔNG DŨNG — NHÓM TRƯỞNG & QUẢN LÝ DỰ ÁN",
            "time": "00:00 – 09:30 (Thời lượng: 9.5 phút)",
            "slides": "Slide 1 đến Slide 5",
            "key_points": [
                "Lời chào hội đồng, giới thiệu 5 thành viên và đề tài đồ án FPTU EventHub.",
                "Bối cảnh thực tế tại FPT University: Hàng tuần có hàng chục sự kiện, workshop, giải đấu của 30+ CLB.",
                "Thực trạng và bất cập của cổng cũ events.fptu.vn cùng phương pháp Google Form truyền thống.",
                "Phân tích 5 đột phá của FPTU EventHub: Vé QR điện tử, Check-in Camera, E-Certificate, Quản lý cháy vé, Phân quyền CTSV.",
                "Chuyển giao phần trình bày kỹ thuật cho Thành viên 2."
            ],
            "script": (
                "\"Kính thưa quý thầy cô trong Hội đồng chấm đồ án tốt nghiệp cùng toàn thể các bạn sinh viên!\n\n"
                "Em tên là Trương Công Dũng, nhóm trưởng của dự án. Đại diện cho nhóm 5 thành viên của chúng em hôm nay, "
                "em xin trân trọng giới thiệu đề tài: 'FPTU EventHub — Cổng Quản Lý & Đăng Ký Sự Kiện Sinh Viên Đại Học FPT'.\n\n"
                "Như thầy cô đã biết, Đại học FPT là một trong những môi trường đại học năng động nhất Việt Nam với hơn 30 câu lạc bộ học thuật, "
                "nghệ thuật và thể thao. Mỗi tuần, tại các Hội trường Alpha, Beta hay phòng Lab Gamma đều diễn ra hàng loạt Workshop công nghệ, "
                "Hackathon lập trình và giải đấu Vovinam. Tuy nhiên, khi nhìn vào cổng thông tin hiện tại của trường là events.fptu.vn, "
                "chúng em nhận thấy một bài toán rất lớn: Cổng cũ thực chất chỉ là một bảng tin tĩnh đăng bài thông báo. Khi sinh viên muốn đăng ký "
                "giữ chỗ, ban tổ chức vẫn phải dẫn link ra ngoài Google Form hoặc biểu mẫu trung gian.\n\n"
                "Cách làm này để lại 4 'nỗi đau' cực kỳ nhức nhối:\n"
                "1. Hội trường Alpha chỉ có sức chứa 100 ghế, nhưng Google Form không thể giới hạn tự động theo thời gian thực, dẫn đến nhận 200 đơn đăng ký gây vỡ trận hội trường.\n"
                "2. Đến giờ diễn ra, hàng trăm sinh viên phải đứng chen chúc ở cửa để cán bộ cầm giấy hoặc dò từng dòng Excel để điểm danh rất thủ công và chậm chạp.\n"
                "3. Sinh viên bận việc đột xuất không có cách nào hủy vé để nhường lại cho bạn khác, dẫn đến tình trạng trên danh sách thì đầy nhưng ghế ngồi lại trống.\n"
                "4. Giấy chứng nhận tham gia thường phải chờ thiết kế thủ công gửi email sau nhiều tuần, gây nản lòng cho sinh viên.\n\n"
                "Chính vì vậy, nhóm chúng em đã xây dựng FPTU EventHub nhằm số hóa 100% quy trình: Sinh viên đăng nhập bằng email trường (@fpt.edu.vn) &rarr; "
                "Giữ chỗ tức thì nhận vé điện tử kèm mã QR riêng &rarr; Cán bộ CTSV dùng Camera quét QR điểm danh chỉ trong 1 giây &rarr; Nhận ngay Giấy chứng nhận E-Certificate chuẩn học thuật.\n\n"
                "Sau đây, em xin kính mời Thành viên 2 tiếp tục trình bày về nền tảng công nghệ và các giải pháp bảo mật mà nhóm đã triển khai!\""
            ),
            "qa": [
                ("Tại sao nhóm không dùng luôn Google Forms hay Microsoft Forms cho nhanh mà phải lập trình riêng một hệ thống web?",
                 "Dạ thưa thầy/cô, Google Forms có 3 giới hạn cốt tử: Thứ nhất, Google Form không kiểm soát sức chứa ghế (Capacity) theo cơ chế giao dịch Transaction thời gian thực, dễ gây vỡ trận số lượng. Thứ hai, Google Forms không tự sinh được vé điện tử có mã QR định danh cá nhân để quét tại cửa. Thứ ba, Google Forms không có kiến trúc phân quyền (RBAC) để phục vụ công tác điều hành của Cán bộ CTSV và tự động xuất file báo cáo điểm danh ạ."),
                ("Đối tượng người dùng chính của hệ thống là ai và họ được phân quyền như thế nào?",
                 "Dạ hệ thống được thiết kế theo chuẩn phân quyền Role-Based Access Control (RBAC) với 2 nhóm người dùng chuyên biệt: 1. Sinh viên (Student): Khám phá sự kiện, đặt vé giữ chỗ, sở hữu Ví vé QR cá nhân, hủy vé và in Giấy chứng nhận. 2. Phòng Công Tác Sinh Viên (Admin/CTSV): Giám sát dữ liệu toàn trường, duyệt và đăng sự kiện, mở Bàn Check-in quét mã QR bằng camera và xuất báo cáo điểm danh ra file Excel/CSV ạ."),
                ("Hệ thống giải quyết vấn đề 'đặt chỗ ảo' (ghế đăng ký kín nhưng người không đến) như thế nào?",
                 "Dạ chúng em giải quyết bằng 2 cơ chế: 1. Tính năng 'Hủy vé 1-click' trong trang Vé Của Tôi: khi sinh viên biết mình bận, các bạn bấm hủy thì slot ghế được hoàn trả ngay lập tức cho bạn khác trên trang chủ. 2. Mỗi sinh viên chỉ được đặt 1 vé duy nhất cho mỗi sự kiện nhờ cơ chế kiểm tra ràng buộc ở cả Client lẫn Server, chấm dứt hoàn toàn tình trạng 1 người ôm nhiều chỗ ạ.")
            ]
        },
        {
            "num": "THÀNH VIÊN 2",
            "name": "KỸ THUẬT, CÔNG NGHỆ & GIẢI PHÁP AN NINH BẢO MẬT",
            "time": "09:30 – 18:30 (Thời lượng: 9.0 phút)",
            "slides": "Slide 6 đến Slide 10",
            "key_points": [
                "Công nghệ Backend: Python 3.14 + Flask Framework siêu nhẹ, module hóa cao.",
                "Xác thực Zero-Registration SSO qua email trường cấp (@fpt.edu.vn / @fe.edu.vn).",
                "Bảo mật mật khẩu bằng thuật toán PBKDF2/SHA-256 kết hợp Salt của Werkzeug Security.",
                "Giải pháp phòng chống Stored XSS bằng thư viện Bleach khi người dùng viết mô tả Markdown.",
                "Công nghệ quét Camera QR thời gian thực thông qua WebRTC MediaDevices API (html5-qrcode).",
                "Frontend Design System: CSS Scoped BEM, Dark Mode / Light Mode lưu tự động vào localStorage."
            ],
            "script": (
                "\"Kính thưa quý thầy cô, em xin phép tiếp nối phần trình bày của nhóm trưởng về bức tranh công nghệ và kiến trúc an ninh của FPTU EventHub.\n\n"
                "Để xây dựng một hệ thống có tốc độ phản hồi nhanh, tải nhẹ và dễ triển khai lên môi trường Cloud, nhóm đã lựa chọn Backend là Python 3.14 "
                "kết hợp cùng Micro-framework Flask. Về mặt kiến trúc bảo mật, nhóm tập trung xử lý 4 trụ cột quan trọng nhất:\n\n"
                "Trụ cột thứ nhất: Cơ chế Campus Zero-Registration SSO. Chúng em giải quyết rào cản lớn nhất của các ứng dụng trường học là sinh viên rất ngại tạo tài khoản mới. "
                "Tại FPTU EventHub, hệ thống kiểm thực tên miền email: chỉ chấp nhận @fpt.edu.vn hoặc @fe.edu.vn. Người ngoài trường dùng Gmail hay Yahoo đều bị chặn ngay từ cổng vào. "
                "Khi sinh viên trường nhập email FPT, hệ thống tự động bóc tách MSSV (ví dụ: dungtcde200433 -> DE200433) và kích hoạt tài khoản ngay tức thì.\n\n"
                "Trụ cột thứ hai: Bảo vệ mật khẩu sinh viên. Mật khẩu tuyệt đối không bao giờ được lưu thô, mà được băm bằng thuật toán tiêu chuẩn công nghiệp PBKDF2 "
                "kết hợp Salt ngẫu nhiên thông qua werkzeug.security. Ngay cả khi hacker có được toàn bộ file cơ sở dữ liệu thì cũng không thể đảo ngược để lấy mật khẩu gốc.\n\n"
                "Trụ cột thứ ba: Phòng chống tấn công Stored XSS bằng Bleach. Trang web cho phép Cán bộ nhập mô tả sự kiện bằng ngôn ngữ Markdown rất đẹp. "
                "Tuy nhiên, nếu dùng thẳng bộ lọc Jinja2 |safe thì kẻ xấu có thể chèn các thẻ độc hại như <script> cướp Session Cookie. "
                "Chúng em đã sử dụng thư viện Bleach làm màng lọc kiểm duyệt: chỉ cho phép các thẻ định dạng an toàn như in đậm, tiêu đề, danh sách, và loại bỏ 100% mã độc JavaScript.\n\n"
                "Trụ cột thứ tư: Công nghệ quét mã QR trên nền WebRTC. Chúng em không bắt buộc sinh viên hay cán bộ phải cài đặt bất kỳ App di động nào từ App Store hay CH Play. "
                "Thông qua thư viện html5-qrcode, hệ thống xin quyền truy cập Camera trực tiếp trên trình duyệt web, phân tích luồng hình ảnh ở tần số 10 khung hình/giây để giải mã "
                "chuỗi vé FU-2026 và gửi AJAX ngầm về máy chủ để check-in tức thì.\n\n"
                "Tiếp theo đây, xin kính mời Thành viên 3 trình bày chi tiết về Sơ đồ dữ liệu ERD và giải pháp chuyển đổi cơ sở dữ liệu Dual-Database!\""
            ),
            "qa": [
                ("Tại sao các bạn lại sử dụng thư viện Bleach trong việc xử lý mô tả sự kiện?",
                 "Dạ thưa cô, tính năng tạo sự kiện cho phép định dạng Markdown để bài viết phong phú. Nếu render trực tiếp mã HTML mà không kiểm duyệt, kẻ tấn công có thể chèn mã độc JavaScript như <script src='evil.js'> hoặc <img src=x onerror='stealData()'> để đánh cắp Cookie phiên đăng nhập của người khác (lỗ hổng Stored XSS). Thư viện Bleach đóng vai trò bộ lọc Whitelist nghiêm ngặt, chỉ cho phép các thẻ văn bản an toàn đi qua và tước bỏ toàn bộ mã độc hại ạ."),
                ("Làm thế nào Camera trên trình duyệt quét được mã QR mà không cần cài thêm ứng dụng App di động?",
                 "Dạ chúng em khai thác WebRTC MediaDevices API chuẩn W3C trên các trình duyệt hiện đại (Chrome, Safari, Edge). JavaScript sẽ yêu cầu quyền camera (navigator.mediaDevices.getUserMedia) với chế độ ưu tiên camera sau (facingMode: 'environment'). Thư viện html5-qrcode quét luồng video thời gian thực, đọc chuỗi mã vé và gửi bất đồng bộ (Fetch API) về endpoint Flask /api/check-in/scan để xác thực mà không hề gây gián đoạn hay tải lại trang web ạ."),
                ("Nếu sinh viên đăng nhập trên máy tính công cộng ở trường, hệ thống có giải pháp gì bảo vệ phiên đăng nhập?",
                 "Dạ hệ thống sử dụng Flask-Login quản lý Session an toàn trên Cookie với các cờ bảo vệ: HttpOnly để ngăn JavaScript truy cập cướp Cookie, và SameSite='Lax' để chống tấn công Cross-Site Request Forgery (CSRF). Đồng thời nút Đăng Xuất An Toàn xóa sạch Session trên máy tính ngay khi bấm ạ.")
            ]
        },
        {
            "num": "THÀNH VIÊN 3",
            "name": "KIẾN TRÚC DỰ ÁN (MVC) & THIẾT KẾ CƠ SỞ DỮ LIỆU (ERD)",
            "time": "18:30 – 27:00 (Thời lượng: 8.5 phút)",
            "slides": "Slide 11 đến Slide 16",
            "key_points": [
                "Mô hình MVC (Model - View - Controller): Tổ chức code rõ ràng, phân tách trách nhiệm.",
                "Sơ đồ quan hệ thực thể ERD với 6 bảng cốt lõi: Role, User, Category, Event, Ticket, Review.",
                "Ràng buộc toàn vẹn dữ liệu: Mối quan hệ 1-N giữa Event và Ticket (cascade delete-orphan).",
                "Thuật toán bảo vệ Capacity và ngăn chặn Race Condition khi đặt vé.",
                "Điểm sáng kiến trúc: Cơ chế Dual-Database thích ứng thông minh giữa SQL Server và SQLite Serverless."
            ],
            "script": (
                "\"Kính thưa quý thầy cô, em xin đại diện nhóm trình bày về cấu trúc mã nguồn MVC và thiết kế Cơ sở dữ liệu của FPTU EventHub.\n\n"
                "Dự án được tổ chức chặt chẽ theo chuẩn kiến trúc MVC:\n"
                "- Tầng Model (models.py): Định nghĩa 6 thực thể dữ liệu kế thừa từ SQLAlchemy ORM.\n"
                "- Tầng View (templates/ và static/): Chứa các khuôn mẫu Jinja2 HTML và mã giao diện, CSS Scoped.\n"
                "- Tầng Controller (app.py): Đảm nhận nhiệm vụ điều hướng, áp dụng các Decorator bảo vệ quyền truy cập (@login_required, @admin_required) và xử lý logic nghiệp vụ.\n\n"
                "Về Sơ đồ thực thể CSDL (ERD), chúng em thiết kế 6 bảng có mối quan hệ chặt chẽ:\n"
                "1. Bảng Role và User: Quan hệ 1 - N. Phân chia rõ ràng vai trò Student (Sinh viên) và Admin (Phòng CTSV).\n"
                "2. Bảng Category và Event: Quan hệ 1 - N. Phân loại sự kiện theo 5 nhóm: Công Nghệ & AI, Học Thuật & Hackathon, Kỹ Năng & Hướng Nghiệp, Văn Hóa & CLB, Thể Thao & Phong Trào.\n"
                "3. Bảng Event và Ticket: Quan hệ 1 - N với ràng buộc cascade='all, delete-orphan'. Mỗi sự kiện có nhiều vé, và khi một sự kiện bị xóa thì các vé con được dọn dẹp sạch sẽ để không sinh ra dữ liệu rác.\n"
                "4. Bảng User và Ticket: Mỗi sinh viên sở hữu danh sách vé riêng, có trạng thái rõ ràng: REGISTERED (Đã giữ chỗ), CHECKED_IN (Đã điểm danh), hoặc CANCELLED (Đã hủy).\n"
                "5. Bảng Review: Cho phép sinh viên sau khi tham dự đánh giá số sao (1 đến 5 sao) và để lại nhận xét, giúp hệ thống tính điểm trung bình (Average Rating).\n\n"
                "Đặc biệt, một điểm sáng kỹ thuật trong đồ án của nhóm là Cơ Chế Dual-Database Switch:\n"
                "- Khi chạy cục bộ trên máy tính của sinh viên hoặc máy phòng thực hành của trường: Mã nguồn tự động kết nối Microsoft SQL Server qua ODBC Driver theo đúng chuẩn môn học CSDL.\n"
                "- Khi triển khai lên nền tảng đám mây Vercel Serverless: Code tự động nhận diện biến môi trường để chuyển sang SQLite Serverless tại thư mục /tmp. Nhờ giải pháp này, hệ thống vừa đáp ứng 100% chuẩn học thuật của trường, vừa có thể chạy mượt mà trên Internet toàn cầu mà không tốn chi phí thuê server đắt đỏ.\n\n"
                "Sau đây, xin mời Thành viên 4 thực hiện phần Live Demo trực tiếp luồng trải nghiệm của Sinh viên!\""
            ),
            "qa": [
                ("Trong CSDL, làm thế nào để đảm bảo 1 sinh viên không thể đặt 2 vé cho cùng 1 sự kiện?",
                 "Dạ thưa thầy/cô, hệ thống bảo vệ ở 2 lớp: Ở tầng ứng dụng (Controller), trước khi tạo vé mới, code thực thi câu truy vấn kiểm tra Ticket.query.filter_by(user_id=current_user.id, event_id=event.id, status='REGISTERED').first(). Nếu đã tồn tại vé, hệ thống chặn ngay lập tức và chuyển hướng người dùng về trang Vé Của Tôi. Ở tầng giao diện, nút đăng ký tự động đổi thành nút màu xanh 'Xem Vé QR & Check-in' để sinh viên không bấm nhầm lần 2 ạ."),
                ("Cơ chế trừ số lượng ghế trống (Available Slots) khi đăng ký và hoàn lại khi hủy vé hoạt động ra sao?",
                 "Dạ trong model Event có thuộc tính total_capacity và available_slots. Khi sinh viên bấm đăng ký, câu lệnh event.available_slots -= 1 được thực thi trong khối Transaction atomic db.session.commit(). Nếu có lỗi xảy ra, db.session.rollback() sẽ hoàn tác. Ngược lại, khi sinh viên hủy vé, trạng thái đổi sang CANCELLED và event.available_slots += 1 được cộng trả lại ngay lập tức để người khác có thể đăng ký ạ."),
                ("Tại sao các bạn lại dùng SQLAlchemy ORM thay vì viết các câu lệnh SQL thuần (Raw SQL)?",
                 "Dạ thưa cô, SQLAlchemy ORM mang lại 3 lợi thế vượt trội: 1. Tự động phòng chống 100% lỗi SQL Injection nhờ cơ chế Parameterized Queries. 2. Tính trừu tượng hóa cao (Database Agnostic), giúp nhóm dễ dàng chuyển đổi qua lại giữa SQL Server và SQLite mà không phải sửa lại một dòng lệnh SQL nào. 3. Code Python rõ ràng, dễ bảo trì và mở rộng theo chuẩn công nghiệp ạ.")
            ]
        },
        {
            "num": "THÀNH VIÊN 4",
            "name": "PHÂN TÍCH USECASE & LIVE DEMO LUỒNG SINH VIÊN",
            "time": "27:00 – 36:30 (Thời lượng: 9.5 phút)",
            "slides": "Slide 17 đến Slide 22",
            "key_points": [
                "Sơ đồ UseCase chi tiết của đối tượng Sinh Viên.",
                "Live Demo 1: Giao diện Trang chủ, chuyển đổi Dark/Light Mode, đồng hồ đếm ngược.",
                "Live Demo 2: Tìm kiếm tức thì (Live Search) theo từ khóa và lọc danh mục không cần F5.",
                "Live Demo 3: Cơ chế đăng nhập nhanh tài khoản sinh viên Trương Công Dũng (DE200433).",
                "Live Demo 4: Xem sự kiện đã Cháy vé (Sold Out) và sự kiện còn chỗ để đăng ký giữ chỗ.",
                "Live Demo 5: Trang Vé Của Tôi & Modal phóng to mã QR; Thao tác Hủy vé hoàn slot ghế.",
                "Live Demo 6: Xem và in Giấy Chứng Nhận Tham Gia (E-Certificate) chuẩn đại học."
            ],
            "script": (
                "\"Kính thưa quý thầy cô, bây giờ em xin phép chia sẻ màn hình để thực hiện phần Live Demo trực tiếp luồng trải nghiệm của Sinh viên trên trang web fptu-event-hub.vercel.app.\n\n"
                "(Thao tác 1 - Màn hình Trang Chủ): Như thầy cô đang thấy trên màn hình, trang chủ hiển thị hệ thống sự kiện của Đại học FPT với tông màu cam đặc trưng. "
                "Em xin phép bấm vào nút biểu tượng Mặt trăng / Mặt trời ở góc phải thanh menu: Giao diện chuyển đổi tức thì giữa chế độ Sáng (Light Mode) và Tối (Dark Mode) rất êm ái, "
                "phù hợp cho sinh viên dùng ban ngày ở giảng đường lẫn ban đêm tại ký túc xá.\n\n"
                "(Thao tác 2 - Đồng hồ đếm ngược & Live Search): Ở banner chính, chúng em có một đồng hồ đếm ngược thời gian thực tới sự kiện gần nhất là Workshop AI Agentic Coding. "
                "Bây giờ, em gõ chữ 'Hackathon' vào ô tìm kiếm: Thầy cô có thể thấy danh sách sự kiện được lọc ngay lập tức trong 0 giây mà trình duyệt không cần reload lại trang web.\n\n"
                "(Thao tác 3 - Đăng nhập Sinh viên): Em bấm nút 'Đăng Nhập FPT Mail'. Hệ thống có câu hỏi xác thực 'Bạn có phải là sinh viên trường Đại học FPT không?'. "
                "Em chọn 'Đúng, tôi là sinh viên FPT' và sử dụng tài khoản mẫu của bạn Trương Công Dũng (MSSV: DE200433). Đăng nhập thành công, thanh menu hiển thị ngay huy hiệu [Sinh Viên FPT].\n\n"
                "(Thao tác 4 - Kiểm soát cháy vé & Đặt chỗ): Em truy cập vào sự kiện 'F-Code Hackathon 2026'. Sự kiện này giới hạn 20 chỗ trong phòng Lab và đã đủ 20 bạn đăng ký, "
                "nên nút bấm tự động hiển thị nhãn màu xám 'ĐÃ HẾT VÉ (SOLD OUT)', sinh viên không thể bấm đăng ký được nữa. "
                "Bây giờ, em quay lại một sự kiện còn chỗ là 'Lễ Hội Văn Hóa CLB', bấm 'ĐĂNG KÝ GIỮ CHỖ NGAY': Hệ thống trừ slot và chuyển thẳng em vào trang 'Vé Của Tôi'.\n\n"
                "(Thao tác 5 - Xem mã QR & Hủy vé): Trong danh sách vé, em bấm nút 'Mã QR Check-in', mã QR cá nhân phóng to trên màn hình để sẵn sàng đưa cho ban tổ chức quét tại cửa hội trường. "
                "Nếu chẳng may em bận việc, em chỉ cần bấm nút đỏ 'Hủy vé' &rarr; Vé lập tức chuyển sang trạng thái ĐÃ HỦY và ghế trống được trả lại cho các bạn sinh viên khác.\n\n"
                "(Thao tác 6 - Giấy chứng nhận E-Certificate): Đối với các sự kiện đã tham gia và được ban tổ chức check-in thành công, một nút màu xanh 'Xem & In Giấy Chứng Nhận' sẽ sáng lên. "
                "Bấm vào đây, hệ thống render ra Giấy Chứng Nhận Tham Gia trang trọng, có đầy đủ tên Trương Công Dũng, MSSV DE200433, tên chương trình, ngày tháng, mã QR xác thực và chữ ký của Trưởng phòng CTSV. "
                "Sinh viên có thể bấm In hoặc lưu thành file PDF nộp báo cáo bất cứ lúc nào.\n\n"
                "Sau đây, em xin nhường quyền trình bày cho Thành viên 5 để demo luồng điều hành của Cán bộ Phòng CTSV!\""
            ),
            "qa": [
                ("Nếu sinh viên cố tình dùng công cụ Postman gửi yêu cầu đăng ký vào một sự kiện đã hết vé thì sao?",
                 "Dạ thưa thầy/cô, hệ thống được bảo vệ vững chắc ở tầng Backend route /events/<id>/register. Trước khi thêm vé, mã nguồn kiểm tra if event.available_slots <= 0. Do đó, ngay cả khi bypass qua giao diện thì Server vẫn chặn đứng với mã lỗi và thông báo 'Sự kiện đã hết sạch chỗ', đảm bảo không thể xảy ra tình trạng vượt quá sức chứa hội trường ạ."),
                ("Làm thế nào tính năng Live Search có thể lọc nhanh như vậy mà không cần tải lại trang?",
                 "Dạ tính năng này được xử lý hoàn toàn bằng Client-side JavaScript tối ưu. Mỗi thẻ sự kiện trên HTML được gắn các thuộc tính data-title, data-venue, data-category. Khi sinh viên gõ phím, sự kiện 'input' kích hoạt việc so sánh chuỗi bằng JavaScript và ẩn các phần tử không khớp bằng CSS display: none. Tốc độ phản hồi đạt mức tức thì mà không tạo bất kỳ tải nào cho máy chủ ạ."),
                ("Tính năng thêm sự kiện vào Google Calendar hoạt động như thế nào?",
                 "Dạ chúng em xây dựng thuật toán tự động sinh đường dẫn Google Calendar Event Intent với các tham số chuẩn hóa: Tiêu đề (text), thời gian bắt đầu và kết thúc (dates theo định dạng UTC ISO), địa điểm hội trường (location) và nội dung tóm tắt. Khi sinh viên bấm vào, lịch Google trên điện thoại hoặc máy tính tự động mở ra và điền sẵn thông tin, giúp sinh viên không bị quên lịch sự kiện ạ.")
            ]
        },
        {
            "num": "THÀNH VIÊN 5",
            "name": "USECASE PHÒNG CÔNG TÁC SINH VIÊN (CTSV) & KẾT LUẬN ĐỒ ÁN",
            "time": "36:30 – 45:30 (Thời lượng: 9.0 phút)",
            "slides": "Slide 23 đến Slide 28",
            "key_points": [
                "Sơ đồ UseCase chi tiết của Cán Bộ Phòng CTSV (Admin).",
                "Live Demo 1: Đăng nhập Cán bộ CTSV (ADM001), thanh Menu sạch sẽ, không trùng lặp.",
                "Live Demo 2: Trang Quản Trị CTSV (/admin/dashboard) với các chỉ số KPI trực quan.",
                "Live Demo 3: Trang Chi Tiết Sự Kiện của CTSV: Tự động thay nút đăng ký bằng Bảng Điều Hành CTSV.",
                "Live Demo 4: Xem Danh Sách Điểm Danh và thao tác Xuất File CSV / Excel.",
                "Live Demo 5: Bàn Check-in thực tế bằng Camera quét mã QR và hiệu ứng pháo hoa chúc mừng.",
                "Tổng kết kết quả đạt được, đóng góp thực tiễn và định hướng mở rộng (Mobile App, FaceID).",
                "Lời cảm ơn hội đồng và chuyển sang phần Hỏi - Đáp (Q&A)."
            ],
            "script": (
                "\"Kính thưa quý thầy cô, em xin phép tiếp quản màn hình để demo phần quan trọng nhất trong công tác tổ chức sự kiện: "
                "Đó chính là Bàn Điều Hành & Công Cụ Check-in Dành Riêng Cho Cán Bộ Phòng Công Tác Sinh Viên (CTSV).\n\n"
                "(Thao tác 1 - Đăng nhập CTSV & Navbar tinh gọn): Em bấm đăng nhập với vai trò 'Quản trị viên: Phòng CTSV' (Mã: ADM001). "
                "Thầy cô có thể quan sát thấy ngay: Thanh menu của cán bộ CTSV hoàn toàn khác biệt với sinh viên. "
                "Menu của cán bộ được tinh gọn tối đa gồm 4 mục: Trang Chủ, Quản Trị CTSV, Quản Lý Sự Kiện & Điểm Danh, và Bàn Check-in. "
                "Góc phải có huy hiệu xanh đậm [Cán Bộ CTSV - ADM001], tuyệt đối không có nhầm lẫn với vé cá nhân của sinh viên.\n\n"
                "(Thao tác 2 - Trung tâm Quản trị CTSV Dashboard): Tại trang /admin/dashboard, cán bộ theo dõi được 4 thẻ thống kê số liệu trực quan: "
                "Tổng số sự kiện toàn trường (8 sự kiện), Lượt vé đã phát hành (190 vé), Số lượt sinh viên đã check-in thực tế (115 lượt) và Danh sách các tài khoản sinh viên hoạt động gần đây.\n\n"
                "(Thao tác 3 - Bảng điều hành CTSV trên trang chi tiết sự kiện): Bây giờ em vào xem chi tiết sự kiện 'Workshop AI Agentic Coding'. "
                "Thầy cô có thể thấy một điểm thiết kế cực kỳ tinh tế: Nếu như tài khoản sinh viên thấy nút 'Đăng ký giữ chỗ', "
                "thì đối với tài khoản Cán bộ CTSV, hệ thống tự động ẩn nút đăng ký và thay thế bằng 'BẢNG ĐIỀU HÀNH SỰ KIỆN (CTSV)'. "
                "Bảng này cung cấp các nút nghiệp vụ chuyên môn: Xem danh sách điểm danh, Mở bàn quét mã QR, và Báo cáo tiến độ.\n\n"
                "(Thao tác 4 - Danh sách sinh viên & Xuất file Excel): Em bấm vào 'Xem Danh Sách Điểm Danh': Toàn bộ danh sách 25 sinh viên đã đăng ký "
                "hiển thị đầy đủ Họ tên, MSSV chuẩn FPTU, thời gian đặt chỗ, mã vé và trạng thái (ĐÃ ĐIỂM DANH màu xanh, CHƯA CHECK-IN màu vàng). "
                "Cán bộ chỉ cần bấm 1 nút 'Xuất File CSV / Excel', hệ thống lập tức tải về file bảng tính hoàn chỉnh để nộp lưu trữ hành chính.\n\n"
                "(Thao tác 5 - Bàn Quét Mã QR Check-in bằng Camera thực tế): Đây là tính năng ấn tượng nhất của dự án. Cán bộ mở trang 'Bàn Check-in'. "
                "Camera của máy tính/điện thoại lập tức sáng lên. Khi sinh viên đưa mã QR trên màn hình điện thoại vào khung ngắm, hệ thống nhận diện trong 1 giây, "
                "phát âm thanh 'bíp' thành công, bắn hiệu ứng pháo hoa rực rỡ và thông báo: 'CHECK-IN THÀNH CÔNG cho sinh viên Trương Công Dũng (DE200433)'. "
                "Nếu camera của sinh viên bị mờ hoặc vỡ màn hình, cán bộ có thể gõ trực tiếp mã vé vào ô 'Check-in thủ công' để cứu hộ tức thì.\n\n"
                "Kính thưa quý thầy cô, sau quá trình nghiên cứu và phát triển nghiêm túc, nhóm chúng em đã hoàn thiện trọn vẹn mục tiêu đề ra: "
                "Biến một cổng sự kiện truyền thống tĩnh thành một hệ thống số hóa tương tác toàn diện, giải phóng gánh nặng hành chính cho phòng CTSV "
                "và mang lại trải nghiệm tiện nghi, tự hào cho sinh viên trường F. "
                "Trong tương lai, nhóm dự kiến sẽ tích hợp thêm nhận diện khuôn mặt FaceID tại cửa hội trường và xây dựng ứng dụng di động Flutter.\n\n"
                "Nhóm chúng em xin chân thành cảm ơn quý thầy cô đã chú ý lắng nghe, và chúng em xin sẵn sàng lắng nghe các câu hỏi nhận xét, góp ý từ Hội đồng!\""
            ),
            "qa": [
                ("Làm thế nào để phân biệt rõ ràng giữa quyền hạn của Cán bộ CTSV và Sinh viên trên cùng một hệ thống?",
                 "Dạ thưa thầy/cô, hệ thống áp dụng cơ chế Role-Based Access Control (RBAC) ở cả tầng Database lẫn tầng Middleware (Decorators trong Flask). Model User có thuộc tính is_admin và is_organizer. Các Route quản trị (/admin/dashboard, /organizer/events/<id>/attendees, /check-in) đều được bảo vệ bởi Custom Decorator @admin_required. Nếu sinh viên cố tình gõ link trên URL, hệ thống sẽ từ chối truy cập (HTTP 403) và chuyển hướng về trang chủ ạ."),
                ("Nếu tại cửa hội trường xảy ra sự cố mất mạng Internet thì quy trình check-in xử lý ra sao?",
                 "Dạ thưa cô, chúng em đã chuẩn bị kịch bản dự phòng 2 tầng: Tầng 1: Web App hỗ trợ Local Cache và PWA Service Worker để tải sẵn danh sách sinh viên. Tầng 2: Cán bộ CTSV có thể mở hotspot phát 4G từ điện thoại cho thiết bị quét vì mỗi request check-in dạng JSON chỉ tiêu tốn vài kilobyte dữ liệu. Đồng thời ô check-in thủ công cho phép nhập mã vé ngay cả khi camera gặp sự cố ánh sáng yếu ạ."),
                ("File CSV xuất ra có hỗ trợ đầy đủ tiếng Việt có dấu khi mở bằng Microsoft Excel trên Windows không?",
                 "Dạ có thưa thầy/cô. Đây là lỗi kỹ thuật kinh điển khi xuất file CSV trên Windows (bị lỗi font Unicode cp1258). Để khắc phục triệt để, trong route /organizer/events/<id>/export-csv, chúng em đã chủ động ghi mã Byte Order Mark (UTF-8 BOM '\\ufeff') vào đầu luồng dữ liệu trước khi xuất dòng tiêu đề. Nhờ vậy, khi mở file bằng Microsoft Excel trên bất kỳ máy tính Windows nào, toàn bộ tên tiếng Việt có dấu như 'Trương Công Dũng', 'Nguyễn Việt Anh' đều hiển thị hoàn hảo 100% mà không bị lỗi font ạ.")
            ]
        }
    ]

    for m in members:
        # Member Section Header
        doc.add_page_break()
        sec_h = doc.add_paragraph()
        sec_r = sec_h.add_run(f"III.{m['num'][-1]}. {m['num']}: {m['name']}")
        sec_r.font.size = Pt(13.5)
        sec_r.font.bold = True
        sec_r.font.color.rgb = NAVY
        sec_h.paragraph_format.space_before = Pt(14)
        sec_h.paragraph_format.space_after = Pt(4)

        # Meta info of member
        info_p = doc.add_paragraph()
        info_r1 = info_p.add_run(f"⏱ Thời lượng trình bày dự kiến: ")
        info_r1.font.bold = True
        info_p.add_run(f"{m['time']}  |  ")
        info_r2 = info_p.add_run(f"🖥 Slide phụ trách: ")
        info_r2.font.bold = True
        info_p.add_run(f"{m['slides']}")

        # Key points box
        doc.add_paragraph().add_run("📌 Các Luận Điểm Trọng Tâm Cần Trình Bày:").font.bold = True
        for kp in m['key_points']:
            bp = doc.add_paragraph(style='List Bullet')
            bp.add_run(kp)

        # Verbatim Script Box
        doc.add_paragraph().paragraph_format.space_before = Pt(6)
        scr_head = doc.add_paragraph()
        scr_head_r = scr_head.add_run("🎙 LỜI THOẠI THUYẾT TRÌNH CHI TIẾT TỪNG CÂU CHỮ (VERBATIM SCRIPT):")
        scr_head_r.font.bold = True
        scr_head_r.font.color.rgb = PRIMARY

        # Script callout table
        tbl_script = doc.add_table(rows=1, cols=1)
        tbl_script.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell_scr = tbl_script.rows[0].cells[0]
        set_cell_background(cell_scr, "FFF7ED") # light orange
        set_cell_margins(cell_scr, 140, 140, 180, 180)

        p_scr = cell_scr.paragraphs[0]
        r_scr = p_scr.add_run(m['script'])
        r_scr.font.size = Pt(10)
        r_scr.font.italic = True
        r_scr.font.color.rgb = RGBColor(15, 23, 42)

        # Q&A Box
        doc.add_paragraph().paragraph_format.space_before = Pt(10)
        qa_head = doc.add_paragraph()
        qa_head_r = qa_head.add_run(f"❓ BỘ 3 CÂU HỎI VẤN ĐÁP THẦY CÔ THƯỜNG HỎI {m['num']} & CÂU TRẢ LỜI MẪU:")
        qa_head_r.font.bold = True
        qa_head_r.font.color.rgb = NAVY

        for q_idx, (q_text, a_text) in enumerate(m['qa'], start=1):
            p_q = doc.add_paragraph()
            p_q.paragraph_format.space_before = Pt(4)
            p_q.paragraph_format.space_after = Pt(2)
            rq_num = p_q.add_run(f"Câu hỏi {q_idx}: ")
            rq_num.font.bold = True
            rq_num.font.color.rgb = PRIMARY
            rq_text = p_q.add_run(q_text)
            rq_text.font.bold = True

            p_a = doc.add_paragraph()
            p_a.paragraph_format.space_after = Pt(6)
            ra_lbl = p_a.add_run("👉 Trả lời mẫu: ")
            ra_lbl.font.bold = True
            ra_lbl.font.color.rgb = SUCCESS
            ra_text = p_a.add_run(f"\"{a_text}\"")
            ra_text.font.size = Pt(10)

    # 4. Preparation Checklist
    doc.add_page_break()
    chk_h = doc.add_paragraph()
    chk_r = chk_h.add_run("IV. CHECKLIST CHUẨN BỊ KỸ THUẬT TRƯỚC KHI BƯỚC VÀO PHÒNG BẢO VỆ")
    chk_r.font.size = Pt(14)
    chk_r.font.bold = True
    chk_r.font.color.rgb = NAVY
    chk_h.paragraph_format.space_before = Pt(14)
    chk_h.paragraph_format.space_after = Pt(6)

    checklist_items = [
        ("Kiểm tra kết nối mạng & Trang web Online:", "Mở sẵn link Vercel https://fptu-event-hub.vercel.app/ trên trình duyệt để đề phòng sự cố localhost."),
        ("Chuẩn bị sẵn 2 Tab trình duyệt độc lập:", "• Tab 1: Đăng nhập sẵn tài khoản Sinh viên (dungtcde200433@fpt.edu.vn / pass123).\n• Tab 2 (Cửa sổ Ẩn danh / Profile khác): Đăng nhập sẵn tài khoản Cán bộ CTSV (ctsv.admin@fpt.edu.vn / pass123)."),
        ("Cấp quyền Camera cho Bàn Check-in:", "Trước khi thuyết trình, truy cập /check-in và bấm 'Cho phép (Allow)' quyền truy cập camera trên Chrome/Edge để khi demo không bị pop-up hỏi quyền làm gián đoạn."),
        ("Chuẩn bị sẵn 1 điện thoại mở mã QR:", "Dùng điện thoại cá nhân đăng nhập sinh viên, mở sẵn 1 vé sự kiện có mã QR trên màn hình để khi Thành viên 5 demo Camera thì đưa điện thoại lại gần laptop quét thử ngay trước mắt hội đồng."),
        ("Chuẩn bị file Slide PowerPoint:", "Trình chiếu slide ở chế độ Presenter View để nhìn thấy thời gian đếm ngược, đảm bảo không ai nói quá thời gian quy định.")
    ]

    for title, desc in checklist_items:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(f"{title} ").font.bold = True
        p.add_run(desc)

    # Save document
    doc.save(output_path)
    print(f"Document created successfully at: {output_path}")

if __name__ == "__main__":
    out_file = r"C:\Users\truon\fptu_eventhub\KICH_BAN_THUYET_TRINH_FPTU_EVENTHUB_5_NGUOI.docx"
    create_presentation_document(out_file)
