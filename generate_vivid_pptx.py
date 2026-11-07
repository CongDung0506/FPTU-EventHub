# -*- coding: utf-8 -*-
"""
Canva-Style Presentation Generator for FPTU EventHub (26 Slides, 45-50 Mins)
Features:
- Visual diversity: Big KPI numbers, colored chips/pills, timeline chevrons, comparison boards.
- Embedded high-res images from static/images/ (FPT logo, hero campus, real event banners).
- Bento grid layouts with colored top accents and high contrast typography.
- Concise bullet points (no text walls), clear visual hierarchy.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    BG_DARK = RGBColor(11, 17, 32)        # Deep Slate 950
    CARD_BG = RGBColor(24, 33, 53)        # Slate 850
    CARD_BORDER = RGBColor(51, 65, 85)    # Slate 700
    
    PRIMARY = RGBColor(242, 111, 33)      # FPT Vibrant Orange
    PRIMARY_LIGHT = RGBColor(254, 215, 170)
    PRIMARY_BG = RGBColor(67, 28, 6)

    BLUE = RGBColor(2, 132, 199)          # Electric Sky Blue
    BLUE_LIGHT = RGBColor(186, 230, 253)
    BLUE_BG = RGBColor(12, 44, 74)

    GREEN = RGBColor(16, 185, 129)        # Emerald Green
    GREEN_LIGHT = RGBColor(167, 243, 208)
    GREEN_BG = RGBColor(6, 78, 59)

    RED = RGBColor(239, 68, 68)           # Coral Red
    RED_LIGHT = RGBColor(254, 202, 202)
    RED_BG = RGBColor(80, 15, 15)

    PURPLE = RGBColor(139, 92, 246)       # Violet AI
    PURPLE_LIGHT = RGBColor(221, 214, 254)

    TEXT_WHITE = RGBColor(255, 255, 255)
    TEXT_LIGHT = RGBColor(241, 245, 249)
    TEXT_MUTED = RGBColor(148, 163, 184)
    TEXT_GOLD = RGBColor(251, 191, 36)

    IMG_DIR = r"C:\Users\truon\fptu_eventhub\static\images"
    IMG_HERO = os.path.join(IMG_DIR, "fpt_campus_hero.jpg")
    IMG_LOGO = os.path.join(IMG_DIR, "fpt_logo.jpg")
    IMG_AI = os.path.join(IMG_DIR, "events", "workshop_ai.jpg")
    IMG_HACK = os.path.join(IMG_DIR, "events", "hackathon.jpg")
    IMG_CAREER = os.path.join(IMG_DIR, "events", "fsoft_career.jpg")
    IMG_FESTIVAL = os.path.join(IMG_DIR, "events", "club_festival.jpg")
    IMG_VOVINAM = os.path.join(IMG_DIR, "events", "vovinam.jpg")

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, tag, title, presenter="", icon="⚡"):
        set_slide_background(slide)
        
        # Top gradient accent bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.1))
        bar.fill.solid()
        bar.fill.fore_color.rgb = PRIMARY
        bar.line.fill.background()

        # Tag Pill
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.35), Inches(3.2), Inches(0.35))
        pill.fill.solid()
        pill.fill.fore_color.rgb = PRIMARY_BG
        pill.line.color.rgb = PRIMARY
        pill.line.width = Pt(1)
        tf_p = pill.text_frame
        p_p = tf_p.paragraphs[0]
        p_p.alignment = PP_ALIGN.CENTER
        r_p = p_p.add_run()
        r_p.text = f"{icon}  {tag.upper()}"
        r_p.font.bold = True
        r_p.font.size = Pt(10.5)
        r_p.font.color.rgb = PRIMARY

        # Presenter Pill (if provided)
        if presenter:
            p_pres = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.2), Inches(0.35), Inches(3.2), Inches(0.35))
            p_pres.fill.solid()
            p_pres.fill.fore_color.rgb = BLUE_BG
            p_pres.line.color.rgb = BLUE
            p_pres.line.width = Pt(1)
            tf_pr = p_pres.text_frame
            pp = tf_pr.paragraphs[0]
            pp.alignment = PP_ALIGN.CENTER
            rr = pp.add_run()
            rr.text = f"🎤 {presenter}"
            rr.font.bold = True
            rr.font.size = Pt(10.5)
            rr.font.color.rgb = BLUE_LIGHT

        # Slide Main Title
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.733), Inches(0.7))
        p = tb.text_frame.paragraphs[0]
        r = p.add_run()
        r.text = title
        r.font.bold = True
        r.font.size = Pt(22)
        r.font.color.rgb = TEXT_WHITE

    def add_kpi_card(slide, left, top, width, height, number_str, label_str, subtext="", color=PRIMARY, bg_color=CARD_BG):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.15), width - Inches(0.3), height - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.alignment = PP_ALIGN.CENTER
        r1 = p1.add_run()
        r1.text = number_str
        r1.font.bold = True
        r1.font.size = Pt(32)
        r1.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        p2.space_before = Pt(2)
        r2 = p2.add_run()
        r2.text = label_str
        r2.font.bold = True
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_WHITE

        if subtext:
            p3 = tf.add_paragraph()
            p3.alignment = PP_ALIGN.CENTER
            p3.space_before = Pt(2)
            r3 = p3.add_run()
            r3.text = subtext
            r3.font.size = Pt(9.5)
            r3.font.color.rgb = TEXT_MUTED

    def add_bento_box(slide, left, top, width, height, title, items, top_accent=PRIMARY, icon="📌"):
        # Main box
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = CARD_BORDER
        box.line.width = Pt(1)

        # Top Accent Strip
        strip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.08))
        strip.fill.solid()
        strip.fill.fore_color.rgb = top_accent
        strip.line.fill.background()

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.18), width - Inches(0.4), height - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = f"{icon} {title}"
        r0.font.bold = True
        r0.font.size = Pt(14)
        r0.font.color.rgb = TEXT_WHITE

        for it in items:
            p = tf.add_paragraph()
            p.space_before = Pt(6)
            if isinstance(it, tuple):
                bold_txt, norm_txt = it
                r_b = p.add_run()
                r_b.text = f"• {bold_txt}: "
                r_b.font.bold = True
                r_b.font.size = Pt(11)
                r_b.font.color.rgb = PRIMARY_LIGHT
                
                r_n = p.add_run()
                r_n.text = norm_txt
                r_n.font.size = Pt(11)
                r_n.font.color.rgb = TEXT_LIGHT
            else:
                r = p.add_run()
                r.text = f"• {it}"
                r.font.size = Pt(11)
                r.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 1: COVER SLIDE (Canva Hero Layout with Campus Photo)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Right side: Hero Campus Photo container
    if os.path.exists(IMG_HERO):
        s1.shapes.add_picture(IMG_HERO, Inches(7.5), Inches(0.8), Inches(5.1), Inches(5.9))
        # Subtle border frame
        frame = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.5), Inches(0.8), Inches(5.1), Inches(5.9))
        frame.fill.background()
        frame.line.color.rgb = PRIMARY
        frame.line.width = Pt(2)

    # Overlay Pill Badge on Image
    badge1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(5.8), Inches(4.5), Inches(0.6))
    badge1.fill.solid()
    badge1.fill.fore_color.rgb = BG_DARK
    badge1.line.color.rgb = GREEN
    badge1.line.width = Pt(1.5)
    tf_b1 = badge1.text_frame
    p_b1 = tf_b1.paragraphs[0]
    p_b1.alignment = PP_ALIGN.CENTER
    r_b1 = p_b1.add_run()
    r_b1.text = "🟢 LIVE PRODUCTION: fptu-event-hub.vercel.app"
    r_b1.font.bold = True
    r_b1.font.size = Pt(10.5)
    r_b1.font.color.rgb = GREEN_LIGHT

    # Left side: Typography & Details
    if os.path.exists(IMG_LOGO):
        s1.shapes.add_picture(IMG_LOGO, Inches(0.8), Inches(0.8), Inches(1.8), Inches(0.7))

    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(6.3), Inches(4.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p_sub = tf1.paragraphs[0]
    r_sub = p_sub.add_run()
    r_sub.text = "TRƯỜNG ĐẠI HỌC FPT — BẢO VỆ ĐỒ ÁN CHUYÊN NGÀNH CNTT\n"
    r_sub.font.bold = True
    r_sub.font.size = Pt(11.5)
    r_sub.font.color.rgb = BLUE

    p_main = tf1.add_paragraph()
    p_main.space_before = Pt(4)
    r_main = p_main.add_run()
    r_main.text = "FPTU EventHub\n"
    r_main.font.bold = True
    r_main.font.size = Pt(38)
    r_main.font.color.rgb = PRIMARY

    p_desc = tf1.add_paragraph()
    r_desc = p_desc.add_run()
    r_desc.text = "CỔNG QUẢN LÝ & ĐĂNG KÝ SỰ KIỆN SINH VIÊN ĐẠI HỌC FPT\n"
    r_desc.font.bold = True
    r_desc.font.size = Pt(15)
    r_desc.font.color.rgb = TEXT_WHITE

    p_sub2 = tf1.add_paragraph()
    p_sub2.space_before = Pt(8)
    r_sub2 = p_sub2.add_run()
    r_sub2.text = (
        "• Tự động hóa 100% quy trình: Zero-SSO 1-Click FPT Mail\n"
        "• Giữ chỗ thời gian thực không overbooking • Check-in Camera WebRTC < 1s\n"
        "• Công nghệ: Python 3.11 / Flask, SQLAlchemy ORM, Vercel Serverless"
    )
    r_sub2.font.size = Pt(11.5)
    r_sub2.font.color.rgb = TEXT_MUTED

    p_team = tf1.add_paragraph()
    p_team.space_before = Pt(14)
    r_team = p_team.add_run()
    r_team.text = "Nhóm thực hiện: Trương Công Dũng (Lead) cùng 4 thành viên (50 phút)"
    r_team.font.bold = True
    r_team.font.size = Pt(12)
    r_team.font.color.rgb = TEXT_GOLD

    # =========================================================================
    # SLIDE 2: BỐI CẢNH (3 Big KPI Cards + Visual Photo)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "1. Giới thiệu dự án", "Bối Cảnh & Nhu Cầu Chuyển Đổi Số Sự Kiện FPTU", "Thành viên 1", "🏫")
    
    # 3 Big KPI Numbers at top
    add_kpi_card(s2, Inches(0.8), Inches(1.5), Inches(3.6), Inches(1.5), "30+ CLB", "Phong Trào Bùng Nổ", "Học thuật, công nghệ, văn hóa, thể thao", PRIMARY)
    add_kpi_card(s2, Inches(4.8), Inches(1.5), Inches(3.6), Inches(1.5), "100+ Buổi/Kỳ", "Tần Suất Liên Tục", "Workshop, Hackathon, Talkshow OJT", BLUE)
    add_kpi_card(s2, Inches(8.8), Inches(1.5), Inches(3.6), Inches(1.5), "100 - 250", "Sức Chứa Giới Hạn", "Hội trường Alpha/Beta & Lab AI", GREEN)

    # Bottom Left: Narrative Bento
    add_bento_box(s2, Inches(0.8), Inches(3.2), Inches(6.8), Inches(3.6), "Thực Trạng Năng Động & Thách Thức Không Gian", [
        ("Áp lực kiểm soát sức chứa", "Hội trường và phòng Lab có số máy cố định, không thể nhận dư sinh viên."),
        ("Kỳ vọng thế hệ Gen Z", "Muốn thao tác 1-chạm trên smartphone, có vé định danh, không muốn xếp hàng ký giấy."),
        ("Yêu cầu từ Cán bộ CTSV", "Cần một hệ thống quản trị thống nhất thay thế các bảng tính Excel rời rạc.")
    ], top_accent=PRIMARY, icon="🎯")

    # Bottom Right: Real Event Picture
    if os.path.exists(IMG_FESTIVAL):
        s2.shapes.add_picture(IMG_FESTIVAL, Inches(7.9), Inches(3.2), Inches(4.6), Inches(3.6))
        # Tag on image
        tag_f = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.1), Inches(6.2), Inches(4.2), Inches(0.45))
        tag_f.fill.solid()
        tag_f.fill.fore_color.rgb = BG_DARK
        tag_f.line.color.rgb = PRIMARY
        tf_tf = tag_f.text_frame
        ptf = tf_tf.paragraphs[0]
        ptf.alignment = PP_ALIGN.CENTER
        rtf = ptf.add_run()
        rtf.text = "Lễ Hội CLB & Workshop Công Nghệ FPTU"
        rtf.font.bold = True
        rtf.font.size = Pt(10.5)
        rtf.font.color.rgb = TEXT_WHITE

    # =========================================================================
    # SLIDE 3: NỖI ĐAU CỔNG CŨ (4 Red Alert Cards with Big Warning Badges)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "1. Giới thiệu dự án", "4 'Nỗi Đau' Lớn Từ Cổng Cũ events.fptu.vn", "Thành viên 1", "⚠️")

    add_bento_box(s3, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.5), "01. Vỡ Trận Sức Chứa Hội Trường", [
        ("events.fptu.vn chỉ là tin tĩnh", "Khi đăng ký bắt buộc phải dẫn link ra Google Form."),
        ("Không khóa số lượng tự động", "Hội trường 100 ghế nhưng Form nhận 250 đơn, sinh viên đến không có chỗ ngồi.")
    ], top_accent=RED, icon="🚨")

    add_bento_box(s3, Inches(6.8), Inches(1.6), Inches(5.6), Inches(2.5), "02. Điểm Danh Thủ Công Ùn Tắc", [
        ("Dò tên trên danh sách giấy", "Sinh viên đứng xếp hàng dài tại cửa ra vào để cán bộ dò từng MSSV."),
        ("Tốn 20-30 phút/buổi", "Dễ thất lạc dữ liệu, gian lận điểm danh hộ rất phổ biến.")
    ], top_accent=RED, icon="⏱️")

    add_bento_box(s3, Inches(0.8), Inches(4.4), Inches(5.6), Inches(2.5), "03. Ghế Ảo (Đăng Ký Đầy Nhưng Vắng)", [
        ("Không có vé điện tử QR", "Sinh viên không có mã định danh để đối soát tại cửa."),
        ("Không có nút hủy vé", "Sinh viên bận đột xuất không thể hủy vé để nhường lại slot ghế cho bạn khác.")
    ], top_accent=RED, icon="🎟️")

    add_bento_box(s3, Inches(6.8), Inches(4.4), Inches(5.6), Inches(2.5), "04. Chậm Trễ Cấp Giấy Chứng Nhận", [
        ("Quy trình văn thư thủ công", "Mất từ 2 đến 3 tuần để ban tổ chức thiết kế và gửi email chứng nhận."),
        ("Mất động lực học thuật", "Sinh viên không theo dõi được lịch sử tham gia phong trào của bản thân.")
    ], top_accent=RED, icon="📜")

    # =========================================================================
    # SLIDE 4: SỨ MỆNH & MỤC TIÊU (3 Big Metrics + Event Poster)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "1. Giới thiệu dự án", "Mục Tiêu Đột Phá Của FPTU EventHub", "Thành viên 1", "🎯")

    add_kpi_card(s4, Inches(0.8), Inches(1.5), Inches(3.6), Inches(1.5), "0.1 Giây", "Đặt Vé Giữ Chỗ", "Transaction nguyên tử, chống overbooking", PRIMARY)
    add_kpi_card(s4, Inches(4.8), Inches(1.5), Inches(3.6), Inches(1.5), "< 1 Giây", "Check-in Camera QR", "WebRTC MediaDevices không cần cài App", GREEN)
    add_kpi_card(s4, Inches(8.8), Inches(1.5), Inches(3.6), Inches(1.5), "100%", "Tự Động Hóa", "Cấp vé QR, hủy vé hoàn slot, cấp E-Cert", BLUE)

    if os.path.exists(IMG_AI):
        s4.shapes.add_picture(IMG_AI, Inches(0.8), Inches(3.2), Inches(4.6), Inches(3.6))

    add_bento_box(s4, Inches(5.7), Inches(3.2), Inches(6.8), Inches(3.6), "3 Trụ Cột Đột Phá Giá Trị", [
        ("Trải Nghiệm Sinh Viên 1-Chạm", "Zero-SSO FPT Mail (@fpt.edu.vn), tự động bóc tách MSSV, ví vé QR cá nhân."),
        ("Vận Hành Điểm Danh Siêu Tốc", "Mở Camera laptop/điện thoại quét mã QR tức thì, phát hiện cảnh báo quét trùng."),
        ("Báo Cáo Thời Gian Thực", "Dashboard tỷ lệ lấp đầy hội trường và xuất danh sách CSV cho phòng CTSV.")
    ], top_accent=GREEN, icon="🚀")

    # =========================================================================
    # SLIDE 5: BẢNG SO SÁNH CŨ VS MỚI (Battle Board Canvas)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "1. Giới thiệu dự án", "So Sánh Toàn Diện: events.fptu.vn vs FPTU EventHub", "Thành viên 1", "⚖️")

    # Left: Old System (Red toned)
    add_bento_box(s5, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3), "CỔNG CŨ: events.fptu.vn (Thủ Công)", [
        ("Phương thức vào", "Dẫn link ngoài qua Google Form rườm rà."),
        ("Kiểm soát ghế", "Không giới hạn real-time, nhận dư 200% số chỗ."),
        ("Vé tham dự", "Không có vé điện tử, chỉ có email text thô."),
        ("Điểm danh", "Dò danh sách giấy hoặc dò MSSV bằng mắt thường."),
        ("Hủy vé", "Không có nút hủy, dẫn đến ghế trống rất nhiều."),
        ("Chứng nhận", "Chờ thiết kế gửi email sau 2-3 tuần."),
        ("Phân quyền", "Không có trang quản trị chuyên biệt cho Cán bộ.")
    ], top_accent=RED, icon="❌")

    # Right: New System (Green/Orange glowing)
    add_bento_box(s5, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.3), "FPTU EVENTHUB (Tự Động Hóa 100%)", [
        ("Phương thức vào", "Zero-SSO 1-Click nhận diện FPT Mail (@fpt.edu.vn)."),
        ("Kiểm soát ghế", "Thuật toán Atomic, tự khóa nút ĐÃ HẾT VÉ tức thì."),
        ("Vé tham dự", "Vé điện tử kèm mã QR động độc bản chống giả mạo."),
        ("Điểm danh", "WebRTC Camera QR Scanner giải mã dưới 1 giây."),
        ("Hủy vé", "Hủy vé 1-click, tự động hoàn trả slot ghế cho bạn khác."),
        ("Chứng nhận", "Cấp Giấy chứng nhận điện tử (E-Cert) tự động."),
        ("Phân quyền", "Tách biệt RBAC: Sinh viên vs Phòng CTSV.")
    ], top_accent=GREEN, icon="✅")

    # =========================================================================
    # SLIDE 6: MA TRẬN 5 THÀNH VIÊN (5 Persona Cards with 20% Contribution)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "2. Phân công nhiệm vụ", "Ma Trận Phân Công 5 Thành Viên (Đóng Góp Đồng Đều 20%)", "Thành viên 2", "👥")

    members_data = [
        ("Trương Công Dũng", "Lead Full-Stack", "MVC Architecture, Flask, Dual-DB, Zero-SSO, Vercel Serverless.", PRIMARY),
        ("Thành Viên 2", "Backend & Security", "Werkzeug PBKDF2/SHA-256, Bleach XSS, custom validators, CSRF.", BLUE),
        ("Thành Viên 3", "Database & ORM", "ERD 6 bảng, migration SQL Server/SQLite, Transaction đặt vé, paginate.", GREEN),
        ("Thành Viên 4", "Frontend & UI/UX", "Giao diện Dark Tech, CSS Scoped BEM, responsive, WebRTC QR Scanner.", PURPLE),
        ("Thành Viên 5", "QA Tester & CTSV", "Bộ 15 Unit Tests tự động, kiểm thử bảo mật, dashboard CTSV, xuất CSV.", TEXT_GOLD)
    ]

    card_w = Inches(2.2)
    card_h = Inches(5.2)
    for idx, (name, role, tasks, col) in enumerate(members_data):
        left_pos = Inches(0.8 + idx * 2.4)
        c = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.5), card_w, card_h)
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = col
        c.line.width = Pt(1.5)

        tb = s6.shapes.add_textbox(left_pos + Inches(0.1), Inches(1.6), card_w - Inches(0.2), card_h - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True

        # Member icon
        p_ico = tf.paragraphs[0]
        p_ico.alignment = PP_ALIGN.CENTER
        r_ico = p_ico.add_run()
        r_ico.text = "👤"
        r_ico.font.size = Pt(28)

        # Name
        p_n = tf.add_paragraph()
        p_n.alignment = PP_ALIGN.CENTER
        p_n.space_before = Pt(4)
        r_n = p_n.add_run()
        r_n.text = name
        r_n.font.bold = True
        r_n.font.size = Pt(13)
        r_n.font.color.rgb = TEXT_WHITE

        # Role Pill
        p_r = tf.add_paragraph()
        p_r.alignment = PP_ALIGN.CENTER
        p_r.space_before = Pt(2)
        r_r = p_r.add_run()
        r_r.text = role
        r_r.font.bold = True
        r_r.font.size = Pt(10)
        r_r.font.color.rgb = col

        # Tasks
        p_t = tf.add_paragraph()
        p_t.space_before = Pt(10)
        r_t = p_t.add_run()
        r_t.text = tasks
        r_t.font.size = Pt(10)
        r_t.font.color.rgb = TEXT_MUTED

        # Contribution
        p_c = tf.add_paragraph()
        p_c.alignment = PP_ALIGN.CENTER
        p_c.space_before = Pt(12)
        r_c = p_c.add_run()
        r_c.text = "20% ĐÓNG GÓP"
        r_c.font.bold = True
        r_c.font.size = Pt(10.5)
        r_c.font.color.rgb = col

    # =========================================================================
    # SLIDE 7: CƠ CHẾ PHỐI HỢP & GIAO TIẾP (3 Connected Process Blocks)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "2. Phân công nhiệm vụ", "Cơ Chế Họp Nhóm, Giao Tiếp & Code Review Chéo", "Thành viên 2", "🤝")

    add_bento_box(s7, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.2), "01. Daily Standup 15 Phút", [
        ("Tần suất", "Họp trực tuyến ngắn mỗi tối."),
        ("3 Câu hỏi trọng tâm", "1. Đã làm gì hôm nay?\n2. Sẽ làm gì ngày mai?\n3. Có vướng mắc hay blocker gì?"),
        ("Kênh liên lạc", "Discord phân luồng #backend, #frontend, #bugs."),
        ("Hiệu quả", "Phát hiện sớm sai lệch yêu cầu.")
    ], top_accent=PRIMARY, icon="⏰")

    add_bento_box(s7, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.2), "02. Code Review Chéo", [
        ("Quy tắc 2 Reviewers", "Bắt buộc ít nhất 2 thành viên duyệt Pull Request trước khi merge."),
        ("Kiểm tra tự động", "Chạy test suite 15 kịch bản trước khi chấp thuận code."),
        ("Chuẩn hóa định dạng", "Tuân thủ PEP8 cho Python và BEM cho CSS."),
        ("Nâng cao chất lượng", "Giảm 90% lỗi phát sinh trong mã nguồn.")
    ], top_accent=BLUE, icon="🔍")

    add_bento_box(s7, Inches(8.8), Inches(1.6), Inches(3.6), Inches(5.2), "03. Quản Trị Rủi Ro & Backup", [
        ("Cơ chế Shadow", "Mỗi module có 1 người phụ trách chính (Primary) và 1 người dự phòng (Shadow)."),
        ("Phòng ngừa sự cố", "Nếu một thành viên gặp trục trặc, người dự phòng lập tức tiếp quản."),
        ("Quyết định dứt khoát", "Trưởng nhóm có quyền quyết định cuối cùng khi có tranh cãi kỹ thuật.")
    ], top_accent=GREEN, icon="🛡️")

    # =========================================================================
    # SLIDE 8: ĐÀO TẠO NỘI BỘ (3 Workshop Cards)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "2. Phân công nhiệm vụ", "Chia Sẻ Tri Thức Kỹ Thuật Nội Bộ (Knowledge Sharing)", "Thành viên 2", "💡")

    add_bento_box(s8, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.2), "Workshop 1: Gitflow Master", [
        ("Nội dung", "Cách phân nhánh feature, xử lý merge conflicts, rebase an toàn."),
        ("Quy ước Commit", "Thống nhất chuẩn Conventional Commits (feat, fix, docs, test)."),
        ("Kết quả", "100% thành viên không làm hỏng nhánh main.")
    ], top_accent=PRIMARY, icon="🌿")

    add_bento_box(s8, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.2), "Workshop 2: Pure SQLAlchemy ORM", [
        ("Nội dung", "Quan hệ cascade delete-orphan, transaction commit/rollback, eager loading."),
        ("Quy tắc sống còn", "Tuyệt đối không dùng SQL raw, 100% qua ORM models."),
        ("Kết quả", "Vô hiệu hóa hoàn toàn lỗ hổng SQL Injection.")
    ], top_accent=BLUE, icon="🗄️")

    add_bento_box(s8, Inches(8.8), Inches(1.6), Inches(3.6), Inches(5.2), "Workshop 3: WebRTC Camera QR", [
        ("Nội dung", "Nguyên lý MediaDevices API, cách tối ưu tốc độ quét 10 fps."),
        ("Kiểm soát bảo mật", "Sinh mã QR Hash bảo vệ và gửi AJAX ngầm về máy chủ."),
        ("Kết quả", "Check-in tốc độ cao không cần tải lại trang.")
    ], top_accent=GREEN, icon="📷")

    # =========================================================================
    # SLIDE 9: BỘ TOOL QLDA (4 Brand Cards)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "3. Quản lý dự án", "Hệ Sinh Thái Công Cụ Quản Lý & Điều Hành Dự Án", "Thành viên 2", "🛠️")

    add_bento_box(s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.5), "GitHub Projects (Kanban Board)", [
        ("4 Cột luồng việc", "Backlog &rarr; To Do &rarr; In Progress &rarr; Done."),
        ("Nhãn dán (Labels)", "Phân loại feature, bug, security, priority-high."),
        ("Tự động hóa", "Đóng Issue tự động khi Pull Request được merge.")
    ], top_accent=PURPLE, icon="📋")

    add_bento_box(s9, Inches(6.8), Inches(1.6), Inches(5.6), Inches(2.5), "Git & GitHub Repository", [
        ("Quản lý mã nguồn", "Lưu trữ tại CongDung0506/FPTU-EventHub."),
        ("Bảo vệ nhánh main", "Chặn commit trực tiếp, bắt buộc Pull Request."),
        ("Lịch sử minh bạch", "Ghi nhận 100% lịch sử đóng góp của từng thành viên.")
    ], top_accent=BLUE, icon="🐙")

    add_bento_box(s9, Inches(0.8), Inches(4.4), Inches(5.6), Inches(2.5), "Notion & Google Workspace", [
        ("Tài liệu SRS & UseCase", "Lưu trữ tập trung đặc tả yêu cầu và sơ đồ luồng."),
        ("Biên bản cuộc họp", "Ghi nhận quyết định sau mỗi buổi Daily Standup."),
        ("Google Calendar", "Theo dõi lịch nộp bài và các mốc deadline.")
    ], top_accent=PRIMARY, icon="📝")

    add_bento_box(s9, Inches(6.8), Inches(4.4), Inches(5.6), Inches(2.5), "Postman & Python Automated Testing", [
        ("Postman Collection", "Lưu trữ bộ API test cho các endpoint /api/v1/*."),
        ("unittest Framework", "Bộ 15 test cases tự động kiểm thử toàn diện hệ thống."),
        ("Test Coverage", "Kiểm thử từ Logic Model, Form đến REST API.")
    ], top_accent=GREEN, icon="🚀")

    # =========================================================================
    # SLIDE 10: AGILE SCRUM 4 SPRINTS (Horizontal Roadmap)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "3. Quản lý dự án", "Quy Trình Lập Kế Hoạch 4 Sprints Theo Agile Scrum", "Thành viên 2", "🏃")

    sprint_w = Inches(2.7)
    sprints = [
        ("Sprint 1 (Tuần 1)", "Khảo Sát & Thiết Kế", ["Phân tích Pain points cổng cũ", "Phác thảo Wireframe Figma", "Thiết kế CSDL ERD 6 bảng"], PRIMARY),
        ("Sprint 2 (Tuần 2)", "Backend & Auth Core", ["Cấu hình Dual-Database", "Cơ chế Zero-SSO FPT Mail", "Thuật toán giữ chỗ Atomic", "Phân quyền RBAC"], BLUE),
        ("Sprint 3 (Tuần 3)", "Frontend & WebRTC", ["Giao diện Dark Tech BEM", "Nhúng QR Scanner Camera", "Dashboard quản trị CTSV", "Xuất file báo cáo CSV"], GREEN),
        ("Sprint 4 (Tuần 4)", "Test & Deploy Cloud", ["Bộ 15 Unit Tests tự động", "Kiểm thử bảo mật XSS/Redirect", "Deploy Vercel Serverless", "Hoàn thiện tài liệu Word"], PURPLE)
    ]

    for i, (s_name, s_goal, tasks, col) in enumerate(sprints):
        left_pos = Inches(0.8 + i * 2.9)
        c = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.6), sprint_w, Inches(5.2))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = col
        c.line.width = Pt(1.5)

        # Status badge top
        st = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos + Inches(0.2), Inches(1.8), sprint_w - Inches(0.4), Inches(0.35))
        st.fill.solid()
        st.fill.fore_color.rgb = GREEN_BG
        st.line.color.rgb = GREEN
        tf_st = st.text_frame
        p_st = tf_st.paragraphs[0]
        p_st.alignment = PP_ALIGN.CENTER
        r_st = p_st.add_run()
        r_st.text = "HOÀN THÀNH ✅"
        r_st.font.bold = True
        r_st.font.size = Pt(9.5)
        r_st.font.color.rgb = GREEN_LIGHT

        tb = s10.shapes.add_textbox(left_pos + Inches(0.15), Inches(2.3), sprint_w - Inches(0.3), Inches(4.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = s_name + "\n"
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = col

        r1_sub = p1.add_run()
        r1_sub.text = s_goal + "\n"
        r1_sub.font.bold = True
        r1_sub.font.size = Pt(11)
        r1_sub.font.color.rgb = TEXT_WHITE

        for t in tasks:
            p = tf.add_paragraph()
            p.space_before = Pt(8)
            r = p.add_run()
            r.text = f"• {t}"
            r.font.size = Pt(10.5)
            r.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 11: GITFLOW (Branching Strategy)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "3. Quản lý dự án", "Chiến Lược Phân Nhánh Mã Nguồn (Git Workflow)", "Thành viên 2", "🌿")

    add_bento_box(s11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Cấu Trúc Nhánh & Quy Trình Tích Hợp", [
        ("Nhánh main (Production)", "Chỉ chứa mã nguồn ổn định nhất, tự động kích hoạt CI/CD deploy Vercel."),
        ("Nhánh develop (Staging)", "Nơi tích hợp các tính năng sau khi đã test nội bộ thành công."),
        ("Nhánh feature/*", "Phát triển tính năng độc lập (e.g. feature/qr-scanner, feature/category-crud)."),
        ("Nhánh bugfix/*", "Xử lý nóng các lỗi phát hiện trong quá trình kiểm thử.")
    ], top_accent=PRIMARY, icon="🌳")

    add_bento_box(s11, Inches(6.8), Inches(1.6), Inches(5.6), Inches(5.2), "Quy Ước Conventional Commits", [
        ("feat: ...", "Tính năng mới (e.g. feat: add camera qr check-in)."),
        ("fix: ...", "Sửa lỗi (e.g. fix: resolve capacity double booking)."),
        ("docs: ...", "Cập nhật tài liệu, slide, báo cáo Word."),
        ("test: ...", "Bổ sung hoặc sửa đổi các bài unit test tự động."),
        ("refactor: ...", "Tối ưu hóa cấu trúc code không làm đổi tính năng."),
        ("Lợi ích", "Lịch sử commit rõ ràng, chuyên nghiệp chuẩn doanh nghiệp.")
    ], top_accent=BLUE, icon="📜")

    # =========================================================================
    # SLIDE 12: MILESTONES (Infographic Timeline)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "3. Quản lý dự án", "Tiến Độ Triển Khai Thực Tế & Đạt Chuẩn Milestones", "Thành viên 2", "🏁")

    add_kpi_card(s12, Inches(0.8), Inches(1.5), Inches(5.6), Inches(1.5), "100%", "Đúng Hạn Cam Kết", "Không có bất kỳ tính năng nào bị trễ deadline", GREEN)
    add_kpi_card(s12, Inches(6.8), Inches(1.5), Inches(5.6), Inches(1.5), "0 Lỗi", "Chất Lượng Vận Hành", "15/15 Unit Tests Pass, CSDL toàn vẹn", BLUE)

    add_bento_box(s12, Inches(0.8), Inches(3.2), Inches(11.6), Inches(3.6), "5 Cột Mốc Quan Trọng Đã Đạt Được (100% Passed)", [
        ("Cột mốc 1: Phê Duyệt Đề Tài", "Được giảng viên thông qua đề tài FPTU EventHub và kiến trúc tổng quan."),
        ("Cột mốc 2: CSDL & Zero-SSO", "Kết nối CSDL MS SQL Server, đăng nhập FPT Mail không cần đăng ký."),
        ("Cột mốc 3: Giữ Chỗ & Camera QR", "Hoàn thành giải thuật đặt vé không overbooking và quét QR trên Camera WebRTC."),
        ("Cột mốc 4: Kiểm Thử Toàn Diện", "Đạt 15/15 bài kiểm thử tự động, loại bỏ 100% lỗ hổng bảo mật Web."),
        ("Cột mốc 5: Triển Khai Cloud Vercel", "Hệ thống vận hành mượt mà 24/7 tại fptu-event-hub.vercel.app.")
    ], top_accent=GREEN, icon="🏆")

    # =========================================================================
    # SLIDE 13: MÔ HÌNH MVC (3 Tiers with Color-Coded Borders)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "4. Kiến trúc & Công nghệ", "Mô Hình Kiến Trúc Phần Mềm MVC (Model - View - Controller)", "Thành viên 3", "📐")

    add_bento_box(s13, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.2), "Model (models.py)", [
        ("SQLAlchemy ORM Models", "6 Thực thể dữ liệu: User, Role, Category, Event, Ticket, Review."),
        ("Logic Nghiệp Vụ", "Phương thức check_password, kiểm tra sức chứa, tính rating trung bình."),
        ("To Dict Serialization", "Chuẩn hóa dữ liệu sang JSON phục vụ REST API v1."),
        ("Cascade Delete", "Xóa sự kiện tự động dọn sạch vé con liên quan.")
    ], top_accent=BLUE, icon="📦")

    add_bento_box(s13, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.2), "View (templates/ & static/)", [
        ("Jinja2 Template Engine", "Server-Side Rendering (SSR) tối ưu SEO và tốc độ tải ban đầu."),
        ("Scoped CSS BEM", "Giao diện Dark Modern Tech, độc lập, không xung đột class."),
        ("Chuyển Theme Linh Hoạt", "Hỗ trợ Sáng / Tối lưu trạng thái tại LocalStorage."),
        ("Trang Lỗi Chuẩn Hóa", "Giao diện 400, 403, 404, 500 đồng bộ.")
    ], top_accent=PRIMARY, icon="🖥️")

    add_bento_box(s13, Inches(8.8), Inches(1.6), Inches(3.6), Inches(5.2), "Controller (app.py)", [
        ("Điều Phối Routing", "Xử lý toàn bộ các HTTP Request (GET, POST, PUT, DELETE)."),
        ("Decorator Phân Quyền", "@login_required, @admin_required, @role_required."),
        ("Transaction Management", "Quản lý đóng/mở phiên CSDL, commit an toàn, rollback khi lỗi."),
        ("RESTful API v1", "Cung cấp các endpoint chuẩn JSON.")
    ], top_accent=GREEN, icon="⚙️")

    # =========================================================================
    # SLIDE 14: VÒNG ĐỜI HTTP REQUEST & BẢO MẬT (5-Step Pipeline)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "4. Kiến trúc & Công nghệ", "Vòng Đời Xử Lý HTTP Request & Màng Lọc Bảo Mật 3 Lớp", "Thành viên 3", "🔄")

    # 5 Horizontal Pipeline Chips
    steps_pipeline = ["1. Client Request", "2. Vercel WSGI", "3. RBAC Guard", "4. Controller", "5. Database ORM"]
    for i, s_txt in enumerate(steps_pipeline):
        chip = s14.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(0.8 + i * 2.4), Inches(1.5), Inches(2.3), Inches(0.6))
        chip.fill.solid()
        chip.fill.fore_color.rgb = BLUE_BG if i < 4 else GREEN_BG
        chip.line.color.rgb = BLUE if i < 4 else GREEN
        tf_c = chip.text_frame
        pc = tf_c.paragraphs[0]
        pc.alignment = PP_ALIGN.CENTER
        rc = pc.add_run()
        rc.text = s_txt
        rc.font.bold = True
        rc.font.size = Pt(11)
        rc.font.color.rgb = TEXT_WHITE

    add_bento_box(s14, Inches(0.8), Inches(2.4), Inches(5.6), Inches(4.5), "Màng Lọc Bảo Mật 3 Lớp Chặt Chẽ", [
        ("Lớp 1: Endpoint Guard", "Chặn người chưa đăng nhập tại @app.before_request trừ các route công khai."),
        ("Lớp 2: Role Authorization", "Decorator @role_required ngăn chặn sinh viên can thiệp vào trang CTSV."),
        ("Lớp 3: Input Sanitization", "Bleach làm sạch toàn bộ văn bản Markdown, tước bỏ mã độc XSS."),
        ("Fail-Safe Rollback", "Tự động rollback phiên giao dịch và trả về trang 500 khi có lỗi.")
    ], top_accent=RED, icon="🛡️")

    add_bento_box(s14, Inches(6.8), Inches(2.4), Inches(5.6), Inches(4.5), "Luồng Xử Lý Dữ Liệu Hai Chiều", [
        ("Xác thực Token/Session", "Đọc cookie HttpOnly, kiểm tra chữ ký số phiên người dùng."),
        ("Truy vấn ORM Tham Số", "Sử dụng SQLAlchemy Parameterized Queries chống SQL Injection."),
        ("Phản Hồi Linh Hoạt", "Tự nhận diện kiểu Client: trả về HTML giao diện hoặc JSON REST API."),
        ("Ghi nhận Audit Log", "Lưu vết thời gian đặt vé, check-in và hủy vé minh bạch.")
    ], top_accent=GREEN, icon="⚡")

    # =========================================================================
    # SLIDE 15: CSDL ERD 6 BẢNG (Bento Grid of Tables)
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "4. Kiến trúc & Công nghệ", "Thiết Kế Cơ Sở Dữ Liệu ERD (6 Bảng Chuẩn Hóa)", "Thành viên 3", "🗄️")

    tables = [
        ("roles", "Phân quyền người dùng", [("id", "PK, Integer"), ("name", "String (Student, Admin)"), ("description", "String")]),
        ("users", "Tài khoản FPTU", [("id", "PK, Integer"), ("student_id", "MSSV (Unique)"), ("email", "Unique (@fpt.edu.vn)"), ("role_id", "FK -> roles.id")]),
        ("categories", "Danh mục sự kiện", [("id", "PK, Integer"), ("name", "Tên nhóm hoạt động"), ("slug", "Unique URL slug"), ("color", "Mã màu HEX")]),
        ("events", "Sự kiện & Hội thảo", [("id", "PK, Integer"), ("title", "Tiêu đề sự kiện"), ("available_slots", "Số ghế còn lại"), ("category_id", "FK -> categories.id")]),
        ("tickets", "Vé điện tử & Check-in", [("id", "PK, Integer"), ("ticket_code", "Unique (FU-2026-X89AD)"), ("status", "REGISTERED / CHECKED_IN"), ("event_id", "FK -> events.id (Cascade)")]),
        ("reviews", "Đánh giá chất lượng", [("id", "PK, Integer"), ("rating", "1 - 5 Sao"), ("comment", "Nội dung nhận xét"), ("event_id", "FK -> events.id")])
    ]

    for idx, (tname, tdesc, cols) in enumerate(tables):
        r_idx = idx // 3
        c_idx = idx % 3
        l_pos = Inches(0.8 + c_idx * 3.9)
        t_pos = Inches(1.6 + r_idx * 2.7)
        
        box = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l_pos, t_pos, Inches(3.7), Inches(2.45))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = CARD_BORDER
        box.line.width = Pt(1)

        # Header of table
        tb = s15.shapes.add_textbox(l_pos + Inches(0.1), t_pos + Inches(0.1), Inches(3.5), Inches(2.25))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = f"📊 {tname} "
        r0.font.bold = True
        r0.font.size = Pt(12.5)
        r0.font.color.rgb = PRIMARY
        
        r0_sub = p0.add_run()
        r0_sub.text = f"({tdesc})\n"
        r0_sub.font.size = Pt(9.5)
        r0_sub.font.color.rgb = TEXT_MUTED

        for col_name, col_type in cols:
            p = tf.add_paragraph()
            p.space_before = Pt(2)
            rcn = p.add_run()
            rcn.text = f"• {col_name}: "
            rcn.font.bold = True
            rcn.font.size = Pt(10)
            rcn.font.color.rgb = BLUE_LIGHT if "PK" in col_type or "FK" in col_type else TEXT_LIGHT
            
            rct = p.add_run()
            rct.text = col_type
            rct.font.size = Pt(9.5)
            rct.font.color.rgb = TEXT_GOLD if "PK" in col_type else (BLUE if "FK" in col_type else TEXT_MUTED)

    # =========================================================================
    # SLIDE 16: DUAL-DATABASE SWITCH (Visual Dual Architecture)
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "4. Kiến trúc & Công nghệ", "Điểm Sáng Kỹ Thuật: Cơ Chế Dual-Database Switch", "Thành viên 3", "🔀")

    add_bento_box(s16, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3), "MÔI TRƯỜNG LOCALHOST / PHÒNG LAB", [
        ("Hệ quản trị CSDL", "Microsoft SQL Server qua ODBC Driver 17."),
        ("Chuẩn học thuật PWD301", "Tuân thủ 100% giáo trình và bài thi của Đại học FPT."),
        ("Tự động nhận diện", "Code kiểm tra cổng kết nối SQL Server cục bộ, nếu có sẵn sẽ tự động kết nối qua chuỗi mssql+pyodbc."),
        ("Ưu điểm", "Dữ liệu lưu trữ bền vững trong hệ quản trị CSDL quan hệ chuẩn doanh nghiệp.")
    ], top_accent=BLUE, icon="🏢")

    add_bento_box(s16, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.3), "MÔI TRƯỜNG CLOUD (VERCEL SERVERLESS)", [
        ("Hệ quản trị CSDL", "SQLite Serverless được cấp phát động trong thư mục /tmp."),
        ("Nhận diện Cloud", "Mã nguồn tự động phát hiện biến môi trường VERCEL / AWS_LAMBDA."),
        ("Tự động Seed dữ liệu", "Khởi tạo sẵn 34 sinh viên, 8 sự kiện và 190 vé điện tử."),
        ("Lợi ích vượt trội", "Chạy mượt mà 24/7 trên Internet mà không tốn chi phí thuê máy chủ riêng.")
    ], top_accent=GREEN, icon="☁️")

    # =========================================================================
    # SLIDE 17: TECH STACK ECOSYSTEM (3 Categorical Bento Cards)
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "4. Kiến trúc & Công nghệ", "Hệ Sinh Thái Công Nghệ & Thư Viện Chuyên Dụng", "Thành viên 3", "💻")

    add_bento_box(s17, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.2), "Backend & ORM", [
        ("Python 3.11 / 3.14", "Ngôn ngữ hiệu năng cao, cú pháp hiện đại."),
        ("Flask Microframework", "Linh hoạt, nhẹ, dễ mở rộng tính năng."),
        ("SQLAlchemy 2.0", "ORM trừu tượng hóa, chống SQL Injection."),
        ("Flask-Login", "Quản lý phiên đăng nhập an toàn.")
    ], top_accent=PRIMARY, icon="🐍")

    add_bento_box(s17, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.2), "Bảo Mật & Kiểm Thực", [
        ("Bleach HTML Sanitizer", "Chống tấn công Stored XSS trong Markdown."),
        ("Werkzeug Security", "Băm mật khẩu PBKDF2/SHA-256 kèm Salt."),
        ("Flask-WTF & CSRF", "Bảo vệ form chống tấn công giả mạo yêu cầu."),
        ("is_safe_url()", "Chặn đứng lỗ hổng Open Redirect.")
    ], top_accent=RED, icon="🛡️")

    add_bento_box(s17, Inches(8.8), Inches(1.6), Inches(3.6), Inches(5.2), "Tương Tác & Real-Time", [
        ("html5-qrcode", "Quét mã QR qua Camera WebRTC MediaDevices."),
        ("Canvas Confetti", "Hiệu ứng pháo hoa chúc mừng check-in."),
        ("Google Calendar API", "Đồng bộ lịch cá nhân chỉ bằng 1-click."),
        ("CSV UTF-8 BOM", "Xuất file tiếng Việt mở không lỗi font.")
    ], top_accent=GREEN, icon="⚡")

    # =========================================================================
    # SLIDE 18: TÍNH NĂNG SINH VIÊN 1 (Zero-SSO & Khám phá với Event Poster)
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "5. Tính năng chính", "Phân Hệ Sinh Viên: Zero-SSO & Khám Phá Đa Chiều", "Thành viên 4", "🎓")

    if os.path.exists(IMG_AI):
        s18.shapes.add_picture(IMG_AI, Inches(0.8), Inches(1.6), Inches(4.8), Inches(5.2))

    add_bento_box(s18, Inches(5.9), Inches(1.6), Inches(6.6), Inches(5.2), "Trải Nghiệm Khám Phá & Đăng Nhập 1-Chạm", [
        ("Zero-Registration SSO", "Nhận diện tức thì email trường (@fpt.edu.vn / @fe.edu.vn), tự động bóc tách MSSV, không cần đăng ký tài khoản mới."),
        ("Nút 1-Click Demo Chấm Điểm", "Hỗ trợ Hội đồng đăng nhập tức thì với Trương Công Dũng (DE200433) hoặc Phòng CTSV (ADM001)."),
        ("Bộ Lọc 5 Danh Mục", "Lọc nhanh: Công nghệ, Học thuật, Kỹ năng mềm, Văn hóa CLB, Thể thao."),
        ("Instant Search", "Tìm kiếm theo tên sự kiện, diễn giả hoặc tên hội trường."),
        ("Countdown Timer", "Đồng hồ đếm ngược thời gian thực đến sự kiện gần nhất.")
    ], top_accent=PRIMARY, icon="✨")

    # =========================================================================
    # SLIDE 19: TÍNH NĂNG SINH VIÊN 2 (Giữ chỗ Atomic & Ví Vé QR Mockup)
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    add_header(s19, "5. Tính năng chính", "Phân Hệ Sinh Viên: Giữ Chỗ Atomic & Ví Vé QR Cá Nhân", "Thành viên 4", "🎟️")

    add_bento_box(s19, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.2), "Thuật Toán Giữ Chỗ & Ví Vé Thông Minh", [
        ("Giao Dịch Atomic Transaction", "Kiểm tra số ghế trống và trừ slot trong 1 phiên duy nhất, chống 100% tình trạng bán lố vé (Overbooking)."),
        ("Chặn Đăng Ký Trùng Lặp", "Mỗi sinh viên chỉ được đặt tối đa 1 vé cho mỗi sự kiện."),
        ("Hủy Vé Tự Động Hoàn Slot", "Sinh viên bận việc có thể bấm Hủy vé 1-click &rarr; hệ thống tự hoàn lại slot ghế trống cho bạn khác."),
        ("Ví 'Vé Của Tôi'", "Quản lý toàn bộ vé đã đăng ký, vé đã check-in và vé đã hủy."),
        ("Giấy Chứng Nhận E-Cert", "Sau khi check-in thành công, hệ thống tự cấp E-Certificate có mã xác thực.")
    ], top_accent=GREEN, icon="⚡")

    # Right: Ticket Visual Card Mockup
    tc = s19.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.2), Inches(1.6), Inches(5.3), Inches(5.2))
    tc.fill.solid()
    tc.fill.fore_color.rgb = CARD_BG
    tc.line.color.rgb = PRIMARY
    tc.line.width = Pt(2)

    tb_tc = s19.shapes.add_textbox(Inches(7.5), Inches(1.8), Inches(4.7), Inches(4.7))
    tf_tc = tb_tc.text_frame
    tf_tc.word_wrap = True

    p_tt = tf_tc.paragraphs[0]
    p_tt.alignment = PP_ALIGN.CENTER
    r_tt = p_tt.add_run()
    r_tt.text = "🎟️ VÉ ĐIỆN TỬ FPTU EVENTHUB\n"
    r_tt.font.bold = True
    r_tt.font.size = Pt(14)
    r_tt.font.color.rgb = PRIMARY

    p_tcode = tf_tc.add_paragraph()
    p_tcode.alignment = PP_ALIGN.CENTER
    p_tcode.space_before = Pt(4)
    r_tcode = p_tcode.add_run()
    r_tcode.text = "MÃ VÉ: FU-2026-AI001\n"
    r_tcode.font.bold = True
    r_tcode.font.size = Pt(16)
    r_tcode.font.color.rgb = TEXT_GOLD

    p_tdet = tf_tc.add_paragraph()
    p_tdet.space_before = Pt(10)
    r_tdet = p_tdet.add_run()
    r_tdet.text = (
        "• Sinh viên: Trương Công Dũng (DE200433)\n"
        "• Sự kiện: Workshop Làm Chủ AI Agentic Coding\n"
        "• Địa điểm: Hội trường Alpha (Tòa nhà Alpha)\n"
        "• Trạng thái: ĐÃ ĐIỂM DANH (CHECKED_IN)\n"
        "• Chứng nhận: E-Certificate Đã Cấp ✅"
    )
    r_tdet.font.size = Pt(11)
    r_tdet.font.color.rgb = TEXT_LIGHT

    # QR Icon simulation
    p_qr = tf_tc.add_paragraph()
    p_qr.alignment = PP_ALIGN.CENTER
    p_qr.space_before = Pt(16)
    r_qr = p_qr.add_run()
    r_qr.text = "📱 [QR CODE ĐỘNG - CHỐNG QUÉT LẶP]"
    r_qr.font.bold = True
    r_qr.font.size = Pt(12)
    r_qr.font.color.rgb = GREEN_LIGHT

    # =========================================================================
    # SLIDE 20: TÍNH NĂNG CTSV 1 (CRUD Sự kiện & Danh mục với Hackathon Image)
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    add_header(s20, "5. Tính năng chính", "Phân Hệ CTSV: Quản Lý Sự Kiện & Danh Mục CRUD", "Thành viên 5", "🛡️")

    add_bento_box(s20, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.2), "Quyền Năng Quản Trị Cán Bộ CTSV", [
        ("Tạo & Quản Lý Sự Kiện CRUD", "Form nhập liệu chuẩn Flask-WTF, cấu hình số lượng ghế, địa điểm, thời gian, banner poster."),
        ("Soạn Thảo Markdown Phong Phú", "Hỗ trợ định dạng bài viết đẹp mắt, tự động làm sạch mã độc bằng Bleach trước khi lưu CSDL."),
        ("Quản Lý Danh Mục (Category CRUD)", "Thêm, sửa, xóa 5 nhóm hoạt động chuẩn của trường."),
        ("Bảo Toàn Toàn Vẹn CSDL", "Chặn xóa danh mục nếu đang có sự kiện liên kết, chống lỗi mồ côi dữ liệu."),
        ("Tách Biệt Vai Trò RBAC", "Cán bộ CTSV là đơn vị tổ chức, không tham gia đặt vé như sinh viên.")
    ], top_accent=BLUE, icon="⚙️")

    if os.path.exists(IMG_HACK):
        s20.shapes.add_picture(IMG_HACK, Inches(7.2), Inches(1.6), Inches(5.3), Inches(5.2))

    # =========================================================================
    # SLIDE 21: TÍNH NĂNG CTSV 2 (Camera Check-in WebRTC & Dashboard CSV)
    # =========================================================================
    s21 = prs.slides.add_slide(blank_layout)
    add_header(s21, "5. Tính năng chính", "Phân Hệ CTSV: Check-in WebRTC & Thống Kê Real-Time", "Thành viên 5", "📊")

    add_bento_box(s21, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Bàn Check-in Camera WebRTC Tức Thì", [
        ("Mở Camera Trình Duyệt 1-Click", "Sử dụng MediaDevices API, không cần cài đặt thêm App di động."),
        ("Giải Mã Siêu Tốc < 1s", "Quét luồng video 10 fps, gửi AJAX ngầm về endpoint /api/check-in/scan."),
        ("Chống Điểm Danh Lặp Lại", "Cảnh báo màu vàng nếu vé đã check-in trước đó, ngăn chặn gian lận."),
        ("Nhập Tay Dự Phòng", "Có ô nhập mã vé nếu camera sinh viên bị mờ hoặc nứt vỡ.")
    ], top_accent=GREEN, icon="📷")

    add_bento_box(s21, Inches(6.8), Inches(1.6), Inches(5.6), Inches(5.2), "Dashboard Báo Cáo & Xuất File Excel", [
        ("Thống Kê Trực Quan Real-Time", "Theo dõi số vé phát hành, số người thực tế có mặt, tỷ lệ lấp đầy hội trường."),
        ("Xuất File CSV Chuẩn UTF-8 BOM", "Bấm 1-click tải danh sách người tham gia, mở trên Microsoft Excel chuẩn tiếng Việt có dấu."),
        ("Lưu Trữ Văn Thư", "Phục vụ đối soát danh sách sinh viên tham gia phong trào cho Phòng CTSV.")
    ], top_accent=PRIMARY, icon="📈")

    # =========================================================================
    # SLIDE 22: KỊCH BẢN LIVE DEMO (3-Step Roadmap)
    # =========================================================================
    s22 = prs.slides.add_slide(blank_layout)
    add_header(s22, "5. Tính năng chính", "Kịch Bản Trình Diễn Live Demo (8 - 10 Phút)", "Thành viên 4 & 5", "🎬")

    demo_steps = [
        ("Chặng 1: Sinh Viên (3 Phút)", "Đặt Vé & Ví QR Cá Nhân", [
            "Mở trang chủ, tìm kiếm Workshop AI.",
            "Đăng nhập Trương Công Dũng (DE200433).",
            "Bấm 'Đăng ký giữ chỗ ngay' &rarr; Nhận mã vé QR.",
            "Mở ví 'Vé Của Tôi', thử nghiệm hủy vé hoàn slot."
        ], PRIMARY),
        ("Chặng 2: CTSV (3 Phút)", "Check-in Camera WebRTC", [
            "Đăng nhập tài khoản Phòng CTSV (ADM001).",
            "Mở Bàn Check-in, bật Camera quét mã QR sinh viên.",
            "Xác thực thành công trong 0.5s &rarr; Bắn pháo hoa.",
            "Quét lại lần 2 &rarr; Hệ thống cảnh báo vé đã dùng."
        ], BLUE),
        ("Chặng 3: Kết Quả (2 Phút)", "Chứng Nhận & Báo Cáo CSV", [
            "Sinh viên mở lại trang &rarr; Nút Giấy chứng nhận kích hoạt.",
            "CTSV mở Dashboard, xem tỷ lệ lấp đầy cập nhật tức thì.",
            "Bấm 'Xuất danh sách CSV' &rarr; Mở file Excel tiếng Việt."
        ], GREEN)
    ]

    for idx, (stitle, sgoal, tasks, col) in enumerate(demo_steps):
        l_pos = Inches(0.8 + idx * 3.9)
        c = s22.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l_pos, Inches(1.6), Inches(3.7), Inches(5.2))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = col
        c.line.width = Pt(1.5)

        tb = s22.shapes.add_textbox(l_pos + Inches(0.15), Inches(1.75), Inches(3.4), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = stitle + "\n"
        r0.font.bold = True
        r0.font.size = Pt(13)
        r0.font.color.rgb = col

        r0_sub = p0.add_run()
        r0_sub.text = s_goal + "\n"
        r0_sub.font.bold = True
        r0_sub.font.size = Pt(11)
        r0_sub.font.color.rgb = TEXT_WHITE

        for t in tasks:
            p = tf.add_paragraph()
            p.space_before = Pt(8)
            r = p.add_run()
            r.text = f"• {t}"
            r.font.size = Pt(10.5)
            r.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 23: CHIẾN LƯỢC KIỂM THỬ (Testing Pyramid)
    # =========================================================================
    s23 = prs.slides.add_slide(blank_layout)
    add_header(s23, "6. Kiểm thử dự án", "Chiến Lược Kiểm Thử Toàn Diện (Testing Pyramid)", "Thành viên 5", "🧪")

    add_bento_box(s23, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.2), "TẦNG 1: Unit Testing", [
        ("Phạm vi kiểm thử", "Kiểm thử các hàm logic độc lập."),
        ("Các hàm trọng tâm", "Mã hóa PBKDF2, sinh mã vé FU-2026, custom validator SĐT 10 số (Lab 6), tính điểm rating."),
        ("Môi trường độc lập", "Khởi tạo database SQLite in-memory tự dọn dẹp sau mỗi bài test."),
        ("Độ tin cậy", "Đảm bảo từng đơn vị code chạy chính xác 100%.")
    ], top_accent=GREEN, icon="🧱")

    add_bento_box(s23, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.2), "TẦNG 2: Integration Testing", [
        ("Flask Test Client", "Giả lập HTTP Request kiểm thử toàn bộ luồng nghiệp vụ."),
        ("Giao Dịch Đặt Vé", "Kiểm thử trừ slot, hết vé, hủy vé hoàn slot."),
        ("Kiểm Thử REST API", "Gửi request đến các endpoint /api/v1/events, /api/v1/categories, /api/v1/stats."),
        ("Mã Lỗi HTTP", "Kiểm tra trả về đúng 200, 201, 400, 403, 404.")
    ], top_accent=BLUE, icon="🔗")

    add_bento_box(s23, Inches(8.8), Inches(1.6), Inches(3.6), Inches(5.2), "TẦNG 3: Security & UI Testing", [
        ("Kiểm Thử Bảo Mật", "Thử nghiệm tấn công XSS injection, Open Redirect URL, giả mạo quyền truy cập 403."),
        ("Kiểm Thử Responsive", "Hiển thị hoàn hảo trên Mobile (iPhone, Samsung), Tablet và Desktop."),
        ("Kiểm Thử Dark Mode", "Độ tương phản màu sắc đạt chuẩn tiếp cận WCAG.")
    ], top_accent=RED, icon="🛡️")

    # =========================================================================
    # SLIDE 24: KẾT QUẢ 15 TEST CASES (Pass 100% Bento Grid)
    # =========================================================================
    s24 = prs.slides.add_slide(blank_layout)
    add_header(s24, "6. Kiểm thử dự án", "Kết Quả Thực Thi 15 Test Cases Tự Động (Pass 100%)", "Thành viên 5", "✅")

    add_kpi_card(s24, Inches(0.8), Inches(1.5), Inches(5.6), Inches(1.5), "15 / 15 TESTS", "Tỷ Lệ Thành Công 100%", "Ran 15 tests - 0 Failures - 0 Errors", GREEN)
    add_kpi_card(s24, Inches(6.8), Inches(1.5), Inches(5.6), Inches(1.5), "7.28 Giây", "Tốc Độ Thực Thi", "Thực thi toàn bộ test suite trên SQLite Memory", BLUE)

    add_bento_box(s24, Inches(0.8), Inches(3.2), Inches(5.6), Inches(3.6), "Nhóm Test Logic & Nghiệp Vụ (1 - 8)", [
        ("test_user_password_hashing", "Mã hóa & kiểm tra mật khẩu PBKDF2. [PASS]"),
        ("test_event_capacity_and_sold_out", "Kiểm soát số ghế & trạng thái Sold Out. [PASS]"),
        ("test_ticket_creation_and_code_gen", "Sinh mã vé định danh FU-2026-XXXXXX. [PASS]"),
        ("test_booking_transaction", "Giao dịch trừ slot & đặt vé atomic. [PASS]"),
        ("test_ticket_cancellation_frees_slot", "Hủy vé tự động hoàn slot ghế. [PASS]")
    ], top_accent=GREEN, icon="🧪")

    add_bento_box(s24, Inches(6.8), Inches(3.2), Inches(5.6), Inches(3.6), "Nhóm Test Bảo Mật & REST API (9 - 15)", [
        ("test_custom_phone_validator", "Kiểm tra SĐT chuẩn 10 số (Lab 6). [PASS]"),
        ("test_open_redirect_safety_helper", "Chặn đứng URL chuyển hướng ngoài. [PASS]"),
        ("test_rest_api_events_list", "API danh sách sự kiện có phân trang. [PASS]"),
        ("test_rest_api_categories", "API danh mục sự kiện trả về JSON. [PASS]"),
        ("test_category_crud_and_integrity", "Kiểm tra bảo toàn CSDL khi xóa. [PASS]")
    ], top_accent=BLUE, icon="🌐")

    # =========================================================================
    # SLIDE 25: BẢO MẬT CHUYÊN SÂU (4 Shield Defense Cards)
    # =========================================================================
    s25 = prs.slides.add_slide(blank_layout)
    add_header(s25, "6. Kiểm thử dự án", "Kiểm Thử An Toàn Thông Tin & Phòng Chống Lỗ Hổng Web", "Thành viên 5", "🛡️")

    add_bento_box(s25, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.5), "01. Chống Tấn Công Stored XSS", [
        ("Payload thử nghiệm", "<script>alert('XSS')</script> hoặc <img onerror=steal()>."),
        ("Kết quả xử lý", "Thư viện Bleach làm sạch 100% mã độc, chỉ giữ lại định dạng an toàn.")
    ], top_accent=GREEN, icon="🛡️")

    add_bento_box(s25, Inches(6.8), Inches(1.6), Inches(5.6), Inches(2.5), "02. Chống Lỗ Hổng Open Redirect", [
        ("Payload thử nghiệm", "next=http://malicious-attacker-site.com/login."),
        ("Kết quả xử lý", "Hàm is_safe_url() kiểm tra netloc máy chủ, từ chối chuyển hướng ngoài.")
    ], top_accent=GREEN, icon="🔒")

    add_bento_box(s25, Inches(0.8), Inches(4.4), Inches(5.6), Inches(2.5), "03. Chống Tấn Công SQL Injection", [
        ("Kỹ thuật phòng thủ", "100% truy vấn qua SQLAlchemy ORM Parameterized Queries."),
        ("Kết quả xử lý", "Không có câu lệnh SQL raw nào, vô hiệu hóa hoàn toàn SQLi.")
    ], top_accent=GREEN, icon="🧱")

    add_bento_box(s25, Inches(6.8), Inches(4.4), Inches(5.6), Inches(2.5), "04. Chống CSRF & Vượt Quyền RBAC", [
        ("CSRF Protection", "Tất cả Form POST đều có csrf_token ẩn được kiểm tra nghiêm ngặt."),
        ("Phân quyền 403", "Sinh viên cố tình vào /admin/* nhận ngay mã lỗi 403 Forbidden.")
    ], top_accent=GREEN, icon="🚫")

    # =========================================================================
    # SLIDE 26: GRAND FINALE / Q&A
    # =========================================================================
    s26 = prs.slides.add_slide(blank_layout)
    set_slide_background(s26)

    # Top Bar
    bar26 = s26.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.12))
    bar26.fill.solid()
    bar26.fill.fore_color.rgb = PRIMARY
    bar26.line.fill.background()

    # Center Container Card
    c26 = s26.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(0.8), Inches(10.933), Inches(5.9))
    c26.fill.solid()
    c26.fill.fore_color.rgb = CARD_BG
    c26.line.color.rgb = PRIMARY
    c26.line.width = Pt(2)

    if os.path.exists(IMG_LOGO):
        s26.shapes.add_picture(IMG_LOGO, Inches(5.7), Inches(1.1), Inches(1.9), Inches(0.8))

    tb26 = s26.shapes.add_textbox(Inches(1.5), Inches(2.0), Inches(10.333), Inches(4.4))
    tf26 = tb26.text_frame
    tf26.word_wrap = True

    p_fn = tf26.paragraphs[0]
    p_fn.alignment = PP_ALIGN.CENTER
    r_fn = p_fn.add_run()
    r_fn.text = "TỔNG KẾT & ĐỊNH HƯỚNG TƯƠNG LAI\n"
    r_fn.font.bold = True
    r_fn.font.size = Pt(24)
    r_fn.font.color.rgb = PRIMARY

    p_val = tf26.add_paragraph()
    p_val.alignment = PP_ALIGN.CENTER
    p_val.space_before = Pt(8)
    r_val = p_val.add_run()
    r_val.text = (
        "FPTU EventHub đã giải quyết triệt để 4 bài toán đau đầu của cổng sự kiện truyền thống:\n"
        "Đăng nhập 1-Click FPT Mail • Giữ chỗ Atomic không overbooking • Check-in Camera WebRTC < 1s • Cấp chứng nhận tự động.\n\n"
        "Định hướng phát triển: Tích hợp gửi mã vé qua Zalo ZNS / SMS và ứng dụng AI gợi ý sự kiện cá nhân hóa."
    )
    r_val.font.size = Pt(12.5)
    r_val.font.color.rgb = TEXT_LIGHT

    p_ty = tf26.add_paragraph()
    p_ty.alignment = PP_ALIGN.CENTER
    p_ty.space_before = Pt(24)
    r_ty = p_ty.add_run()
    r_ty.text = "XIN TRÂN TRỌNG CẢM ƠN QUÝ THẦY CÔ TRONG HỘI ĐỒNG!\n"
    r_ty.font.bold = True
    r_ty.font.size = Pt(20)
    r_ty.font.color.rgb = BLUE

    p_qa = tf26.add_paragraph()
    p_qa.alignment = PP_ALIGN.CENTER
    p_qa.space_before = Pt(4)
    r_qa = p_qa.add_run()
    r_qa.text = "Nhóm chúng em sẵn sàng lắng nghe câu hỏi và nhận xét từ Quý Thầy Cô (Q&A Session)."
    r_qa.font.size = Pt(13)
    r_qa.font.color.rgb = TEXT_GOLD

    out_file = r"C:\Users\truon\fptu_eventhub\SLIDE_THUYET_TRINH_FPTU_EVENTHUB.pptx"
    prs.save(out_file)
    print(f"Canva-style presentation generated successfully at: {out_file}")

if __name__ == "__main__":
    build_deck()
