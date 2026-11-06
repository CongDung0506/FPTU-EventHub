# -*- coding: utf-8 -*-
"""
Script to generate the comprehensive 45-50 minute 5-person Presentation Script & Q&A Defense Guide
in Microsoft Word (.docx) format for FPTU EventHub, explicitly structured around 4 required pillars:
1. Giới thiệu dự án (Project Introduction & Background)
2. Các tool và công nghệ được sử dụng (Tech Stack, Tools & Security Libraries)
3. Kiến trúc dự án (MVC, Data Flow, Database ERD & Dual-Database Switch)
4. Chức năng chính mô tả bằng UseCase (Student & CTSV UseCases + Live Demo)
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

    # Set page margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)

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
    run_sub = title_p.add_run("TRƯỜNG ĐẠI HỌC FPT — BẢO VỆ ĐỒ ÁN CHUYÊN NGÀNH CÔNG NGHỆ THÔNG TIN\n")
    run_sub.font.size = Pt(11)
    run_sub.font.bold = True
    run_sub.font.color.rgb = NAVY

    run_title = title_p.add_run("KỊCH BẢN BÁO CÁO THUYẾT TRÌNH & CẨM NANG VẤN ĐÁP BẢO VỆ ĐỒ ÁN\n(THỜI LƯỢNG: 45 – 50 PHÚT — PHÂN BỔ 5 THÀNH VIÊN)\n")
    run_title.font.size = Pt(17)
    run_title.font.bold = True
    run_title.font.color.rgb = PRIMARY

    run_proj = title_p.add_run("DỰ ÁN: FPTU EVENTHUB — CỔNG QUẢN LÝ & ĐĂNG KÝ SỰ KIỆN NỘI BỘ FPT UNIVERSITY")
    run_proj.font.size = Pt(12.5)
    run_proj.font.bold = True
    run_proj.font.color.rgb = NAVY

    # Meta Info Box Table
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False

    meta_data = [
        ("Cổng web trực tuyến (Vercel):", "https://fptu-event-hub.vercel.app/"),
        ("Kho lưu trữ mã nguồn (GitHub):", "https://github.com/CongDung0506/FPTU-EventHub"),
        ("Cấu trúc 4 trụ cột báo cáo:", "1. Giới thiệu dự án | 2. Tools & Công nghệ | 3. Kiến trúc dự án | 4. UseCases"),
        ("Công nghệ cốt lõi áp dụng:", "Python 3.14, Flask, HTML5/CSS (BEM), WebRTC Camera QR, SQL Server & SQLite"),
        ("Phân quyền hệ thống (RBAC):", "Sinh viên (Student) & Phòng Công Tác Sinh Viên (Admin/CTSV)"),
        ("Thời lượng & Phân bổ nhân sự:", "45 – 50 phút tổng cộng, phân chia đều 5 thành viên (8 – 9.5 phút/thành viên)")
    ]

    for idx, (label, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width = Inches(2.6)
        cell_val.width = Inches(4.5)

        set_cell_background(cell_lbl, "F8FAFC")
        set_cell_background(cell_val, "FFFFFF")
        set_cell_margins(cell_lbl, 70, 70, 110, 110)
        set_cell_margins(cell_val, 70, 70, 110, 110)

        p0 = cell_lbl.paragraphs[0]
        p0.add_run(label).font.bold = True
        p0.runs[0].font.size = Pt(9.5)
        p0.runs[0].font.color.rgb = NAVY

        p1 = cell_val.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.size = Pt(9.5)
        if "http" in val:
            r1.font.color.rgb = PRIMARY
            r1.font.underline = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # TIMELINE TABLE
    # -------------------------------------------------------------
    h_time = doc.add_paragraph()
    r_htime = h_time.add_run("BẢNG PHÂN BỔ THỜI LƯỢNG 45 – 50 PHÚT THEO 4 TRỤ CỘT BÁO CÁO")
    r_htime.font.size = Pt(13)
    r_htime.font.bold = True
    r_htime.font.color.rgb = NAVY
    h_time.paragraph_format.space_before = Pt(10)
    h_time.paragraph_format.space_after = Pt(4)

    time_table = doc.add_table(rows=7, cols=4)
    time_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Thời Lượng", "Thành Viên", "Trụ Cột Báo Cáo Phụ Trách", "Slide & Demo"]

    for col_idx, h_text in enumerate(headers):
        cell = time_table.rows[0].cells[col_idx]
        set_cell_background(cell, "004B91")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)

    time_rows = [
        ("Phút 00:00 – 09:30\n(9.5 phút)", "Thành Viên 1 (Nhóm Trưởng)\nTrương Công Dũng", "1. GIỚI THIỆU DỰ ÁN\n(Bối cảnh FPTU, Pain Points cổng cũ events.fptu.vn, Mục tiêu & Bảng so sánh đột phá)", "Slide 1 &rarr; 5\nTrang chủ EventHub"),
        ("Phút 09:30 – 18:30\n(9.0 phút)", "Thành Viên 2\nKỹ Thuật & Bảo Mật", "2. CÁC TOOL & CÔNG NGHỆ\n(Tech Stack: Python/Flask, Bleach XSS, WebRTC Camera QR, PBKDF2/Salt, Zero-SSO)", "Slide 6 &rarr; 10\nVS Code (Mã nguồn)"),
        ("Phút 18:30 – 27:00\n(8.5 phút)", "Thành Viên 3\nKiến Trúc & Database", "3. KIẾN TRÚC DỰ ÁN\n(Mô hình MVC, Luồng Request, Thiết kế CSDL ERD 6 bảng, Cơ chế Dual-Database)", "Slide 11 &rarr; 16\nDiagram ERD, DB Tool"),
        ("Phút 27:00 – 36:30\n(9.5 phút)", "Thành Viên 4\nLive Demo Sinh Viên", "4A. CHỨC NĂNG CHÍNH (USECASE SINH VIÊN)\n(UC01 &rarr; UC08: Live Search, Đặt vé real-time, Quản lý ví vé QR, Hủy vé, E-Cert)", "Slide 17 &rarr; 22\nTrình duyệt (Tab SV)"),
        ("Phút 36:30 – 45:30\n(9.0 phút)", "Thành Viên 5\nLive Demo CTSV & Kết Luận", "4B. CHỨC NĂNG CHÍNH (USECASE PHÒNG CTSV)\n(UC09 &rarr; UC14: Bảng điều hành CTSV, Quét Camera QR Check-in, Xuất CSV, Tổng kết)", "Slide 23 &rarr; 28\nTrình duyệt (Tab CTSV)"),
        ("Phút 45:30 – 50:00+\n(5 – 10 phút)", "Cả 5 Thành Viên\nHội đồng phản biện", "PHẦN VẤN ĐÁP BẢO VỆ (Q&A)\n(Trả lời 15 câu hỏi kỹ thuật chuyên sâu từ quý thầy cô phản biện)", "Tất cả slide, mã nguồn")
    ]

    for row_idx, r_data in enumerate(time_rows, start=1):
        row = time_table.rows[row_idx]
        bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(r_data):
            cell = row.cells[col_idx]
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, 70, 70, 90, 90)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9)
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = PRIMARY
            elif col_idx == 1:
                r.font.bold = True

    # -------------------------------------------------------------
    # PHẦN 1: GIỚI THIỆU DỰ ÁN
    # -------------------------------------------------------------
    doc.add_page_break()
    p1_h = doc.add_paragraph()
    r1_h = p1_h.add_run("PHẦN 1: GIỚI THIỆU DỰ ÁN (THÀNH VIÊN 1: 00:00 – 09:30)")
    r1_h.font.size = Pt(13.5)
    r1_h.font.bold = True
    r1_h.font.color.rgb = NAVY
    p1_h.paragraph_format.space_before = Pt(12)
    p1_h.paragraph_format.space_after = Pt(4)

    doc.add_paragraph().add_run("1.1. Bối cảnh thực tế tại Đại học FPT:").font.bold = True
    p_bc = doc.add_paragraph()
    p_bc.add_run(
        "Đại học FPT nổi tiếng với văn hóa phong trào bùng nổ, quy tụ hơn 30 câu lạc bộ học thuật, nghệ thuật, thể thao và kỹ năng mềm. "
        "Hàng tuần, tại các Hội trường Alpha, Beta, Phòng Lab Gamma và Nhà thi đấu đều diễn ra các sự kiện quy mô lớn: Workshop AI, Hackathon 24h, "
        "Career Talk doanh nghiệp và giải vô địch Vovinam. Nhu cầu tham gia và gắn kết của sinh viên là vô cùng to lớn."
    )

    doc.add_paragraph().add_run("1.2. Phân tích bất cập của cổng cũ (events.fptu.vn) & phương pháp truyền thống:").font.bold = True
    bullet_pts1 = [
        ("Bản chất bảng tin tĩnh:", "Cổng events.fptu.vn chỉ đăng bài viết thông báo, không có tương tác giữ chỗ trực tiếp. Để đăng ký, các CLB phải dẫn link ra ngoài Google Form."),
        ("Vấn nạn vỡ trận số lượng ghế (Capacity Overload):", "Hội trường Alpha chỉ có 100 ghế, nhưng Google Form không thể giới hạn tự động theo thời gian thực (Atomic capacity constraint), dẫn đến nhận 200 đơn đăng ký gây quá tải."),
        ("Điểm danh thủ công chậm chạp & ùn tắc:", "Đến ngày diễn ra, sinh viên phải xếp hàng dài trước cửa hội trường để cán bộ dò tìm tên trên giấy hoặc file Excel, dễ nhầm lẫn và tốn 30 - 45 phút."),
        ("Hiện tượng 'ghế ảo' không thể hủy chỗ:", "Sinh viên có việc bận đột xuất không thể hủy vé, dẫn đến tình trạng trên danh sách thì đầy nhưng ghế ngồi trong hội trường lại trống trơn."),
        ("Cấp chứng nhận chậm trễ:", "Giấy chứng nhận tham gia thường phải chờ cán bộ thiết kế gửi email sau nhiều tuần hoặc không được cấp.")
    ]
    for b_title, b_desc in bullet_pts1:
        bp = doc.add_paragraph(style='List Bullet')
        bp.add_run(b_title).font.bold = True
        bp.add_run(f" {b_desc}")

    doc.add_paragraph().add_run("1.3. Mục tiêu & Giá trị đột phá của FPTU EventHub:").font.bold = True
    p_mt = doc.add_paragraph()
    p_mt.add_run(
        "FPTU EventHub được phát triển nhằm khép kín toàn bộ vòng đời của một sự kiện: "
        "Sinh viên đăng nhập FPT SSO &rarr; Giữ chỗ tức thì nhận vé điện tử kèm mã QR riêng &rarr; Cán bộ CTSV dùng Camera quét QR điểm danh trong 1 giây &rarr; Nhận ngay Giấy chứng nhận E-Certificate chuẩn học thuật."
    )

    # Comparison Table inside Section 1
    doc.add_paragraph().add_run("1.4. Bảng so sánh đột phá giữa Cổng cũ events.fptu.vn và FPTU EventHub:").font.bold = True
    comp_table = doc.add_table(rows=8, cols=3)
    comp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_heads = ["Tiêu Chí So Sánh", "Cổng Cũ Của Trường (events.fptu.vn)", "FPTU EventHub (Web Của Nhóm) 🌟"]
    for c_i, c_h in enumerate(c_heads):
        cell = comp_table.rows[0].cells[c_i]
        set_cell_background(cell, "F26F21" if c_i == 2 else "004B91")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(c_h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)

    comp_rows_data = [
        ("Mô hình hoạt động", "Trang tin tức tĩnh / blog thông báo sự kiện, không tương tác đặt chỗ nội bộ.", "Nền tảng quản trị và vận hành sự kiện trực tuyến khép kín (Full-lifecycle event portal)."),
        ("Cơ chế đặt vé (Ticket)", "Chuyển hướng ra ngoài điền Google Form thủ công, không có mã vé định danh.", "Sinh vé điện tử tức thì (mã dạng FU-2026-XXXXX), lưu vào Ví vé cá nhân có mã QR riêng."),
        ("Quy trình Check-in", "In danh sách giấy hoặc dò file Excel thủ công, dễ ùn tắc kéo dài tại cửa phòng.", "Tích hợp Bàn Check-in bằng Camera điện thoại/laptop (WebRTC), quét QR xong trong 1 giây."),
        ("Chứng nhận tham gia", "Chờ cán bộ thiết kế gửi email sau nhiều tuần (hoặc không có giấy chứng nhận).", "Hệ thống tự động phát hành Giấy Chứng Nhận Điện Tử (E-Cert) có mã số xác thực ngay khi check-in."),
        ("Kiểm soát sức chứa", "Không đếm số ghế trống real-time, sinh viên đăng ký quá tải gây vỡ trận hội trường.", "Thanh sức chứa trực quan; tự động khóa nút và gắn mác ĐÃ HẾT VÉ (SOLD OUT) khi kín chỗ."),
        ("Hủy vé & Nhượng chỗ", "Sinh viên bận không có cách nào hủy vé, dẫn đến đặt chỗ ảo nhưng hội trường vắng ngắt.", "Sinh viên hủy vé 1-click, hệ thống tự động hoàn lại slot ghế trống cho bạn khác."),
        ("Phân quyền nghiệp vụ", "Chung một giao diện người xem, không có trang nghiệp vụ cho cán bộ CTSV.", "Tách biệt tuyệt đối 2 luồng: Sinh viên (đặt vé, QR) & Phòng CTSV (điều hành, điểm danh, xuất CSV).")
    ]
    for r_i, r_d in enumerate(comp_rows_data, start=1):
        row = comp_table.rows[r_i]
        bg_col = "F8FAFC" if r_i % 2 == 1 else "FFFFFF"
        for col_i, text in enumerate(r_d):
            cell = row.cells[col_i]
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9)
            if col_i == 0:
                r.font.bold = True

    # Verbatim Script Member 1
    doc.add_paragraph().paragraph_format.space_before = Pt(8)
    doc.add_paragraph().add_run("🎙 Lời thoại thuyết trình mẫu Thành viên 1 (9.5 phút):").font.bold = True
    tbl_s1 = doc.add_table(rows=1, cols=1)
    tbl_s1.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_s1 = tbl_s1.rows[0].cells[0]
    set_cell_background(c_s1, "FFF7ED")
    set_cell_margins(c_s1, 100, 100, 140, 140)
    p_s1 = c_s1.paragraphs[0]
    r_s1 = p_s1.add_run(
        "\"Kính thưa quý thầy cô trong Hội đồng chấm đồ án tốt nghiệp cùng toàn thể các bạn sinh viên!\n\n"
        "Em tên là Trương Công Dũng, nhóm trưởng của dự án. Đại diện cho nhóm 5 thành viên của chúng em hôm nay, "
        "em xin trân trọng giới thiệu đề tài: 'FPTU EventHub — Cổng Quản Lý & Đăng Ký Sự Kiện Sinh Viên Đại Học FPT'.\n\n"
        "Như thầy cô đã biết, Đại học FPT là một môi trường năng động với hơn 30 CLB học thuật, nghệ thuật và thể thao. "
        "Mỗi tuần, tại Hội trường Alpha, Beta hay phòng Lab Gamma đều diễn ra hàng loạt Workshop công nghệ, Hackathon và giải đấu phong trào. "
        "Tuy nhiên, khi nhìn vào cổng thông tin hiện tại của trường là events.fptu.vn, chúng em nhận thấy một bài toán rất lớn: Cổng cũ thực chất chỉ là một bảng tin tĩnh đăng bài thông báo. "
        "Khi sinh viên muốn đăng ký giữ chỗ, ban tổ chức vẫn phải dẫn link ra ngoài Google Form hoặc biểu mẫu trung gian.\n\n"
        "Cách làm này để lại 4 nỗi đau nhức nhối:\n"
        "1. Hội trường Alpha chỉ có sức chứa 100 ghế, nhưng Google Form không thể giới hạn tự động theo thời gian thực, dẫn đến nhận 200 đơn đăng ký gây vỡ trận hội trường.\n"
        "2. Đến giờ diễn ra, sinh viên phải đứng chen chúc ở cửa để cán bộ cầm giấy hoặc dò từng dòng Excel rất thủ công và chậm chạp.\n"
        "3. Sinh viên bận việc đột xuất không có cách nào hủy vé để nhường lại cho bạn khác, dẫn đến tình trạng trên danh sách thì đầy nhưng ghế ngồi lại trống.\n"
        "4. Giấy chứng nhận tham gia thường phải chờ thiết kế gửi email sau nhiều tuần, gây nản lòng cho sinh viên.\n\n"
        "Chính vì vậy, nhóm chúng em đã xây dựng FPTU EventHub nhằm số hóa 100% quy trình: Sinh viên đăng nhập bằng email trường (@fpt.edu.vn) &rarr; "
        "Giữ chỗ tức thì nhận vé điện tử kèm mã QR riêng &rarr; Cán bộ CTSV dùng Camera quét QR điểm danh chỉ trong 1 giây &rarr; Nhận ngay Giấy chứng nhận E-Certificate chuẩn học thuật.\n\n"
        "Sau đây, em xin kính mời Thành viên 2 tiếp tục trình bày về các Tool và Công nghệ cốt lõi mà nhóm đã lựa chọn để triển khai dự án!\""
    )
    r_s1.font.size = Pt(9.5)
    r_s1.font.italic = True

    # Q&A Member 1
    doc.add_paragraph().paragraph_format.space_before = Pt(8)
    doc.add_paragraph().add_run("❓ Bộ 3 câu hỏi vấn đáp trọng tâm cho Thành viên 1:").font.bold = True
    qa1 = [
        ("Tại sao nhóm không dùng luôn Google Forms hay Microsoft Forms cho nhanh mà phải lập trình riêng một hệ thống web?",
         "Dạ thưa thầy/cô, Google Forms có 3 giới hạn cốt tử: Thứ nhất, Google Form không kiểm soát sức chứa ghế (Capacity) theo cơ chế giao dịch Transaction thời gian thực, dễ gây vỡ trận số lượng. Thứ hai, Google Forms không tự sinh được vé điện tử có mã QR định danh cá nhân để quét tại cửa. Thứ ba, Google Forms không có kiến trúc phân quyền (RBAC) để phục vụ công tác điều hành của Cán bộ CTSV và tự động xuất file báo cáo điểm danh ạ."),
        ("Đối tượng người dùng chính của hệ thống là ai và họ được phân quyền như thế nào?",
         "Dạ hệ thống được thiết kế theo chuẩn phân quyền Role-Based Access Control (RBAC) với 2 nhóm người dùng chuyên biệt: 1. Sinh viên (Student): Khám phá sự kiện, đặt vé giữ chỗ, sở hữu Ví vé QR cá nhân, hủy vé và in Giấy chứng nhận. 2. Phòng Công Tác Sinh Viên (Admin/CTSV): Giám sát dữ liệu toàn trường, duyệt và đăng sự kiện, mở Bàn Check-in quét mã QR bằng camera và xuất báo cáo điểm danh ra file Excel/CSV ạ."),
        ("Hệ thống giải quyết vấn đề 'đặt chỗ ảo' (ghế đăng ký kín nhưng người không đến) như thế nào?",
         "Dạ chúng em giải quyết bằng 2 cơ chế: 1. Tính năng 'Hủy vé 1-click' trong trang Vé Của Tôi: khi sinh viên biết mình bận, các bạn bấm hủy thì slot ghế được hoàn trả ngay lập tức cho bạn khác trên trang chủ. 2. Mỗi sinh viên chỉ được đặt 1 vé duy nhất cho mỗi sự kiện nhờ cơ chế kiểm tra ràng buộc ở cả Client lẫn Server, chấm dứt hoàn toàn tình trạng 1 người ôm nhiều chỗ ạ.")
    ]
    for q_i, (q_t, a_t) in enumerate(qa1, start=1):
        p_q = doc.add_paragraph()
        p_q.add_run(f"Câu {q_i}: {q_t}").font.bold = True
        p_a = doc.add_paragraph()
        p_a.add_run("👉 Trả lời mẫu: ").font.bold = True
        p_a.runs[0].font.color.rgb = SUCCESS
        p_a.add_run(f"\"{a_t}\"").font.size = Pt(9.5)

    # -------------------------------------------------------------
    # PHẦN 2: CÁC TOOL VÀ CÔNG NGHỆ ĐƯỢC SỬ DỤNG
    # -------------------------------------------------------------
    doc.add_page_break()
    p2_h = doc.add_paragraph()
    r2_h = p2_h.add_run("PHẦN 2: CÁC TOOL VÀ CÔNG NGHỆ ĐƯỢC SỬ DỤNG ĐỂ TRIỂN KHAI DỰ ÁN (THÀNH VIÊN 2: 09:30 – 18:30)")
    r2_h.font.size = Pt(13.5)
    r2_h.font.bold = True
    r2_h.font.color.rgb = NAVY
    p2_h.paragraph_format.space_before = Pt(12)
    p2_h.paragraph_format.space_after = Pt(4)

    doc.add_paragraph().add_run("2.1. Phân loại Công nghệ và Công cụ (Tech Stack Ecosystem):").font.bold = True
    
    tools_table = doc.add_table(rows=6, cols=3)
    tools_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_heads = ["Nhóm Công Nghệ", "Công Cụ / Thư Viện Cụ Thể", "Mục Đích & Vai Trò Trong Dự Án"]
    for t_i, t_h in enumerate(t_heads):
        cell = tools_table.rows[0].cells[t_i]
        set_cell_background(cell, "004B91")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(t_h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)

    tools_data = [
        ("Backend & Framework", "Python 3.14 + Flask Microframework\nJinja2 Template Engine\nWerkzeug WSGI", "Tạo máy chủ ứng dụng web tốc độ cao, xử lý nghiệp vụ tinh gọn, dễ module hóa và tích hợp tốt với các thư viện AI/Data sau này."),
        ("Bảo Mật & Kiểm Thực", "Bleach (HTML Sanitizer)\nWerkzeug Security (PBKDF2/SHA-256)\nFlask-WTF & CSRFProtect", "Lọc mã độc XSS khi render Markdown bài viết; Băm mật khẩu sinh viên với Salt ngẫu nhiên; Ngăn chặn tấn công CSRF và kiểm thực email FPT."),
        ("Frontend & UI/UX", "HTML5 & CSS Scoped (BEM standard)\nJavaScript ES6+ (Native Fetch)\nBootstrap 3 Grid & FontAwesome 6", "Đảm bảo giao diện chuẩn FPT Design System, tránh xung đột class CSS; Tích hợp Dark/Light Theme mượt mà lưu trữ tại LocalStorage."),
        ("Quét QR & Tương Tác", "html5-qrcode (WebRTC MediaDevices)\nCanvas-Confetti & Web Audio API\nGoogle Calendar Event Intent API", "Bật camera laptop/điện thoại quét mã QR vé thời gian thực trong 1 giây; Bắn hiệu ứng pháo hoa khi check-in; Đồng bộ lịch vào Google Calendar."),
        ("Cơ Sở Dữ Liệu & Cloud", "SQLAlchemy ORM (Data Abstraction)\nMicrosoft SQL Server (ODBC Driver 17)\nSQLite Serverless & Vercel Cloud", "Trừu tượng hóa truy vấn, chống SQL Injection; Chạy Dual-Database thích ứng (SQL Server cục bộ môn học và SQLite trên Vercel Serverless).")
    ]
    for r_i, r_d in enumerate(tools_data, start=1):
        row = tools_table.rows[r_i]
        bg_col = "F8FAFC" if r_i % 2 == 1 else "FFFFFF"
        for col_i, text in enumerate(r_d):
            cell = row.cells[col_i]
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9)
            if col_i == 0:
                r.font.bold = True


    # 2.2 Bang tong hop 100% cac ham PWD301
    doc.add_paragraph().paragraph_format.space_before = Pt(8)
    doc.add_paragraph().add_run("2.2. Bảng Tổng Hợp Đầy Đủ 100% Các Hàm & Kỹ Thuật Lập Trình Web Python (PWD301) Được Áp Dụng:").font.bold = True
    
    pwd_table = doc.add_table(rows=9, cols=3)
    pwd_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    pwd_heads = ["Mô-đun Kiến Thức PWD301", "Danh Sách Các Hàm & Lớp Được Hiện Thực", "Vị Trí & Nghiệp Vụ Cụ Thể Trong Dự Án"]
    for p_i, p_h in enumerate(pwd_heads):
        cell = pwd_table.rows[0].cells[p_i]
        set_cell_background(cell, "004B91")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(p_h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)

    pwd_data = [
        ("1. Routing, HTTP & Error Handling", 
         "@app.route(methods=['GET','POST','PUT','DELETE'])\nrender_template(), redirect(), url_for()\nrequest.args, request.form, request.get_json()\nflash(), abort(400/403/404/500), jsonify()\n@app.errorhandler(400/403/404/500)", 
         "app.py: Xử lý toàn bộ vòng đời Request/Response; Hỗ trợ đồng thời cả hiển thị giao diện HTML (400.html, 403.html, 404.html, 500.html) lẫn phản hồi JSON chuẩn REST API."),
        
        ("2. Template Engine & Jinja Filters", 
         "@app.template_filter('vnd')\n@app.template_filter('datetime_format')\n@app.template_filter('timeago')\n@app.template_filter('truncate_words')\n@app.context_processor (inject_global_data)", 
         "app.py: Định dạng tiền tệ VND, định dạng ngày tháng chuẩn Việt Nam, tính toán thời gian tương đối (Sắp diễn ra, Còn n ngày), cắt ngắn mô tả; Tiêm biến dùng chung vào mọi template Jinja2."),
        
        ("3. Authentication & Session Security", 
         "LoginManager(), @login_manager.user_loader\nlogin_user(remember=True), logout_user()\n@login_required, current_user.is_authenticated\nis_safe_url() (Open Redirect Prevention)\ngenerate_password_hash(), check_password_hash()", 
         "app.py & models.py: Cơ chế Zero-SSO nhận diện FPT Mail; Bảo vệ chuyển hướng an toàn theo bài Lab 6; Mã hóa mật khẩu PBKDF2/SHA-256 kèm muối ngẫu nhiên (Werkzeug Security)."),
        
        ("4. Form Validation & CSRF (Flask-WTF)", 
         "FlaskForm, StringField, PasswordField, BooleanField\nTextAreaField, IntegerField, SelectField, DateTimeLocalField\nDataRequired, Email, Length, NumberRange, EqualTo\nCustom validator: validate_email(), validate_student_id()\nCustom validator: validate_phone() (10 số bắt đầu bằng 0)", 
         "forms.py: Kiểm thực dữ liệu nghiêm ngặt ở tầng Server; Kiểm tra đuôi email @fpt.edu.vn; Kiểm tra MSSV FPT; Kiểm tra số điện thoại chuẩn Việt Nam (bài Lab 6); CSRF token form.hidden_tag()."),
        
        ("5. Cơ Sở Dữ Liệu & SQLAlchemy ORM", 
         "db.Model, Column, ForeignKey, relationship()\nback_populates, cascade='all, delete-orphan'\ndb.session.add(), db.session.delete()\ndb.session.commit(), db.session.rollback()\nget_or_404(), filter(), filter_by(), order_by()\nModel.query.paginate(page, per_page, error_out=False)\nto_dict() serialization", 
         "models.py & app.py: 100% truy vấn ORM chuẩn hóa; Cơ chế giao dịch Transaction nguyên tử (Atomic) bảo vệ số lượng ghế; Phân trang sự kiện bằng paginate(); Xuất dữ liệu to_dict() cho REST API."),
        
        ("6. Phân Quyền RBAC (Decorators)", 
         "@role_required(*roles) (3-level parameterized decorator)\n@organizer_required (Organizer & Admin)\n@admin_required (Admin only)\nKiểm tra current_user.role và abort(403)", 
         "decorators.py: Kế thừa mô hình phân quyền từ bài thực hành FPT Parking; Tách biệt triệt để quyền hạn giữa Sinh viên và Cán bộ CTSV; Trả về lỗi 403 Forbidden khi vi phạm."),
        
        ("7. Full RESTful API v1 (Chương 9 & Exam)", 
         "GET /api/v1/events (phân trang, lọc danh mục, tìm kiếm)\nGET /api/v1/events/<id>\nPOST /api/v1/events (Tạo mới, mã 201 Created)\nPUT /api/v1/events/<id> (Cập nhật, mã 200 OK)\nDELETE /api/v1/events/<id> (Xóa, mã 200/204)\nGET /api/v1/categories, GET /api/v1/stats\nPOST /api/v1/auth/login", 
         "app.py: Xây dựng toàn bộ hệ thống API chuẩn RESTful theo yêu cầu Chương 9 và bài thi ParkTicket API; Trả về mã lỗi HTTP chuẩn hóa (200, 201, 204, 400, 401, 403, 404, 422)."),
        
        ("8. Xử Lý Tệp Tin & Xuất Báo Cáo", 
         "csv.writer(), io.StringIO()\nResponse(mimetype='text/csv')\nContent-Disposition: attachment\nKý tự UTF-8 BOM ('\\ufeff') hỗ trợ Microsoft Excel", 
         "app.py (export_attendees_csv): Xuất danh sách sinh viên tham dự sự kiện ra file CSV chuẩn tiếng Việt có dấu, phục vụ lưu trữ văn thư và đối soát cho Phòng CTSV.")
    ]
    for r_i, r_d in enumerate(pwd_data, start=1):
        row = pwd_table.rows[r_i]
        bg_col = "F8FAFC" if r_i % 2 == 1 else "FFFFFF"
        for col_i, text in enumerate(r_d):
            cell = row.cells[col_i]
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(8.5)
            if col_i == 0:
                r.font.bold = True

    # Verbatim Script Member 2
    doc.add_paragraph().paragraph_format.space_before = Pt(8)
    doc.add_paragraph().add_run("🎙 Lời thoại thuyết trình mẫu Thành viên 2 (9.0 phút):").font.bold = True
    tbl_s2 = doc.add_table(rows=1, cols=1)
    tbl_s2.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_s2 = tbl_s2.rows[0].cells[0]
    set_cell_background(c_s2, "FFF7ED")
    set_cell_margins(c_s2, 100, 100, 140, 140)
    p_s2 = c_s2.paragraphs[0]
    r_s2 = p_s2.add_run(
        "\"Kính thưa quý thầy cô, em xin phép tiếp nối phần trình bày của nhóm trưởng về bức tranh công nghệ và các giải pháp kỹ thuật bảo mật của FPTU EventHub.\n\n"
        "Để xây dựng một hệ thống có tốc độ phản hồi nhanh, tải nhẹ và dễ triển khai lên môi trường Cloud, nhóm đã lựa chọn Backend là Python 3.14 kết hợp cùng Flask Framework. "
        "Về mặt kiến trúc công nghệ và bảo mật, nhóm tập trung xử lý 4 trụ cột quan trọng nhất:\n\n"
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
        "Đặc biệt, thưa quý thầy cô, hệ thống FPTU EventHub đã hiện thực hóa trọn vẹn 100% tất cả các hàm và kỹ thuật trọng tâm đã học trong chương trình Python Web (PWD301): "
        "từ Routing, Custom Template Filters (vnd, datetime_format, timeago), Context Processor, Form Validation với custom validator SĐT và MSSV của Lab 6, "
        "kỹ thuật phân quyền Parameterized Decorator @role_required của đề thi FPT Parking, cơ chế phân trang paginate() của SQLAlchemy ORM, "
        "cho đến bộ RESTful API v1 hoàn chỉnh đầy đủ mã HTTP Status Codes (200, 201, 204, 400, 401, 403, 404, 422) theo chuẩn Chương 9 và bài thi ParkTicket API!\n\n"
        "Tiếp theo đây, xin kính mời Thành viên 3 trình bày chi tiết về Kiến trúc MVC và Thiết kế cơ sở dữ liệu ERD của dự án!\""
    )
    r_s2.font.size = Pt(9.5)
    r_s2.font.italic = True

    # Q&A Member 2
    doc.add_paragraph().paragraph_format.space_before = Pt(8)
    doc.add_paragraph().add_run("❓ Bộ 3 câu hỏi vấn đáp trọng tâm cho Thành viên 2:").font.bold = True
    qa2 = [
        ("Tại sao các bạn lại sử dụng thư viện Bleach trong việc xử lý mô tả sự kiện?",
         "Dạ thưa cô, tính năng tạo sự kiện cho phép định dạng Markdown để bài viết phong phú. Nếu render trực tiếp mã HTML mà không kiểm duyệt, kẻ tấn công có thể chèn mã độc JavaScript như <script src='evil.js'> hoặc <img src=x onerror='stealData()'> để đánh cắp Cookie phiên đăng nhập của người khác (lỗ hổng Stored XSS). Thư viện Bleach đóng vai trò bộ lọc Whitelist nghiêm ngặt, chỉ cho phép các thẻ văn bản an toàn đi qua và tước bỏ toàn bộ mã độc hại ạ."),
        ("Làm thế nào Camera trên trình duyệt quét được mã QR mà không cần cài thêm ứng dụng App di động?",
         "Dạ chúng em khai thác WebRTC MediaDevices API chuẩn W3C trên các trình duyệt hiện đại (Chrome, Safari, Edge). JavaScript sẽ yêu cầu quyền camera (navigator.mediaDevices.getUserMedia) với chế độ ưu tiên camera sau (facingMode: 'environment'). Thư viện html5-qrcode quét luồng video thời gian thực, đọc chuỗi mã vé và gửi bất đồng bộ (Fetch API) về endpoint Flask /api/check-in/scan để xác thực mà không hề gây gián đoạn hay tải lại trang web ạ."),
        ("Nếu sinh viên đăng nhập trên máy tính công cộng ở trường, hệ thống có giải pháp gì bảo vệ phiên đăng nhập?",
         "Dạ hệ thống sử dụng Flask-Login quản lý Session an toàn trên Cookie với các cờ bảo vệ: HttpOnly để ngăn JavaScript truy cập cướp Cookie, và SameSite='Lax' để chống tấn công Cross-Site Request Forgery (CSRF). Đồng thời nút Đăng Xuất An Toàn xóa sạch Session trên máy tính ngay khi bấm ạ.")
    ]
    for q_i, (q_t, a_t) in enumerate(qa2, start=1):
        p_q = doc.add_paragraph()
        p_q.add_run(f"Câu {q_i}: {q_t}").font.bold = True
        p_a = doc.add_paragraph()
        p_a.add_run("👉 Trả lời mẫu: ").font.bold = True
        p_a.runs[0].font.color.rgb = SUCCESS
        p_a.add_run(f"\"{a_t}\"").font.size = Pt(9.5)

    # -------------------------------------------------------------
    # PHẦN 3: KIẾN TRÚC DỰ ÁN & THIẾT KẾ CƠ SỞ DỮ LIỆU
    # -------------------------------------------------------------
    doc.add_page_break()
    p3_h = doc.add_paragraph()
    r3_h = p3_h.add_run("PHẦN 3: KIẾN TRÚC DỰ ÁN & THIẾT KẾ CƠ SỞ DỮ LIỆU (THÀNH VIÊN 3: 18:30 – 27:00)")
    r3_h.font.size = Pt(13.5)
    r3_h.font.bold = True
    r3_h.font.color.rgb = NAVY
    p3_h.paragraph_format.space_before = Pt(12)
    p3_h.paragraph_format.space_after = Pt(4)

    doc.add_paragraph().add_run("3.1. Mô hình kiến trúc phần mềm MVC (Model - View - Controller):").font.bold = True
    mvc_desc = [
        ("Model (models.py):", "Định nghĩa 6 thực thể dữ liệu kế thừa từ SQLAlchemy Model, đóng gói các phương thức logic như hash password, kiểm tra vai trò người dùng, kiểm tra vé hợp lệ."),
        ("View (templates/ & static/):", "Tập hợp các template Jinja2 kế thừa từ base.html. Áp dụng CSS BEM, xử lý giao diện hiển thị linh hoạt theo vai trò người dùng (Sinh viên vs Cán bộ CTSV)."),
        ("Controller (app.py):", "Đảm nhiệm định tuyến (Routing), kiểm soát quyền truy cập bằng Decorators (@login_required, @admin_required), quản lý Transaction đặt vé và điều phối dữ liệu giữa Model và View.")
    ]
    for m_t, m_d in mvc_desc:
        bp = doc.add_paragraph(style='List Bullet')
        bp.add_run(m_t).font.bold = True
        bp.add_run(f" {m_d}")

    doc.add_paragraph().add_run("3.2. Sơ đồ thực thể CSDL (ERD Details - 6 Bảng dữ liệu):").font.bold = True
    erd_data = [
        ("Bảng roles:", "Lưu thông tin vai trò: id (PK), name (Student, Admin, Organizer), description."),
        ("Bảng users:", "Lưu tài khoản: id (PK), student_id (MSSV), full_name, email, password_hash, phone, avatar_url, role_id (FK)."),
        ("Bảng categories:", "Lưu danh mục: id (PK), name, slug, icon, color, description (5 danh mục hoạt động FPTU)."),
        ("Bảng events:", "Lưu thông tin sự kiện: id (PK), title, slug, venue, start_time, end_time, total_capacity, available_slots, status, category_id (FK), organizer_id (FK)."),
        ("Bảng tickets:", "Lưu vé điện tử: id (PK), ticket_code (Unique, e.g. FU-2026-AI001), qr_url, status (REGISTERED, CHECKED_IN, CANCELLED), registered_at, checked_in_at, event_id (FK), user_id (FK). Ràng buộc cascade='all, delete-orphan'."),
        ("Bảng reviews:", "Lưu đánh giá: id (PK), rating (1-5 sao), comment, created_at, event_id (FK), user_id (FK).")
    ]
    for e_t, e_d in erd_data:
        bp = doc.add_paragraph(style='List Bullet')
        bp.add_run(e_t).font.bold = True
        bp.add_run(f" {e_d}")

    doc.add_paragraph().add_run("3.3. Điểm nhấn kiến trúc: Cơ chế Dual-Database Switch:").font.bold = True
    p_dd = doc.add_paragraph()
    p_dd.add_run(
        "Hệ thống sở hữu giải pháp kiến trúc độc đáo: Tự động chuyển đổi giữa 2 hệ quản trị CSDL tùy theo môi trường triển khai:\n"
        "• Khi chạy Offline trên máy cục bộ / phòng thực hành: Kết nối Microsoft SQL Server qua ODBC Driver 17 theo đúng giáo trình môn học.\n"
        "• Khi deploy lên Cloud Vercel Serverless: Code tự động nhận diện biến môi trường VERCEL để chuyển sang SQLite Serverless tại /tmp, "
        "đảm bảo trang web chạy mượt mà 24/7 trên Internet mà không tốn chi phí thuê máy chủ riêng."
    )

    # Verbatim Script Member 3
    doc.add_paragraph().paragraph_format.space_before = Pt(8)
    doc.add_paragraph().add_run("🎙 Lời thoại thuyết trình mẫu Thành viên 3 (8.5 phút):").font.bold = True
    tbl_s3 = doc.add_table(rows=1, cols=1)
    tbl_s3.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_s3 = tbl_s3.rows[0].cells[0]
    set_cell_background(c_s3, "FFF7ED")
    set_cell_margins(c_s3, 100, 100, 140, 140)
    p_s3 = c_s3.paragraphs[0]
    r_s3 = p_s3.add_run(
        "\"Kính thưa quý thầy cô, em xin đại diện nhóm trình bày về cấu trúc mã nguồn MVC và thiết kế Cơ sở dữ liệu của FPTU EventHub.\n\n"
        "Dự án được tổ chức chặt chẽ theo chuẩn kiến trúc MVC:\n"
        "- Tầng Model (models.py): Định nghĩa 6 thực thể dữ liệu kế thừa từ SQLAlchemy ORM.\n"
        "- Tầng View (templates/ và static/): Chứa các khuôn mẫu Jinja2 HTML và mã giao diện, CSS Scoped.\n"
        "- Tầng Controller (app.py): Đảm nhận nhiệm vụ điều hướng, áp dụng các Decorator bảo vệ quyền truy cập (@login_required, @admin_required) và xử lý logic nghiệp vụ.\n\n"
        "Về Sơ đồ thực thể CSDL (ERD), chúng em thiết kế 6 bảng có mối quan hệ chặt chẽ:\n"
        "1. Bảng Role và User: Quan hệ 1 - N. Phân chia rõ ràng vai trò Student (Sinh viên) và Admin (Phòng CTSV).\n"
        "2. Bảng Category và Event: Quan hệ 1 - N. Phân loại sự kiện theo 5 nhóm hoạt động chuẩn của trường.\n"
        "3. Bảng Event và Ticket: Quan hệ 1 - N với ràng buộc cascade='all, delete-orphan'. Mỗi sự kiện có nhiều vé, và khi một sự kiện bị xóa thì các vé con được dọn dẹp sạch sẽ để không sinh ra dữ liệu rác.\n"
        "4. Bảng User và Ticket: Mỗi sinh viên sở hữu danh sách vé riêng, có trạng thái rõ ràng: REGISTERED (Đã giữ chỗ), CHECKED_IN (Đã điểm danh), hoặc CANCELLED (Đã hủy).\n"
        "5. Bảng Review: Cho phép sinh viên sau khi tham dự đánh giá số sao (1 đến 5 sao) và để lại nhận xét, giúp hệ thống tính điểm trung bình (Average Rating).\n\n"
        "Đặc biệt, một điểm sáng kỹ thuật trong đồ án của nhóm là Cơ Chế Dual-Database Switch:\n"
        "- Khi chạy cục bộ trên máy tính của sinh viên hoặc máy phòng thực hành của trường: Mã nguồn tự động kết nối Microsoft SQL Server qua ODBC Driver theo đúng chuẩn môn học CSDL.\n"
        "- Khi triển khai lên nền tảng đám mây Vercel Serverless: Code tự động nhận diện biến môi trường để chuyển sang SQLite Serverless tại thư mục /tmp. Nhờ giải pháp này, hệ thống vừa đáp ứng 100% chuẩn học thuật của trường, vừa có thể chạy mượt mà trên Internet toàn cầu mà không tốn chi phí thuê server đắt đỏ.\n\n"
        "Sau đây, xin mời Thành viên 4 thực hiện phần phân tích UseCase và Live Demo trực tiếp luồng trải nghiệm của Sinh viên!\""
    )
    r_s3.font.size = Pt(9.5)
    r_s3.font.italic = True

    # Q&A Member 3
    doc.add_paragraph().paragraph_format.space_before = Pt(8)
    doc.add_paragraph().add_run("❓ Bộ 3 câu hỏi vấn đáp trọng tâm cho Thành viên 3:").font.bold = True
    qa3 = [
        ("Trong CSDL, làm thế nào để đảm bảo 1 sinh viên không thể đặt 2 vé cho cùng 1 sự kiện?",
         "Dạ thưa thầy/cô, hệ thống bảo vệ ở 2 lớp: Ở tầng ứng dụng (Controller), trước khi tạo vé mới, code thực thi câu truy vấn kiểm tra Ticket.query.filter_by(user_id=current_user.id, event_id=event.id, status='REGISTERED').first(). Nếu đã tồn tại vé, hệ thống chặn ngay lập tức và chuyển hướng người dùng về trang Vé Của Tôi. Ở tầng giao diện, nút đăng ký tự động đổi thành nút màu xanh 'Xem Vé QR & Check-in' để sinh viên không bấm nhầm lần 2 ạ."),
        ("Cơ chế trừ số lượng ghế trống (Available Slots) khi đăng ký và hoàn lại khi hủy vé hoạt động ra sao?",
         "Dạ trong model Event có thuộc tính total_capacity và available_slots. Khi sinh viên bấm đăng ký, câu lệnh event.available_slots -= 1 được thực thi trong khối Transaction atomic db.session.commit(). Nếu có lỗi xảy ra, db.session.rollback() sẽ hoàn tác. Ngược lại, khi sinh viên hủy vé, trạng thái đổi sang CANCELLED và event.available_slots += 1 được cộng trả lại ngay lập tức để người khác có thể đăng ký ạ."),
        ("Tại sao các bạn lại dùng SQLAlchemy ORM thay vì viết các câu lệnh SQL thuần (Raw SQL)?",
         "Dạ thưa cô, SQLAlchemy ORM mang lại 3 lợi thế vượt trội: 1. Tự động phòng chống 100% lỗi SQL Injection nhờ cơ chế Parameterized Queries. 2. Tính trừu tượng hóa cao (Database Agnostic), giúp nhóm dễ dàng chuyển đổi qua lại giữa SQL Server và SQLite mà không phải sửa lại một dòng lệnh SQL nào. 3. Code Python rõ ràng, dễ bảo trì và mở rộng theo chuẩn công nghiệp ạ.")
    ]
    for q_i, (q_t, a_t) in enumerate(qa3, start=1):
        p_q = doc.add_paragraph()
        p_q.add_run(f"Câu {q_i}: {q_t}").font.bold = True
        p_a = doc.add_paragraph()
        p_a.add_run("👉 Trả lời mẫu: ").font.bold = True
        p_a.runs[0].font.color.rgb = SUCCESS
        p_a.add_run(f"\"{a_t}\"").font.size = Pt(9.5)

    # -------------------------------------------------------------
    # PHẦN 4: CHỨC NĂNG CHÍNH (MÔ TẢ BẰNG USECASE)
    # -------------------------------------------------------------
    doc.add_page_break()
    p4_h = doc.add_paragraph()
    r4_h = p4_h.add_run("PHẦN 4: CÁC CHỨC NĂNG CHÍNH CỦA HỆ THỐNG (MÔ TẢ BẰNG USECASE)")
    r4_h.font.size = Pt(13.5)
    r4_h.font.bold = True
    r4_h.font.color.rgb = NAVY
    p4_h.paragraph_format.space_before = Pt(12)
    p4_h.paragraph_format.space_after = Pt(4)

    doc.add_paragraph().add_run("4.1. Phân Hệ Sinh Viên (Student UseCases) — Thành Viên 4 (27:00 – 36:30):").font.bold = True
    
    uc_student = [
        ("UC01 - Xác thực Campus SSO:", "Sinh viên sử dụng email trường (@fpt.edu.vn / @fe.edu.vn) đăng nhập. Hệ thống bóc tách MSSV và tự động kích hoạt tài khoản."),
        ("UC02 - Live Search & Filter Sự Kiện:", "Tìm kiếm theo thời gian thực (tên sự kiện, diễn giả, hội trường) không cần tải lại trang; lọc theo 5 danh mục; chuyển đổi Grid/Timeline."),
        ("UC03 - Đặt Vé Giữ Chỗ Real-time:", "Sinh viên xem số ghế còn lại. Bấm 'Đăng Ký Giữ Chỗ Ngay', hệ thống trừ slot ghế atomic và tạo vé điện tử duy nhất."),
        ("UC04 - Quản Lý Ví Vé QR Cá Nhân:", "Trang 'Vé Của Tôi' hiển thị danh sách vé đã đặt. Modal phóng to mã QR sắc nét để sẵn sàng quét tại cửa hội trường."),
        ("UC05 - Hủy Vé 1-Click:", "Khi có việc bận, sinh viên bấm 'Hủy vé', trạng thái đổi sang CANCELLED và slot ghế tự động hoàn trả lại cho người khác."),
        ("UC06 - Đồng Bộ Google Calendar:", "Bấm 1 nút để tự động thêm ngày giờ, địa điểm hội trường vào ứng dụng Google Calendar trên điện thoại."),
        ("UC07 - Nhận & In E-Certificate:", "Sau khi được điểm danh check-in, nút 'Xem Giấy Chứng Nhận' kích hoạt, cho phép sinh viên xem và in chứng nhận chuẩn học thuật."),
        ("UC08 - Đánh Giá & Nhận Xét (Review):", "Đánh giá 1 đến 5 sao và gửi phản hồi chất lượng về công tác tổ chức sự kiện.")
    ]
    for u_t, u_d in uc_student:
        bp = doc.add_paragraph(style='List Bullet')
        bp.add_run(u_t).font.bold = True
        bp.add_run(f" {u_d}")

    # Verbatim Script Member 4
    doc.add_paragraph().paragraph_format.space_before = Pt(6)
    doc.add_paragraph().add_run("🎙 Lời thoại thuyết trình & Live Demo Thành viên 4 (9.5 phút):").font.bold = True
    tbl_s4 = doc.add_table(rows=1, cols=1)
    tbl_s4.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_s4 = tbl_s4.rows[0].cells[0]
    set_cell_background(c_s4, "FFF7ED")
    set_cell_margins(c_s4, 100, 100, 140, 140)
    p_s4 = c_s4.paragraphs[0]
    r_s4 = p_s4.add_run(
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
    )
    r_s4.font.size = Pt(9.5)
    r_s4.font.italic = True

    # Q&A Member 4
    doc.add_paragraph().paragraph_format.space_before = Pt(8)
    doc.add_paragraph().add_run("❓ Bộ 3 câu hỏi vấn đáp trọng tâm cho Thành viên 4:").font.bold = True
    qa4 = [
        ("Nếu sinh viên cố tình dùng công cụ Postman gửi yêu cầu đăng ký vào một sự kiện đã hết vé thì sao?",
         "Dạ thưa thầy/cô, hệ thống được bảo vệ vững chắc ở tầng Backend route /events/<id>/register. Trước khi thêm vé, mã nguồn kiểm tra if event.available_slots <= 0. Do đó, ngay cả khi bypass qua giao diện thì Server vẫn chặn đứng với thông báo từ chối, đảm bảo không thể xảy ra tình trạng vượt quá sức chứa hội trường ạ."),
        ("Làm thế nào tính năng Live Search có thể lọc nhanh như vậy mà không cần tải lại trang?",
         "Dạ tính năng này được xử lý hoàn toàn bằng Client-side JavaScript tối ưu. Mỗi thẻ sự kiện trên HTML được gắn các thuộc tính data-title, data-venue, data-category. Khi sinh viên gõ phím, sự kiện 'input' kích hoạt việc so sánh chuỗi bằng JavaScript và ẩn các phần tử không khớp bằng CSS display: none. Tốc độ phản hồi đạt mức tức thì mà không tạo bất kỳ tải nào cho máy chủ ạ."),
        ("Tính năng thêm sự kiện vào Google Calendar hoạt động như thế nào?",
         "Dạ chúng em xây dựng thuật toán tự động sinh đường dẫn Google Calendar Event Intent với các tham số chuẩn hóa: Tiêu đề (text), thời gian bắt đầu và kết thúc (dates theo định dạng UTC ISO), địa điểm hội trường (location) và nội dung tóm tắt. Khi sinh viên bấm vào, lịch Google trên điện thoại hoặc máy tính tự động mở ra và điền sẵn thông tin, giúp sinh viên không bị quên lịch sự kiện ạ.")
    ]
    for q_i, (q_t, a_t) in enumerate(qa4, start=1):
        p_q = doc.add_paragraph()
        p_q.add_run(f"Câu {q_i}: {q_t}").font.bold = True
        p_a = doc.add_paragraph()
        p_a.add_run("👉 Trả lời mẫu: ").font.bold = True
        p_a.runs[0].font.color.rgb = SUCCESS
        p_a.add_run(f"\"{a_t}\"").font.size = Pt(9.5)

    # 4.2. Phân Hệ Phòng CTSV UseCases (Thành Viên 5)
    doc.add_page_break()
    doc.add_paragraph().add_run("4.2. Phân Hệ Phòng Công Tác Sinh Viên (Admin/CTSV UseCases) — Thành Viên 5 (36:30 – 45:30):").font.bold = True
    
    uc_ctsv = [
        ("UC09 - Trung Tâm Quản Trị CTSV Dashboard:", "Theo dõi 4 thẻ KPI số liệu toàn trường: Tổng số sự kiện, Lượt vé phát hành, Lượt check-in thực tế, Danh sách tài khoản hoạt động gần đây."),
        ("UC10 - Đăng Tải Sự Kiện Cấp Trường:", "Khởi tạo sự kiện mới, nhập tiêu đề, danh mục, hội trường, thời gian, số lượng ghế tối đa và mô tả Markdown an toàn."),
        ("UC11 - Bảng Điều Hành Sự Kiện (Executive Panel):", "Tại trang chi tiết sự kiện, cán bộ không thấy nút đăng ký vé mà thấy Bảng Điều Hành CTSV để truy cập nhanh danh sách điểm danh và mở máy quét."),
        ("UC12 - Điểm Danh Bằng Camera Quét Mã QR (WebRTC):", "Sử dụng camera quét mã QR của sinh viên; hệ thống nhận diện trong 1 giây, phát âm thanh 'bíp', bắn pháo hoa và cập nhật trạng thái CHECKED_IN."),
        ("UC13 - Điểm Danh Thủ Công Dự Phòng:", "Hỗ trợ gõ trực tiếp mã vé (Ticket Code) để check-in khi màn hình điện thoại sinh viên bị nứt vỡ hoặc ánh sáng yếu."),
        ("UC14 - Quản Lý Điểm Danh & Xuất File Excel/CSV:", "Xem danh sách toàn bộ sinh viên đăng ký, lọc theo trạng thái và bấm 1 nút để xuất file CSV có UTF-8 BOM chuẩn tiếng Việt không lỗi font.")
    ]
    for u_t, u_d in uc_ctsv:
        bp = doc.add_paragraph(style='List Bullet')
        bp.add_run(u_t).font.bold = True
        bp.add_run(f" {u_d}")

    # Verbatim Script Member 5
    doc.add_paragraph().paragraph_format.space_before = Pt(6)
    doc.add_paragraph().add_run("🎙 Lời thoại thuyết trình & Live Demo Thành viên 5 (9.0 phút):").font.bold = True
    tbl_s5 = doc.add_table(rows=1, cols=1)
    tbl_s5.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_s5 = tbl_s5.rows[0].cells[0]
    set_cell_background(c_s5, "FFF7ED")
    set_cell_margins(c_s5, 100, 100, 140, 140)
    p_s5 = c_s5.paragraphs[0]
    r_s5 = p_s5.add_run(
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
    )
    r_s5.font.size = Pt(9.5)
    r_s5.font.italic = True

    # Q&A Member 5
    doc.add_paragraph().paragraph_format.space_before = Pt(8)
    doc.add_paragraph().add_run("❓ Bộ 3 câu hỏi vấn đáp trọng tâm cho Thành viên 5:").font.bold = True
    qa5 = [
        ("Làm thế nào để phân biệt rõ ràng giữa quyền hạn của Cán bộ CTSV và Sinh viên trên cùng một hệ thống?",
         "Dạ thưa thầy/cô, hệ thống áp dụng cơ chế Role-Based Access Control (RBAC) ở cả tầng Database lẫn tầng Middleware (Decorators trong Flask). Model User có thuộc tính is_admin. Các Route quản trị (/admin/dashboard, /organizer/events/<id>/attendees, /check-in) đều được bảo vệ bởi Custom Decorator @admin_required. Nếu sinh viên cố tình gõ link trên URL, hệ thống sẽ từ chối truy cập (HTTP 403) và chuyển hướng về trang chủ ạ."),
        ("Nếu tại cửa hội trường xảy ra sự cố mất mạng Internet thì quy trình check-in xử lý ra sao?",
         "Dạ thưa cô, chúng em đã chuẩn bị kịch bản dự phòng 2 tầng: Tầng 1: Cán bộ CTSV có thể mở hotspot phát 4G từ điện thoại cho thiết bị quét vì mỗi request check-in dạng JSON chỉ tiêu tốn vài kilobyte dữ liệu. Tầng 2: Ô check-in thủ công cho phép gõ trực tiếp mã vé dự phòng ngay cả khi camera gặp sự cố ánh sáng yếu ạ."),
        ("File CSV xuất ra có hỗ trợ đầy đủ tiếng Việt có dấu khi mở bằng Microsoft Excel trên Windows không?",
         "Dạ có thưa thầy/cô. Đây là lỗi kỹ thuật kinh điển khi xuất file CSV trên Windows (bị lỗi font Unicode cp1258). Để khắc phục triệt để, trong route /organizer/events/<id>/export-csv, chúng em đã chủ động ghi mã Byte Order Mark (UTF-8 BOM '\\ufeff') vào đầu luồng dữ liệu trước khi xuất dòng tiêu đề. Nhờ vậy, khi mở file bằng Microsoft Excel trên bất kỳ máy tính Windows nào, toàn bộ tên tiếng Việt có dấu như 'Trương Công Dũng', 'Nguyễn Việt Anh' đều hiển thị hoàn hảo 100% mà không bị lỗi font ạ.")
    ]
    for q_i, (q_t, a_t) in enumerate(qa5, start=1):
        p_q = doc.add_paragraph()
        p_q.add_run(f"Câu {q_i}: {q_t}").font.bold = True
        p_a = doc.add_paragraph()
        p_a.add_run("👉 Trả lời mẫu: ").font.bold = True
        p_a.runs[0].font.color.rgb = SUCCESS
        p_a.add_run(f"\"{a_t}\"").font.size = Pt(9.5)

    # -------------------------------------------------------------
    # PHẦN 5: CHECKLIST CHUẨN BỊ KỸ THUẬT PHÒNG THI
    # -------------------------------------------------------------
    doc.add_page_break()
    chk_h = doc.add_paragraph()
    chk_r = chk_h.add_run("PHẦN 5: CHECKLIST CHUẨN BỊ KỸ THUẬT TRƯỚC KHI BƯỚC VÀO PHÒNG BẢO VỆ")
    chk_r.font.size = Pt(13.5)
    chk_r.font.bold = True
    chk_r.font.color.rgb = NAVY
    chk_h.paragraph_format.space_before = Pt(12)
    chk_h.paragraph_format.space_after = Pt(4)

    checklist_items = [
        ("Kiểm tra kết nối mạng & Trang web Online:", "Mở sẵn link Vercel https://fptu-event-hub.vercel.app/ trên trình duyệt để đề phòng sự cố mạng nội bộ."),
        ("Chuẩn bị sẵn 2 Tab trình duyệt độc lập:", "• Tab 1: Đăng nhập sẵn tài khoản Sinh viên (dungtcde200433@fpt.edu.vn / pass123).\n• Tab 2 (Cửa sổ Ẩn danh / Profile khác): Đăng nhập sẵn tài khoản Cán bộ CTSV (ctsv.admin@fpt.edu.vn / pass123)."),
        ("Cấp quyền Camera cho Bàn Check-in:", "Trước khi thuyết trình, truy cập /organizer/check-in và bấm 'Cho phép (Allow)' quyền truy cập camera trên Chrome/Edge để khi demo không bị pop-up hỏi quyền làm gián đoạn."),
        ("Chuẩn bị sẵn 1 điện thoại mở mã QR:", "Dùng điện thoại cá nhân đăng nhập sinh viên, mở sẵn 1 vé sự kiện có mã QR trên màn hình để khi Thành viên 5 demo Camera thì đưa điện thoại lại gần laptop quét thử ngay trước mắt hội đồng."),
        ("Đồng hồ canh thời gian Presenter View:", "Bật chế độ Presenter View trên PowerPoint để luôn thấy thời gian đếm ngược, đảm bảo toàn đội dừng ở mốc 45 – 50 phút hoàn hảo.")
    ]

    for title, desc in checklist_items:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(f"{title} ").font.bold = True
        p.add_run(desc)

    doc.save(output_path)
    print(f"Full 4-Pillar Document created successfully at: {output_path}")

if __name__ == "__main__":
    out_file = r"C:\Users\truon\fptu_eventhub\KICH_BAN_THUYET_TRINH_FPTU_EVENTHUB_5_NGUOI.docx"
    create_presentation_document(out_file)
