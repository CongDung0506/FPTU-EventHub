# -*- coding: utf-8 -*-
"""
Script to generate the complete 26-slide PowerPoint presentation (.pptx)
for FPTU EventHub defense (45-50 minutes, 5 members),
strictly structured into the 6 requested sections:
1. Giới thiệu dự án
2. Phân công nhiệm vụ các thành viên
3. Tool quản lý dự án, cách lên kế hoạch dự án
4. Kiến trúc phần mềm, công nghệ sử dụng
5. Các tính năng chính của dự án
6. Phần kiểm thử (Testing & Security)
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation(output_path):
    prs = Presentation()
    # 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette
    BG_DARK = RGBColor(15, 23, 42)      # Slate 900
    CARD_BG = RGBColor(30, 41, 59)      # Slate 800
    PRIMARY = RGBColor(242, 111, 33)    # FPT Orange
    PRIMARY_LIGHT = RGBColor(254, 215, 170)
    SECONDARY = RGBColor(2, 132, 199)   # Sky Blue
    TEXT_LIGHT = RGBColor(248, 250, 252) # Slate 50
    TEXT_MUTED = RGBColor(148, 163, 184) # Slate 400
    ACCENT_GREEN = RGBColor(34, 197, 94) # Green 500

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, section_tag, title_text, presenter_text=""):
        # Dark Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()

        # Top Bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.12))
        bar.fill.solid()
        bar.fill.fore_color.rgb = PRIMARY
        bar.line.fill.background()

        # Section Tag & Presenter Tag
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.4))
        p = tb.text_frame.paragraphs[0]
        r1 = p.add_run()
        r1.text = section_tag.upper()
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = PRIMARY
        
        if presenter_text:
            r2 = p.add_run()
            r2.text = f"  |  🎤 {presenter_text}"
            r2.font.bold = False
            r2.font.size = Pt(11)
            r2.font.color.rgb = SECONDARY

        # Title
        tb_t = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.733), Inches(0.8))
        p_t = tb_t.text_frame.paragraphs[0]
        r_t = p_t.add_run()
        r_t.text = title_text
        r_t.font.bold = True
        r_t.font.size = Pt(24)
        r_t.font.color.rgb = TEXT_LIGHT

    def add_card(slide, left, top, width, height, title, items, badge="", border_color=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.5)
        else:
            card.line.color.rgb = RGBColor(51, 65, 85)
            card.line.width = Pt(1)

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        # Header of Card
        p_h = tf.paragraphs[0]
        if badge:
            r_b = p_h.add_run()
            r_b.text = f"[{badge}] "
            r_b.font.bold = True
            r_b.font.size = Pt(11)
            r_b.font.color.rgb = PRIMARY

        r_title = p_h.add_run()
        r_title.text = title
        r_title.font.bold = True
        r_title.font.size = Pt(16)
        r_title.font.color.rgb = TEXT_LIGHT

        # Items
        for item in items:
            p = tf.add_paragraph()
            p.space_before = Pt(8)
            p.level = 0
            
            if isinstance(item, tuple):
                bold_part, norm_part = item
                r_b = p.add_run()
                r_b.text = f"• {bold_part}: "
                r_b.font.bold = True
                r_b.font.size = Pt(12)
                r_b.font.color.rgb = PRIMARY_LIGHT
                
                r_n = p.add_run()
                r_n.text = norm_part
                r_n.font.size = Pt(12)
                r_n.font.color.rgb = TEXT_LIGHT
            else:
                r = p.add_run()
                r.text = f"• {item}"
                r.font.size = Pt(12)
                r.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 1: COVER
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = BG_DARK
    bg1.line.fill.background()

    # Accent decorative top-right shape
    accent1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.5), Inches(0.8), Inches(4.2), Inches(5.9))
    accent1.fill.solid()
    accent1.fill.fore_color.rgb = CARD_BG
    accent1.line.color.rgb = PRIMARY
    accent1.line.width = Pt(2)

    tb_acc = s1.shapes.add_textbox(Inches(8.8), Inches(1.2), Inches(3.6), Inches(5.1))
    tf_acc = tb_acc.text_frame
    tf_acc.word_wrap = True
    p_acc = tf_acc.paragraphs[0]
    p_acc.text = "THÔNG TIN BẢO VỆ ĐỒ ÁN"
    p_acc.runs[0].font.bold = True
    p_acc.runs[0].font.size = Pt(13)
    p_acc.runs[0].font.color.rgb = PRIMARY

    acc_items = [
        ("Thời lượng", "45 – 50 Phút báo cáo & vấn đáp"),
        ("Đội ngũ", "5 Thành viên (8-10 phút/thành viên)"),
        ("Môn học", "Lập trình Web với Python (PWD301)"),
        ("Live URL", "https://fptu-event-hub.vercel.app"),
        ("Mã nguồn", "GitHub /CongDung0506/FPTU-EventHub"),
        ("Điểm nổi bật", "100% Thuần ORM, WebRTC QR, Zero-SSO")
    ]
    for b_p, n_p in acc_items:
        p = tf_acc.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"{b_p}:\n"
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = SECONDARY
        r2 = p.add_run()
        r2.text = n_p
        r2.font.size = Pt(11.5)
        r2.font.color.rgb = TEXT_LIGHT

    # Title Box Left
    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(7.5), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    r_sub = p1.add_run()
    r_sub.text = "TRƯỜNG ĐẠI HỌC FPT — ĐỒ ÁN CHUYÊN NGÀNH CNTT\n"
    r_sub.font.bold = True
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = SECONDARY

    r_main = p1.add_run()
    r_main.text = "FPTU EVENTHUB\n"
    r_main.font.bold = True
    r_main.font.size = Pt(40)
    r_main.font.color.rgb = PRIMARY

    r_desc = p1.add_run()
    r_desc.text = "CỔNG QUẢN LÝ & ĐĂNG KÝ SỰ KIỆN SINH VIÊN ĐẠI HỌC FPT\n"
    r_desc.font.bold = True
    r_desc.font.size = Pt(17)
    r_desc.font.color.rgb = TEXT_LIGHT

    r_tag = p1.add_run()
    r_tag.text = "Hệ thống đặt vé giữ chỗ tức thì, Check-in bằng Camera WebRTC và cấp chứng nhận tự động\n\n"
    r_tag.font.size = Pt(13)
    r_tag.font.color.rgb = TEXT_MUTED

    r_auth = p1.add_run()
    r_auth.text = "Nhóm sinh viên thực hiện: Trương Công Dũng (Trưởng nhóm) cùng 4 thành viên"
    r_auth.font.bold = True
    r_auth.font.size = Pt(13)
    r_auth.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SECTION 1: GIỚI THIỆU DỰ ÁN (Slides 2 - 5)
    # =========================================================================
    # Slide 2: Bối Cảnh
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "1. Giới thiệu dự án", "Bối Cảnh Phong Trào Sinh Viên Tại Đại Học FPT", "Thành viên 1")
    add_card(s2, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0), "Môi Trường Năng Động", [
        ("30+ Câu lạc bộ", "Đa dạng các lĩnh vực học thuật, công nghệ, âm nhạc, kịch nghệ và thể thao."),
        ("Tần suất liên tục", "Hàng chục sự kiện, workshop, hackathon diễn ra mỗi tuần tại các cơ sở."),
        ("Quy mô bùng nổ", "Mỗi sự kiện thu hút từ 50 đến hơn 300 sinh viên đăng ký tham gia.")
    ], badge="BỐI CẢNH")
    add_card(s2, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0), "Địa Điểm Trọng Điểm", [
        ("Hội trường Alpha/Beta", "Không gian sự kiện quy mô lớn với sức chứa cố định từ 100 - 250 chỗ."),
        ("Phòng Lab AI & Robotics", "Sức chứa giới hạn chỉ 20 - 30 máy tính, đòi hỏi quản lý chỗ nghiêm ngặt."),
        ("Áp lực kiểm soát", "Yêu cầu hệ thống phải cập nhật số ghế trống chính xác theo thời gian thực.")
    ], badge="ĐỊA ĐIỂM")
    add_card(s2, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0), "Nhu Cầu Số Hóa", [
        ("Sinh viên thế hệ Gen Z", "Kỳ vọng trải nghiệm 1-click, dùng ngay email trường, có vé trên điện thoại."),
        ("Phòng CTSV & BTC", "Cần công cụ quản lý tập trung, loại bỏ danh sách giấy và báo cáo tự động."),
        ("Chuyển đổi số FPTU", "Chuẩn hóa quy trình tổ chức sự kiện học đường văn minh, hiện đại.")
    ], badge="CẤP THIẾT", border_color=PRIMARY)

    # Slide 3: Vấn Đề Của Cổng Cũ
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "1. Giới thiệu dự án", "Thách Thức & 'Nỗi Đau' Từ Cổng Cũ events.fptu.vn", "Thành viên 1")
    add_card(s3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.35), "1. Thiếu Cơ Chế Giữ Chỗ Tức Thì", [
        ("Google Form trung gian", "events.fptu.vn chỉ là bảng tin tĩnh, đăng ký phải dẫn link ra Google Form."),
        ("Vỡ trận sức chứa", "Form không tự khóa khi đủ 100 người, dẫn đến nhận 200 đơn gây quá tải hội trường.")
    ], badge="PAIN POINT 1", border_color=RGBColor(239, 68, 68))
    add_card(s3, Inches(6.8), Inches(1.8), Inches(5.6), Inches(2.35), "2. Điểm Danh Thủ Công Ùn Tắc", [
        ("Dò tên trên giấy", "Sinh viên đứng xếp hàng dài tại cửa hội trường để ban tổ chức dò từng MSSV."),
        ("Sai sót dữ liệu", "Dễ nhầm lẫn, mất danh sách và tốn từ 20 đến 30 phút chỉ để điểm danh.")
    ], badge="PAIN POINT 2", border_color=RGBColor(239, 68, 68))
    add_card(s3, Inches(0.8), Inches(4.45), Inches(5.6), Inches(2.35), "3. Không Có Vé Điện Tử Cá Nhân", [
        ("Không có mã định danh", "Sinh viên không có mã QR cá nhân để chứng minh đã đăng ký thành công."),
        ("Đặt chỗ ảo", "Sinh viên bận không có nút hủy vé, dẫn đến danh sách thì kín nhưng ghế ngồi lại trống.")
    ], badge="PAIN POINT 3", border_color=RGBColor(239, 68, 68))
    add_card(s3, Inches(6.8), Inches(4.45), Inches(5.6), Inches(2.35), "4. Chờ Đợi Giấy Chứng Nhận", [
        ("Quy trình chậm chạp", "Sinh viên phải chờ ban tổ chức thiết kế và gửi email chứng nhận sau nhiều tuần."),
        ("Mất động lực tham gia", "Không có hệ thống lưu trữ lịch sử tham gia sự kiện minh bạch.")
    ], badge="PAIN POINT 4", border_color=RGBColor(239, 68, 68))

    # Slide 4: Sứ Mệnh & Mục Tiêu FPTU EventHub
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "1. Giới thiệu dự án", "Sứ Mệnh & Mục Tiêu Cốt Lõi Của FPTU EventHub", "Thành viên 1")
    add_card(s4, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0), "Tự Động Hóa 100%", [
        ("Zero-Registration SSO", "Nhận diện tức thì FPT Mail (@fpt.edu.vn / @fe.edu.vn), không cần đăng ký."),
        ("Đặt vé Atomic 0.1s", "Kiểm soát số lượng ghế thực, ngăn chặn triệt để đặt trùng (Double Booking)."),
        ("Tự động hoàn vé", "Sinh viên hủy vé 1-click, trả lại slot ghế trống tức thì cho bạn khác.")
    ], badge="TRẢI NGHIỆM")
    add_card(s4, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0), "Số Hóa Điểm Danh", [
        ("WebRTC Camera Scanner", "Quét mã QR trực tiếp trên trình duyệt máy tính và điện thoại dưới 1 giây."),
        ("Không cài thêm App", "Hoạt động mượt mà trên nền Web, tương thích mọi hệ điều hành iOS/Android."),
        ("Chống gian lận", "Mỗi vé có QR Hash duy nhất, tự khóa trạng thái ngay sau lần quét đầu tiên.")
    ], badge="VẬN HÀNH")
    add_card(s4, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0), "Quản Trị Tập Trung", [
        ("Phân quyền 2 phân hệ", "Tách biệt luồng Sinh viên (khám phá/vé) và Cán bộ CTSV (điều hành/thống kê)."),
        ("Dashboard trực quan", "Thống kê tỷ lệ lấp đầy, số vé phát hành và số lượt có mặt thực tế."),
        ("Xuất báo cáo 1-click", "Xuất file CSV/Excel chuẩn UTF-8 BOM lưu trữ văn thư cho nhà trường.")
    ], badge="QUẢN TRỊ", border_color=PRIMARY)

    # Slide 5: Bảng So Sánh Đột Phá
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "1. Giới thiệu dự án", "Bảng So Sánh Đột Phá: FPTU EventHub vs Cổng Cũ", "Thành viên 1")
    add_card(s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Cổng Cũ: events.fptu.vn", [
        ("Đăng nhập", "Biểu mẫu riêng hoặc phụ thuộc vào tài khoản nội bộ rời rạc."),
        ("Giữ chỗ", "Dẫn link sang Google Form, không giới hạn tự động sức chứa."),
        ("Vé tham dự", "Không có vé điện tử, chỉ gửi email xác nhận văn bản thô."),
        ("Điểm danh", "Thủ công bằng danh sách giấy hoặc dò MSSV bằng mắt thường."),
        ("Hủy vé", "Không có tính năng hủy vé, dẫn đến ghế ảo rất nhiều."),
        ("Chứng nhận", "Chờ thiết kế gửi email thủ công sau 2 - 3 tuần.")
    ], badge="TRUYỀN THỐNG", border_color=RGBColor(239, 68, 68))
    add_card(s5, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "FPTU EventHub (Hệ Thống Mới)", [
        ("Đăng nhập", "Zero-SSO 1-click nhận diện FPT Mail (@fpt.edu.vn / @fe.edu.vn)."),
        ("Giữ chỗ", "Transaction nguyên tử, tự khóa nút ĐÃ HẾT VÉ khi kín chỗ."),
        ("Vé tham dự", "Vé điện tử kèm mã QR động độc bản có chữ ký số xác thực."),
        ("Điểm danh", "WebRTC Camera QR Scanner giải mã tức thì dưới 1 giây."),
        ("Hủy vé", "Hủy vé 1-click, hệ thống tự động hoàn ghế cho sinh viên khác."),
        ("Chứng nhận", "Cấp Giấy chứng nhận điện tử (E-Cert) tự động ngay khi check-in.")
    ], badge="ĐỘT PHÁ MỚI", border_color=ACCENT_GREEN)

    # =========================================================================
    # SECTION 2: PHÂN CÔNG NHIỆM VỤ CÁC THÀNH VIÊN (Slides 6 - 8)
    # =========================================================================
    # Slide 6: Ma Trận Phân Công 5 Thành Viên
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "2. Phân công nhiệm vụ", "Ma Trận Phân Công Nhiệm Vụ 5 Thành Viên (100% Đóng Góp)", "Thành viên 2")
    add_card(s6, Inches(0.8), Inches(1.8), Inches(2.2), Inches(5.0), "Trương Công Dũng", [
        ("Vai trò", "Trưởng nhóm / Lead Full-Stack"),
        ("Nhiệm vụ", "Khởi tạo kiến trúc MVC, tích hợp Flask, cấu hình CSDL Dual-Database, Zero-SSO, Vercel Serverless."),
        ("Đóng góp", "20% (Chịu trách nhiệm tổng thể)")
    ], badge="MEMBER 1")
    add_card(s6, Inches(3.2), Inches(1.8), Inches(2.2), Inches(5.0), "Thành Viên 2", [
        ("Vai trò", "Backend & Security Lead"),
        ("Nhiệm vụ", "Triển khai xác thực Werkzeug PBKDF2, màng lọc XSS Bleach, custom validators (Phone, MSSV), CSRF."),
        ("Đóng góp", "20% (Module Bảo Mật)")
    ], badge="MEMBER 2")
    add_card(s6, Inches(5.6), Inches(1.8), Inches(2.2), Inches(5.0), "Thành Viên 3", [
        ("Vai trò", "Database & ORM Architect"),
        ("Nhiệm vụ", "Thiết kế ERD 6 bảng, migration SQL Server/SQLite, Transaction đặt vé, phân trang paginate, to_dict()."),
        ("Đóng góp", "20% (Module CSDL)")
    ], badge="MEMBER 3")
    add_card(s6, Inches(8.0), Inches(1.8), Inches(2.2), Inches(5.0), "Thành Viên 4", [
        ("Vai trò", "Frontend & UI/UX Developer"),
        ("Nhiệm vụ", "Thiết kế giao diện Dark Tech, CSS Scoped BEM, responsive mobile, tích hợp QR Scanner WebRTC."),
        ("Đóng góp", "20% (Module Giao Diện)")
    ], badge="MEMBER 4")
    add_card(s6, Inches(10.4), Inches(1.8), Inches(2.2), Inches(5.0), "Thành Viên 5", [
        ("Vai trò", "QA / Tester & CTSV Flow"),
        ("Nhiệm vụ", "Xây dựng bộ 15 Unit Tests, kiểm thử bảo mật, xây dựng dashboard CTSV và xuất báo cáo CSV."),
        ("Đóng góp", "20% (Kiểm Thử & CTSV)")
    ], badge="MEMBER 5")

    # Slide 7: Cơ Chế Phối Hợp & Giao Tiếp
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "2. Phân công nhiệm vụ", "Cơ Chế Phối Hợp, Giao Tiếp & Kiểm Soát Tiến Độ Nhóm", "Thành viên 2")
    add_card(s7, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0), "Giao Tiếp & Đồng Bộ", [
        ("Daily Standup 15 Phút", "Họp trực tuyến ngắn mỗi tối cập nhật 3 câu hỏi: Đã làm gì? Sẽ làm gì? Có vướng mắc gì?"),
        ("Kênh trao đổi riêng", "Nhóm Discord & Zalo phân luồng chuyên trách: #backend, #frontend, #bugs-issue."),
        ("Biên bản cuộc họp", "Lưu trữ nội dung thống nhất sau mỗi buổi thảo luận trên Notion.")
    ], badge="GIAO TIẾP")
    add_card(s7, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0), "Code Review Chéo", [
        ("Quy tắc 2 Reviewers", "Mỗi Pull Request bắt buộc có ít nhất 2 thành viên review code trước khi merge vào main."),
        ("Kiểm thử tự động", "Chạy test suite tự động trước khi chấp thuận tích hợp mã nguồn."),
        ("Chuẩn hóa Code Style", "Tuân thủ nghiêm ngặt tiêu chuẩn PEP8 cho Python và BEM cho CSS.")
    ], badge="CHẤT LƯỢNG")
    add_card(s7, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0), "Quản Trị Rủi Ro", [
        ("Kế hoạch dự phòng (Backup)", "Mỗi phân hệ có 1 thành viên chính (Primary) và 1 thành viên dự phòng (Shadow)."),
        ("Giải quyết xung đột", "Trưởng nhóm có thẩm quyền quyết định cuối cùng khi có bất đồng quan điểm thiết kế."),
        ("Cam kết Deadline", "Hoàn thành trước mốc thời gian 48 tiếng để có thời gian diễn tập và fix bug.")
    ], badge="RỦI RO", border_color=PRIMARY)

    # Slide 8: Kế Hoạch Đào Tạo & Chia Sẻ Kiến Thức
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "2. Phân công nhiệm vụ", "Chia Sẻ Tri Thức Kỹ Thuật (Knowledge Sharing)", "Thành viên 2")
    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Chuyên Đề Nội Bộ Nhóm", [
        ("Workshop 1: Làm chủ Gitflow", "Hướng dẫn phân nhánh, tạo PR, giải quyết merge conflicts và rebase an toàn."),
        ("Workshop 2: SQLAlchemy ORM", "Chia sẻ kỹ thuật tối ưu truy vấn, quan hệ cascade, eager loading và transaction."),
        ("Workshop 3: WebRTC & Camera QR", "Nguyên lý hoạt động của luồng video MediaDevices và cách giải mã QR trên trình duyệt.")
    ], badge="ĐÀO TẠO")
    add_card(s8, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Hiệu Quả Đạt Được", [
        ("100% Hiểu sâu dự án", "Tất cả 5 thành viên đều nắm rõ luồng dữ liệu tổng thể và có thể tự tin phản biện trước Hội đồng."),
        ("Không phụ thuộc cá nhân", "Bất kỳ thành viên nào cũng có thể hỗ trợ sửa lỗi hoặc demo tính năng thay nhau."),
        ("Kỷ luật & Tinh thần đồng đội", "Dự án hoàn thành đúng hạn 100% các cam kết đề ra mà không bị chậm tiến độ.")
    ], badge="KẾT QUẢ", border_color=ACCENT_GREEN)

    # =========================================================================
    # SECTION 3: TOOL QUẢN LÝ DỰ ÁN & CÁCH LÊN KẾ HOẠCH (Slides 9 - 12)
    # =========================================================================
    # Slide 9: Bộ Tool Quản Lý Dự Án
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "3. Quản lý dự án", "Hệ Sinh Thái Công Cụ Quản Lý & Vận Hành Dự Án", "Thành viên 2")
    add_card(s9, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0), "GitHub Projects & Issues", [
        ("Bảng Kanban trực quan", "Quản lý luồng công việc 4 cột: Backlog, To Do, In Progress, Done."),
        ("Gắn thẻ nhãn (Labels)", "Phân loại rõ ràng: Feature, Bug, Documentation, Security, Priority-High."),
        ("Liên kết Commit & PR", "Mỗi Issue gắn liền với commit ID cụ thể để dễ đối chiếu lịch sử.")
    ], badge="TASK MANAGEMENT", border_color=PRIMARY)
    add_card(s9, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0), "Git & GitHub Repository", [
        ("Quản lý phiên bản", "Lưu trữ mã nguồn an toàn tại CongDung0506/FPTU-EventHub."),
        ("Bảo vệ nhánh main", "Chặn commit trực tiếp vào main, bắt buộc mở Pull Request."),
        ("Lịch sử minh bạch", "Ghi nhận đầy đủ từng commit của tất cả các thành viên trong nhóm.")
    ], badge="VERSION CONTROL")
    add_card(s9, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0), "Tài Liệu & Báo Cáo", [
        ("Notion & Google Drive", "Lưu trữ tài liệu thiết kế UseCase, sơ đồ CSDL và biên bản kiểm thử."),
        ("Microsoft Word Automation", "Script Python tự động tạo báo cáo DOCX chuẩn học thuật."),
        ("Postman Workspace", "Lưu trữ và chia sẻ bộ test collection cho RESTful API.")
    ], badge="DOCUMENTATION")

    # Slide 10: Quy Trình Lập Kế Hoạch Agile Scrum
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "3. Quản lý dự án", "Quy Trình Lập Kế Hoạch & Triển Khai Theo Agile Scrum", "Thành viên 2")
    add_card(s10, Inches(0.8), Inches(1.8), Inches(2.7), Inches(5.0), "Sprint 1: Phân Tích", [
        ("Thời gian", "Tuần 1"),
        ("Mục tiêu", "Khảo sát cổng cũ events.fptu.vn, xác định Pain Points, phác thảo Wireframe và thiết kế ERD 6 bảng."),
        ("Kết quả", "Đặc tả yêu cầu SRS và CSDL.")
    ], badge="SPRINT 1")
    add_card(s10, Inches(3.7), Inches(1.8), Inches(2.7), Inches(5.0), "Sprint 2: Backend Core", [
        ("Thời gian", "Tuần 2"),
        ("Mục tiêu", "Xây dựng ORM Models, xác thực Zero-SSO, thuật toán giữ chỗ Atomic Transaction, phân quyền RBAC."),
        ("Kết quả", "Hoàn thành 100% logic đặt vé.")
    ], badge="SPRINT 2")
    add_card(s10, Inches(6.6), Inches(1.8), Inches(2.7), Inches(5.0), "Sprint 3: UI & WebRTC", [
        ("Thời gian", "Tuần 3"),
        ("Mục tiêu", "Thiết kế giao diện Dark Tech, responsive mobile, nhúng Camera QR Scanner, xuất báo cáo CSV."),
        ("Kết quả", "Giao diện web hoàn chỉnh.")
    ], badge="SPRINT 3")
    add_card(s10, Inches(9.5), Inches(1.8), Inches(2.7), Inches(5.0), "Sprint 4: Test & Deploy", [
        ("Thời gian", "Tuần 4"),
        ("Mục tiêu", "Xây dựng bộ 15 Unit Tests, kiểm thử bảo mật XSS/Redirect, deploy Vercel Serverless, viết tài liệu."),
        ("Kết quả", "Dự án sẵn sàng bảo vệ.")
    ], badge="SPRINT 4", border_color=ACCENT_GREEN)

    # Slide 11: Git Workflow & Phân Nhánh
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "3. Quản lý dự án", "Chiến Lược Phân Nhánh Mã Nguồn (Git Workflow)", "Thành viên 2")
    add_card(s11, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Cấu Trúc Nhánh Nghiêm Ngặt", [
        ("Nhánh main", "Chỉ chứa mã nguồn ổn định nhất, tự động kích hoạt CI/CD deploy lên Vercel Production."),
        ("Nhánh develop", "Nơi tích hợp các tính năng mới sau khi đã test nội bộ thành công."),
        ("Nhánh feature/*", "Mỗi tính năng được tạo trên một nhánh riêng (e.g. feature/qr-scanner, feature/category-crud)."),
        ("Nhánh bugfix/*", "Xử lý nhanh các vấn đề phát sinh được phát hiện trong quá trình kiểm thử.")
    ], badge="BRANCHING")
    add_card(s11, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Quy Ước Commit Chuẩn Conventional", [
        ("feat: ...", "Dành cho các tính năng mới (e.g. feat: add camera qr check-in)."),
        ("fix: ...", "Dành cho việc sửa lỗi (e.g. fix: resolve capacity double booking)."),
        ("docs: ...", "Cập nhật tài liệu, slide, báo cáo Word (e.g. docs: update slide deck)."),
        ("test: ...", "Bổ sung hoặc sửa đổi các bài unit test tự động."),
        ("refactor: ...", "Tối ưu cấu trúc mã nguồn mà không làm đổi hành vi hệ thống.")
    ], badge="CONVENTIONS", border_color=PRIMARY)

    # Slide 12: Biểu Đồ Gantt & Tiến Độ Thực Tế
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "3. Quản lý dự án", "Tiến Độ Triển Khai Thực Tế & Đánh Giá Milestone", "Thành viên 2")
    add_card(s12, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Các Mốc Đạt Được (Milestones)", [
        ("M1: Phê Duyệt Đề Tài", "Được giảng viên thông qua đề tài FPTU EventHub và kiến trúc tổng quan."),
        ("M2: Nguyên Mẫu CSDL & Auth", "Hoàn thành kết nối MS SQL Server, đăng nhập FPT Mail và hash password."),
        ("M3: Nghiệp Vụ Giữ Chỗ & QR", "Hiện thực thành công giải thuật giữ chỗ không nghẽn và giải mã QR Camera."),
        ("M4: Kiểm Thử Toàn Diện", "Đạt 15/15 Unit Tests Passed và loại bỏ 100% lỗ hổng bảo mật."),
        ("M5: Triển Khai Cloud Vercel", "Chạy trực tiếp trên Internet tại fptu-event-hub.vercel.app.")
    ], badge="MILESTONES", border_color=ACCENT_GREEN)
    add_card(s12, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Đánh Giá Hiệu Suất Nhóm", [
        ("Đúng hạn 100%", "Mọi tác vụ trên bảng GitHub Projects đều được hoàn thành trước thời hạn."),
        ("Tỷ lệ lỗi phát sinh thấp", "Nhờ áp dụng cơ chế code review và unit test từ sớm."),
        ("Sự phối hợp nhịp nhàng", "Không xảy ra xung đột mã nguồn lớn nhờ tuân thủ kỷ luật Gitflow."),
        ("Sẵn sàng bảo vệ", "Sản phẩm thực tế hoạt động trơn tru, tài liệu báo cáo đầy đủ, chuẩn chỉnh.")
    ], badge="HIỆU SUẤT")

    # =========================================================================
    # SECTION 4: KIẾN TRÚC PHẦN MỀM & CÔNG NGHỆ SỬ DỤNG (Slides 13 - 17)
    # =========================================================================
    # Slide 13: Mô Hình MVC
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "4. Kiến trúc & Công nghệ", "Mô Hình Kiến Trúc Phần Mềm MVC (Model - View - Controller)", "Thành viên 3")
    add_card(s13, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0), "Model (models.py)", [
        ("Kế thừa SQLAlchemy Model", "Định nghĩa 6 thực thể dữ liệu quan hệ, quan hệ khóa ngoại và ràng buộc cascade."),
        ("Đóng gói logic nghiệp vụ", "Phương thức hash mật khẩu, kiểm tra sức chứa, tính điểm đánh giá trung bình."),
        ("Serialization to_dict()", "Chuẩn hóa dữ liệu sang JSON phục vụ cho hệ thống RESTful API.")
    ], badge="MODEL", border_color=SECONDARY)
    add_card(s13, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0), "View (templates/ & static/)", [
        ("Jinja2 Template Engine", "Server-Side Rendering (SSR) giúp tải trang ban đầu cực nhanh và chuẩn SEO."),
        ("Scoped CSS (BEM standard)", "Giao diện Dark Modern Tech, chia khối độc lập, không bị xung đột style."),
        ("Dynamic UI & Dark Theme", "Chuyển đổi giao diện Sáng / Tối mượt mà lưu trạng thái tại LocalStorage.")
    ], badge="VIEW", border_color=PRIMARY)
    add_card(s13, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0), "Controller (app.py)", [
        ("Điều phối Routing", "Xử lý toàn bộ các yêu cầu HTTP (GET, POST, PUT, DELETE) gửi từ Client."),
        ("Security Guards", "Áp dụng các Decorator phân quyền (@login_required, @admin_required, @role_required)."),
        ("Transaction Management", "Quản lý đóng/mở phiên CSDL, thực thi commit an toàn và rollback khi có lỗi.")
    ], badge="CONTROLLER", border_color=ACCENT_GREEN)

    # Slide 14: Vòng Đời HTTP Request
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "4. Kiến trúc & Công nghệ", "Vòng Đời Xử Lý HTTP Request & Màng Lọc Bảo Mật", "Thành viên 3")
    add_card(s14, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Quy Trình 6 Bước Xử Lý Yêu Cầu", [
        ("Bước 1: Client Request", "Sinh viên/Cán bộ gửi request từ trình duyệt lên Vercel Edge Serverless."),
        ("Bước 2: WSGI Handler", "Vercel chuyển tiếp request qua Flask Application WSGI."),
        ("Bước 3: RBAC & Auth Guard", "Kiểm tra Session Cookie, cờ đăng nhập và thẩm quyền vai trò của người dùng."),
        ("Bước 4: Router & Controller", "Điều hướng đến hàm xử lý tương ứng trong app.py."),
        ("Bước 5: ORM & Database", "Thực thi truy vấn thông qua SQLAlchemy ORM đến SQL Server hoặc SQLite."),
        ("Bước 6: Render & Response", "Render Jinja2 template hoặc trả về JSON API kèm mã trạng thái HTTP chuẩn.")
    ], badge="LIFECYCLE")
    add_card(s14, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Màng Lọc Bảo Mật 3 Lớp", [
        ("Lớp 1: Endpoint Guard", "Chặn đứng người chưa đăng nhập bằng @app.before_request trừ các trang công khai."),
        ("Lớp 2: Role Authorization", "Custom Decorator @role_required ngăn chặn sinh viên can thiệp vào trang CTSV."),
        ("Lớp 3: Input Sanitization", "Bleach làm sạch toàn bộ văn bản Markdown, tước bỏ các script tấn công XSS."),
        ("Cơ chế Fail-safe", "Nếu có bất kỳ lỗi ngoại lệ nào, hệ thống tự động rollback transaction và trả về trang lỗi 500.")
    ], badge="SECURITY", border_color=RGBColor(239, 68, 68))

    # Slide 15: Sơ Đồ Thực Thể CSDL ERD
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "4. Kiến trúc & Công nghệ", "Thiết Kế Cơ Sở Dữ Liệu ERD (6 Bảng Chuẩn Hóa)", "Thành viên 3")
    add_card(s15, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.35), "1. Phân Hệ Người Dùng & Vai Trò", [
        ("roles", "id (PK), name (Student, Admin, Organizer), description."),
        ("users", "id (PK), student_id (MSSV), full_name, email, password_hash, phone, avatar_url, role_id (FK).")
    ], badge="AUTH DATA")
    add_card(s15, Inches(6.8), Inches(1.8), Inches(5.6), Inches(2.35), "2. Phân Hệ Sự Kiện & Phân Loại", [
        ("categories", "id (PK), name, slug, icon, color, description (5 danh mục FPTU)."),
        ("events", "id (PK), title, slug, venue, start_time, end_time, total_capacity, available_slots, status, category_id (FK), organizer_id (FK).")
    ], badge="EVENT DATA")
    add_card(s15, Inches(0.8), Inches(4.45), Inches(5.6), Inches(2.35), "3. Vé Điện Tử & Check-in", [
        ("tickets", "id (PK), ticket_code (Unique, e.g. FU-2026-X89AD), qr_url, status (REGISTERED, CHECKED_IN, CANCELLED), registered_at, checked_in_at, event_id (FK), user_id (FK)."),
        ("Cascade delete", "Ràng buộc cascade='all, delete-orphan' dọn sạch vé rác khi xóa sự kiện.")
    ], badge="TICKET DATA", border_color=PRIMARY)
    add_card(s15, Inches(6.8), Inches(4.45), Inches(5.6), Inches(2.35), "4. Phản Hồi & Đánh Giá Chất Lượng", [
        ("reviews", "id (PK), rating (1-5 sao), comment, created_at, event_id (FK), user_id (FK)."),
        ("Điểm trung bình", "Tự động tính Average Rating phục vụ cho sinh viên tham khảo uy tín sự kiện.")
    ], badge="FEEDBACK DATA")

    # Slide 16: Cơ Chế Dual-Database Switch
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "4. Kiến trúc & Công nghệ", "Điểm Sáng Kỹ Thuật: Cơ Chế Dual-Database Switch", "Thành viên 3")
    add_card(s16, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Môi Trường Localhost / Phòng Lab", [
        ("Hệ quản trị CSDL", "Microsoft SQL Server thông qua ODBC Driver 17."),
        ("Chuẩn học thuật PWD301", "Đáp ứng 100% chuẩn cấu hình bài giảng và các kỳ thi thực hành của Đại học FPT."),
        ("Kết nối tự động", "Mã nguồn thử kết nối SQL Server cục bộ trước, nếu phát hiện có driver sẽ tự động kết nối qua chuỗi mssql+pyodbc.")
    ], badge="LOCAL ENTERPRISE", border_color=SECONDARY)
    add_card(s16, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Môi Trường Cloud (Vercel Serverless)", [
        ("Hệ quản trị CSDL", "SQLite Serverless được cấp phát động trong thư mục /tmp."),
        ("Nhận diện thông minh", "Code tự động kiểm tra biến môi trường VERCEL / AWS_LAMBDA để kích hoạt SQLite."),
        ("Lợi ích vượt trội", "Chạy mượt mà 24/7 trên Internet toàn cầu, không tốn bất kỳ chi phí thuê server riêng, tự động seed dữ liệu mẫu.")
    ], badge="CLOUD PRODUCTION", border_color=ACCENT_GREEN)

    # Slide 17: Hệ Sinh Thái Công Nghệ Cốt Lõi
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "4. Kiến trúc & Công nghệ", "Hệ Sinh Thái Công Nghệ & Thư Viện Chuyên Dụng", "Thành viên 3")
    add_card(s17, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0), "Backend & ORM", [
        ("Python 3.11 / 3.14", "Ngôn ngữ chủ đạo, cú pháp hiện đại, tối ưu hiệu năng."),
        ("Flask Microframework", "Linh hoạt, nhẹ, dễ mở rộng và kiểm soát toàn bộ luồng xử lý."),
        ("SQLAlchemy 2.0", "ORM chuẩn hóa, bảo vệ 100% khỏi tấn công SQL Injection.")
    ], badge="BACKEND")
    add_card(s17, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0), "Bảo Mật & Kiểm Thực", [
        ("Bleach HTML Sanitizer", "Loại bỏ mã độc Stored XSS trong nội dung mô tả Markdown."),
        ("Werkzeug Security", "Mã hóa mật khẩu bằng thuật toán PBKDF2 phối hợp SHA-256 kèm Salt."),
        ("Flask-WTF CSRFProtect", "Bảo vệ form bằng CSRF Token và bộ custom validators.")
    ], badge="SECURITY", border_color=RGBColor(239, 68, 68))
    add_card(s17, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0), "Tương Tác & Real-Time", [
        ("html5-qrcode", "Quét mã QR bằng Camera qua WebRTC MediaDevices API."),
        ("Canvas Confetti", "Hiệu ứng pháo hoa chúc mừng check-in thành công."),
        ("Google Calendar API", "Tạo liên kết đồng bộ lịch sự kiện cá nhân chỉ bằng 1-click.")
    ], badge="INTERACTION", border_color=PRIMARY)

    # =========================================================================
    # SECTION 5: CÁC TÍNH NĂNG CHÍNH CỦA DỰ ÁN (Slides 18 - 22)
    # =========================================================================
    # Slide 18: Phân Hệ Sinh Viên: Khám Phá & Đăng Nhập
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "5. Tính năng chính", "Phân Hệ Sinh Viên: Zero-SSO & Khám Phá Đa Chiều", "Thành viên 4")
    add_card(s18, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "1. Đăng Nhập Zero-Registration SSO", [
        ("Chỉ chấp nhận Email FPT", "Kiểm thực chặt chẽ tên miền @fpt.edu.vn hoặc @fe.edu.vn."),
        ("Tự động trích xuất MSSV", "Hệ thống tự bóc tách MSSV từ email (e.g. dungtcde200433 -> DE200433) và kích hoạt tài khoản tức thì."),
        ("Nút 1-Click Demo", "Hỗ trợ chấm điểm nhanh cho Hội đồng với tài khoản Sinh viên và Cán bộ CTSV.")
    ], badge="UC01: AUTHENTICATION")
    add_card(s18, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "2. Khám Phá Sự Kiện Đa Chiều", [
        ("Instant Search", "Tìm kiếm tức thì theo tiêu đề sự kiện, tên diễn giả hoặc tên hội trường."),
        ("Bộ lọc 5 danh mục", "Phân loại Công nghệ, Học thuật, Kỹ năng mềm, Văn hóa CLB, Thể thao."),
        ("Phân trang Paginate", "Áp dụng SQLAlchemy paginate() phân trang 6 sự kiện/trang giúp tải nhanh."),
        ("Countdown Timer", "Đồng hồ đếm ngược thời gian thực đến sự kiện nổi bật gần nhất.")
    ], badge="UC02: DISCOVERY", border_color=PRIMARY)

    # Slide 19: Phân Hệ Sinh Viên: Giữ Chỗ & Ví Vé QR
    s19 = prs.slides.add_slide(blank_layout)
    add_header(s19, "5. Tính năng chính", "Phân Hệ Sinh Viên: Đặt Vé Atomic & Ví Vé QR Cá Nhân", "Thành viên 4")
    add_card(s19, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "3. Đặt Vé Atomic & Hủy Vé 1-Click", [
        ("Thuật toán Transaction", "Kiểm tra sức chứa còn trống và trừ slot trong một giao dịch an toàn, chống overbooking."),
        ("Chặn đăng ký trùng lặp", "Mỗi sinh viên chỉ được đặt tối đa 1 vé cho mỗi sự kiện."),
        ("Tự động hoàn ghế", "Khi sinh viên bấm Hủy vé, hệ thống tự động cộng lại slot ghế trống cho bạn khác.")
    ], badge="UC03 & UC05: BOOKING", border_color=ACCENT_GREEN)
    add_card(s19, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "4. Ví Vé QR & Giấy Chứng Nhận E-Cert", [
        ("Ví 'Vé Của Tôi'", "Quản lý toàn bộ vé đã đăng ký, vé đã tham dự và vé đã hủy."),
        ("Mã QR cá nhân hóa", "Mỗi vé đi kèm mã QR chuẩn FU-2026-XXXXXX hiển thị sắc nét trên điện thoại."),
        ("Giấy chứng nhận E-Cert", "Sau khi check-in thành công, sinh viên có thể xem và in Giấy chứng nhận có mã định danh.")
    ], badge="UC04 & UC06: TICKET & CERT")

    # Slide 20: Phân Hệ CTSV: Quản Trị & Tạo Sự Kiện
    s20 = prs.slides.add_slide(blank_layout)
    add_header(s20, "5. Tính năng chính", "Phân Hệ Cán Bộ CTSV: Quản Trị Toàn Trường & Sự Kiện CRUD", "Thành viên 5")
    add_card(s20, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "5. Quản Lý Sự Kiện CRUD Hoàn Chỉnh", [
        ("Tạo sự kiện mới", "Form nhập liệu chuẩn Flask-WTF với tiêu đề, hội trường, thời gian, số lượng ghế, banner."),
        ("Soạn thảo Markdown", "Hỗ trợ định dạng bài viết chuyên nghiệp, tự động chuyển đổi sang HTML an toàn bằng Bleach."),
        ("Chỉnh sửa & Xóa sự kiện", "Cập nhật thông tin sự kiện hoặc xóa sự kiện kèm cơ chế cascade dọn sạch dữ liệu.")
    ], badge="UC10 & UC11: EVENT CRUD")
    add_card(s20, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "6. Quản Lý Danh Mục Sự Kiện (Category CRUD)", [
        ("Quản lý 5 nhóm hoạt động", "Thêm mới, chỉnh sửa tên, đường dẫn slug, màu sắc và icon hiển thị."),
        ("Bảo toàn dữ liệu (Data Integrity)", "Chặn xóa danh mục nếu đang có sự kiện liên kết, chống lỗi mồ côi dữ liệu."),
        ("Kế thừa chuẩn Chương 9", "Hiện thực trọn vẹn yêu cầu quản lý Category của môn học PWD301.")
    ], badge="CATEGORY CRUD", border_color=PRIMARY)

    # Slide 21: Phân Hệ CTSV: Check-in WebRTC & Dashboard
    s21 = prs.slides.add_slide(blank_layout)
    add_header(s21, "5. Tính năng chính", "Phân Hệ Cán Bộ CTSV: Check-in Camera & Dashboard", "Thành viên 5")
    add_card(s21, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "7. Bàn Check-in Camera WebRTC Tức Thì", [
        ("Bật Camera 1-Click", "Nhận diện Camera máy tính hoặc điện thoại, quét luồng hình ảnh 10 khung hình/giây."),
        ("Xác thực dưới 1 giây", "Giải mã chuỗi vé và gửi AJAX về máy chủ xác thực không cần tải lại trang."),
        ("Chống check-in lặp lại", "Phát cảnh báo màu vàng nếu vé đã điểm danh trước đó, ngăn chặn gian lận."),
        ("Hỗ trợ nhập tay", "Có ô nhập mã vé dự phòng nếu camera sinh viên bị mờ hoặc vỡ màn hình.")
    ], badge="UC12: QR CHECK-IN", border_color=ACCENT_GREEN)
    add_card(s21, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "8. Dashboard Thống Kê & Xuất File Excel", [
        ("Dashboard thời gian thực", "Theo dõi số vé phát hành, số người thực tế có mặt, tỷ lệ lấp đầy hội trường."),
        ("Xuất báo cáo CSV chuẩn", "Xuất toàn bộ danh sách người tham gia kèm ký tự UTF-8 BOM, mở trên Excel không lỗi font tiếng Việt."),
        ("Hỗ trợ lưu trữ văn thư", "Phục vụ đối soát danh sách sinh viên tham gia phong trào cho Phòng CTSV.")
    ], badge="UC13 & UC14: ANALYTICS")

    # Slide 22: Kịch Bản Live Demo Thực Tế
    s22 = prs.slides.add_slide(blank_layout)
    add_header(s22, "5. Tính năng chính", "Kịch Bản Trình Diễn Live Demo Hệ Thống (8 - 10 Phút)", "Thành viên 4 & 5")
    add_card(s22, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0), "Chặng 1: Sinh Viên (3 phút)", [
        ("Bước 1", "Mở trang chủ, tìm kiếm Workshop AI, lọc danh mục Công nghệ."),
        ("Bước 2", "Đăng nhập bằng FPT Mail của Trương Công Dũng (DE200433)."),
        ("Bước 3", "Bấm 'Đăng ký giữ chỗ ngay' &rarr; Nhận mã vé điện tử và QR Code."),
        ("Bước 4", "Mở trang 'Vé Của Tôi', xem mã QR và thử nghiệm tính năng hủy vé.")
    ], badge="DEMO FLOW 1")
    add_card(s22, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0), "Chặng 2: CTSV Điểm Danh (3 phút)", [
        ("Bước 5", "Đăng nhập tài khoản Phòng CTSV (ADM001)."),
        ("Bước 6", "Mở 'Bàn Check-in', bật Camera quét mã QR trên điện thoại của sinh viên."),
        ("Bước 7", "Hệ thống xác thực thành công trong 0.5s &rarr; Bắn hiệu ứng pháo hoa."),
        ("Bước 8", "Thử quét lại vé lần 2 &rarr; Hệ thống cảnh báo vé đã check-in.")
    ], badge="DEMO FLOW 2", border_color=PRIMARY)
    add_card(s22, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0), "Chặng 3: Kết Quả & Báo Cáo (2 phút)", [
        ("Bước 9", "Sinh viên tải lại trang &rarr; Nút 'Xem Giấy Chứng Nhận E-Cert' kích hoạt."),
        ("Bước 10", "CTSV mở Dashboard, xem tỷ lệ lấp đầy hội trường cập nhật tức thì."),
        ("Bước 11", "Bấm 'Xuất danh sách CSV' &rarr; Mở file Excel tiếng Việt hiển thị chuẩn chỉnh.")
    ], badge="DEMO FLOW 3", border_color=ACCENT_GREEN)

    # =========================================================================
    # SECTION 6: PHẦN KIỂM THỬ (TESTING & SECURITY) (Slides 23 - 26)
    # =========================================================================
    # Slide 23: Chiến Lược Kiểm Thử
    s23 = prs.slides.add_slide(blank_layout)
    add_header(s23, "6. Kiểm thử dự án", "Chiến Lược Kiểm Thử Toàn Diện (Testing Pyramid)", "Thành viên 5")
    add_card(s23, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0), "1. Unit Testing (Đơn Vị)", [
        ("Thư viện sử dụng", "unittest chuẩn của Python."),
        ("Phạm vi kiểm thử", "Kiểm thử các hàm logic độc lập: password hashing, sinh mã vé, custom validator SĐT, tính điểm rating."),
        ("Môi trường độc lập", "Tự động khởi tạo database SQLite in-memory cho mỗi bài test (setUp và tearDown).")
    ], badge="TẦNG 1: UNIT TEST")
    add_card(s23, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0), "2. Integration Testing (Tích Hợp)", [
        ("Flask Test Client", "Giả lập HTTP Request kiểm thử toàn bộ luồng nghiệp vụ."),
        ("Kiểm thử giao dịch", "Quy trình đặt vé giữ chỗ, trừ slot, kiểm tra hết vé và hủy vé hoàn lại chỗ."),
        ("Kiểm thử API", "Gửi request đến các endpoint /api/v1/events, /api/v1/categories, /api/v1/stats.")
    ], badge="TẦNG 2: INTEGRATION")
    add_card(s23, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0), "3. Security & UI Testing", [
        ("Kiểm thử bảo mật", "Thử nghiệm tấn công XSS injection, Open Redirect URL, giả mạo quyền truy cập 403."),
        ("Kiểm thử giao diện", "Kiểm tra hiển thị responsive trên các kích thước màn hình Mobile, Tablet, Desktop."),
        ("Kiểm thử Dark Mode", "Đảm bảo độ tương phản màu sắc đạt chuẩn WCAG.")
    ], badge="TẦNG 3: SECURITY & UI", border_color=PRIMARY)

    # Slide 24: Kết Quả 15 Test Cases Tự Động
    s24 = prs.slides.add_slide(blank_layout)
    add_header(s24, "6. Kiểm thử dự án", "Kết Quả Thực Thi 15 Test Cases Tự Động (Pass 100%)", "Thành viên 5")
    add_card(s24, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Danh Sách Test Cases Đã Chạy", [
        ("test_user_password_hashing", "Kiểm tra mã hóa và xác thực mật khẩu PBKDF2. [PASS]"),
        ("test_event_capacity_and_sold_out", "Kiểm tra giới hạn số lượng ghế và trạng thái Sold Out. [PASS]"),
        ("test_ticket_creation_and_code_gen", "Kiểm tra sinh mã vé định danh FU-2026-XXXXXX. [PASS]"),
        ("test_booking_transaction", "Kiểm tra trừ slot và tạo vé trong transaction. [PASS]"),
        ("test_ticket_cancellation_frees_slot", "Kiểm tra hủy vé tự động hoàn lại chỗ ngồi. [PASS]"),
        ("test_check_in_logic", "Kiểm tra điểm danh và ghi nhận thời gian thực. [PASS]"),
        ("test_event_review_and_average_rating", "Kiểm tra đánh giá và tính điểm sao trung bình. [PASS]"),
        ("test_email_domain_validation", "Chặn email ngoài trường, chỉ nhận @fpt.edu.vn. [PASS]")
    ], badge="TEST CASES 1 - 8", border_color=ACCENT_GREEN)
    add_card(s24, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Danh Sách Test Cases Tiếp Theo", [
        ("test_custom_phone_validator", "Kiểm tra SĐT chuẩn 10 số bắt đầu bằng 0 (Lab 6). [PASS]"),
        ("test_open_redirect_safety_helper", "Chặn đứng các URL độc hại chuyển hướng ngoài. [PASS]"),
        ("test_rest_api_events_list", "Kiểm tra API danh sách sự kiện kèm phân trang. [PASS]"),
        ("test_rest_api_categories", "Kiểm tra API danh mục sự kiện trả về JSON. [PASS]"),
        ("test_rest_api_stats", "Kiểm tra API thống kê tổng quan hệ thống. [PASS]"),
        ("test_custom_template_filters", "Kiểm tra bộ lọc VND, ngày tháng, cắt ngắn chữ. [PASS]"),
        ("test_category_crud_and_integrity", "Kiểm tra toàn vẹn CSDL khi thao tác danh mục. [PASS]"),
        ("TỔNG KẾT THỰC THI", "15/15 Tests Passed trong 7.28s — Không có lỗi nào!")
    ], badge="TEST CASES 9 - 15", border_color=ACCENT_GREEN)

    # Slide 25: Kiểm Thử Bảo Mật Chuyên Sâu
    s25 = prs.slides.add_slide(blank_layout)
    add_header(s25, "6. Kiểm thử dự án", "Kiểm Thử An Toàn Thông Tin & Phòng Chống Lỗ Hổng Web", "Thành viên 5")
    add_card(s25, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.35), "1. Chống Tấn Công Stored XSS", [
        ("Payload thử nghiệm", "<script>alert('XSS')</script> hoặc <img src=x onerror=steal()>."),
        ("Kết quả xử lý", "Bleach lọc sạch 100% mã độc, chỉ giữ lại các thẻ văn bản an toàn.")
    ], badge="XSS DEFENSE", border_color=ACCENT_GREEN)
    add_card(s25, Inches(6.8), Inches(1.8), Inches(5.6), Inches(2.35), "2. Chống Lỗ Hổng Open Redirect", [
        ("Payload thử nghiệm", "next=http://malicious-attacker-site.com/login."),
        ("Kết quả xử lý", "Hàm is_safe_url() kiểm tra netloc máy chủ, từ chối chuyển hướng ngoài.")
    ], badge="REDIRECT DEFENSE", border_color=ACCENT_GREEN)
    add_card(s25, Inches(0.8), Inches(4.45), Inches(5.6), Inches(2.35), "3. Chống Tấn Công SQL Injection", [
        ("Kỹ thuật phòng thủ", "100% truy vấn qua SQLAlchemy ORM với Parameterized Queries."),
        ("Kết quả xử lý", "Không có bất kỳ câu lệnh SQL raw nào, vô hiệu hóa hoàn toàn SQLi.")
    ], badge="SQLI DEFENSE", border_color=ACCENT_GREEN)
    add_card(s25, Inches(6.8), Inches(4.45), Inches(5.6), Inches(2.35), "4. Chống Tấn Công CSRF & Vượt Quyền", [
        ("CSRF Protection", "Tất cả các Form POST đều có csrf_token ẩn được kiểm tra nghiêm ngặt."),
        ("Phân quyền 403", "Sinh viên cố tình truy cập /admin/* nhận ngay mã lỗi 403 Forbidden.")
    ], badge="CSRF & RBAC", border_color=ACCENT_GREEN)

    # Slide 26: Kết Luận & Q&A
    s26 = prs.slides.add_slide(blank_layout)
    bg26 = s26.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg26.fill.solid()
    bg26.fill.fore_color.rgb = BG_DARK
    bg26.line.fill.background()

    tb26 = s26.shapes.add_textbox(Inches(1.5), Inches(1.5), Inches(10.333), Inches(4.5))
    tf26 = tb26.text_frame
    tf26.word_wrap = True

    p_c1 = tf26.paragraphs[0]
    p_c1.alignment = PP_ALIGN.CENTER
    r_c1 = p_c1.add_run()
    r_c1.text = "TỔNG KẾT & ĐỊNH HƯỚNG PHÁT TRIỂN\n"
    r_c1.font.bold = True
    r_c1.font.size = Pt(28)
    r_c1.font.color.rgb = PRIMARY

    p_c2 = tf26.add_paragraph()
    p_c2.alignment = PP_ALIGN.CENTER
    p_c2.space_before = Pt(14)
    r_c2 = p_c2.add_run()
    r_c2.text = (
        "FPTU EventHub đã giải quyết triệt để 4 bài toán đau đầu của cổng sự kiện truyền thống:\n"
        "Đăng nhập 1-Click FPT Mail • Giữ chỗ thời gian thực không vỡ trận • Check-in Camera WebRTC dưới 1 giây • Cấp Giấy chứng nhận tự động.\n\n"
        "Định hướng phát triển: Mở rộng tích hợp gửi mã QR qua Zalo/Email sinh viên và ứng dụng AI gợi ý sự kiện phù hợp."
    )
    r_c2.font.size = Pt(14)
    r_c2.font.color.rgb = TEXT_LIGHT

    p_c3 = tf26.add_paragraph()
    p_c3.alignment = PP_ALIGN.CENTER
    p_c3.space_before = Pt(28)
    r_c3 = p_c3.add_run()
    r_c3.text = "XIN TRÂN TRỌNG CẢM ƠN QUÝ THẦY CÔ TRONG HỘI ĐỒNG!\n"
    r_c3.font.bold = True
    r_c3.font.size = Pt(20)
    r_c3.font.color.rgb = SECONDARY

    r_c4 = p_c3.add_run()
    r_c4.text = "Nhóm chúng em sẵn sàng lắng nghe câu hỏi và nhận xét từ Hội đồng chấm thi."
    r_c4.font.size = Pt(14)
    r_c4.font.color.rgb = TEXT_MUTED

    prs.save(output_path)
    print(f"Presentation successfully saved to: {output_path}")

if __name__ == "__main__":
    out = r"C:\Users\truon\fptu_eventhub\SLIDE_THUYET_TRINH_FPTU_EVENTHUB.pptx"
    create_presentation(out)
