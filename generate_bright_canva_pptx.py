# -*- coding: utf-8 -*-
"""
Canva-Style Light & Bright Presentation Deck Generator for FPTU EventHub (26 Slides, 45-50 Mins)
Design Highlights:
- Bright Modern Canva Aesthetic: Pristine Slate-50 background, crisp white cards with soft slate borders.
- Vibrant FPT Colors: High contrast FPT Orange (#EA580C / #F26F21), Royal Sky Blue (#0284C7), Emerald Green (#059669), Coral Red (#DC2626), Violet (#7C3AED).
- Bold Dark Typography: Deep Charcoal (#0F172A) titles and Slate-700 body text for razor-sharp projection readability.
- Big KPI Callouts, Battle Board (Cổng Cũ vs EventHub), Persona Cards for 5 Members, Browser Mockup for Live Demo.
- Real high-res photos embedded from static/images/ (Campus Hero, AI Workshop, Hackathon, Festival).
- Strictly NO PDP / rèn luyện points mentioned anywhere.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_bright_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- Modern Bright Palette ---
    BG_LIGHT = RGBColor(248, 250, 252)       # Slate 50 (Airy, clean canvas)
    CARD_WHITE = RGBColor(255, 255, 255)     # Pure White Card
    CARD_BORDER = RGBColor(226, 232, 240)    # Slate 200 Border
    CARD_BORDER_DARK = RGBColor(203, 213, 225) # Slate 300

    PRIMARY = RGBColor(242, 111, 33)         # FPT Vibrant Orange
    PRIMARY_DARK = RGBColor(194, 65, 12)     # Deep Orange 700
    PRIMARY_TINT = RGBColor(255, 247, 237)   # Orange 50 (Soft warm background)
    PRIMARY_BORDER = RGBColor(254, 215, 170) # Orange 200

    BLUE = RGBColor(2, 132, 199)             # Sky Blue 600
    BLUE_DARK = RGBColor(3, 105, 161)        # Sky Blue 700
    BLUE_TINT = RGBColor(240, 249, 255)      # Sky 50
    BLUE_BORDER = RGBColor(186, 230, 253)    # Sky 200

    GREEN = RGBColor(16, 185, 129)           # Emerald 500
    GREEN_DARK = RGBColor(5, 150, 105)       # Emerald 600
    GREEN_TINT = RGBColor(236, 253, 245)     # Emerald 50
    GREEN_BORDER = RGBColor(167, 243, 208)   # Emerald 200

    RED = RGBColor(239, 68, 68)              # Coral Red 500
    RED_DARK = RGBColor(220, 38, 38)         # Red 600
    RED_TINT = RGBColor(254, 242, 242)       # Red 50
    RED_BORDER = RGBColor(254, 202, 202)     # Red 200

    PURPLE = RGBColor(124, 58, 237)          # Violet 600
    PURPLE_TINT = RGBColor(245, 243, 255)    # Violet 50
    PURPLE_BORDER = RGBColor(221, 214, 254)  # Violet 200

    AMBER = RGBColor(217, 119, 6)            # Amber 600
    AMBER_TINT = RGBColor(254, 243, 199)     # Amber 50
    AMBER_BORDER = RGBColor(253, 230, 138)   # Amber 200

    # Typography Colors (High Contrast on White)
    TEXT_HEAD = RGBColor(15, 23, 42)         # Deep Midnight Slate 900
    TEXT_SUB = RGBColor(51, 65, 85)          # Slate 700
    TEXT_MUTED = RGBColor(100, 116, 139)     # Slate 500
    TEXT_WHITE = RGBColor(255, 255, 255)

    IMG_DIR = r"C:\Users\truon\fptu_eventhub\static\images"
    IMG_HERO = os.path.join(IMG_DIR, "fpt_campus_hero.jpg")
    IMG_LOGO = os.path.join(IMG_DIR, "fpt_logo.jpg")
    IMG_AI = os.path.join(IMG_DIR, "events", "workshop_ai.jpg")
    IMG_HACK = os.path.join(IMG_DIR, "events", "hackathon.jpg")
    IMG_CAREER = os.path.join(IMG_DIR, "events", "fsoft_career.jpg")
    IMG_FESTIVAL = os.path.join(IMG_DIR, "events", "club_festival.jpg")
    IMG_VOVINAM = os.path.join(IMG_DIR, "events", "vovinam.jpg")

    def set_bright_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_LIGHT
        bg.line.fill.background()

        # Top Accent Ribbon (Orange + Amber dual gradient feel)
        ribbon1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(8.0), Inches(0.08))
        ribbon1.fill.solid()
        ribbon1.fill.fore_color.rgb = PRIMARY
        ribbon1.line.fill.background()

        ribbon2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.0), 0, Inches(5.333), Inches(0.08))
        ribbon2.fill.solid()
        ribbon2.fill.fore_color.rgb = BLUE
        ribbon2.line.fill.background()

        # Bottom Clean Footer
        ft_tb = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.35))
        ft_p = ft_tb.text_frame.paragraphs[0]
        r1 = ft_p.add_run()
        r1.text = "FPTU EventHub 2026  •  Hệ Thống Quản Trị Sự Kiện FPT University  •  Live: "
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = TEXT_MUTED

        r2 = ft_p.add_run()
        r2.text = "fptu-event-hub.vercel.app"
        r2.font.bold = True
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = PRIMARY_DARK
        return bg

    def add_header(slide, tag, title, presenter="", icon="⚡"):
        set_bright_bg(slide)

        # Tag Pill (Top Left)
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.32), Inches(3.2), Inches(0.36))
        pill.fill.solid()
        pill.fill.fore_color.rgb = PRIMARY_TINT
        pill.line.color.rgb = PRIMARY_BORDER
        pill.line.width = Pt(1)
        tf_p = pill.text_frame
        p_p = tf_p.paragraphs[0]
        p_p.alignment = PP_ALIGN.CENTER
        r_p = p_p.add_run()
        r_p.text = f"{icon}  {tag.upper()}"
        r_p.font.bold = True
        r_p.font.size = Pt(10.5)
        r_p.font.color.rgb = PRIMARY_DARK

        # Presenter Pill (Top Right)
        if presenter:
            p_pres = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.833), Inches(0.32), Inches(3.7), Inches(0.36))
            p_pres.fill.solid()
            p_pres.fill.fore_color.rgb = BLUE_TINT
            p_pres.line.color.rgb = BLUE_BORDER
            p_pres.line.width = Pt(1)
            tf_pr = p_pres.text_frame
            pp = tf_pr.paragraphs[0]
            pp.alignment = PP_ALIGN.CENTER
            rr = pp.add_run()
            rr.text = f"🎤 {presenter}"
            rr.font.bold = True
            rr.font.size = Pt(10.5)
            rr.font.color.rgb = BLUE_DARK

        # Main Title Box
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.733), Inches(0.7))
        p = tb.text_frame.paragraphs[0]
        r = p.add_run()
        r.text = title
        r.font.bold = True
        r.font.size = Pt(23)
        r.font.color.rgb = TEXT_HEAD

    def add_kpi_card(slide, left, top, width, height, number_str, label_str, subtext="", color=PRIMARY, bg_color=CARD_WHITE, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        # Subtle top stripe
        strip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.06))
        strip.fill.solid()
        strip.fill.fore_color.rgb = color
        strip.line.fill.background()

        tb = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.12), width - Inches(0.3), height - Inches(0.24))
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
        r2.font.color.rgb = TEXT_HEAD

        if subtext:
            p3 = tf.add_paragraph()
            p3.alignment = PP_ALIGN.CENTER
            p3.space_before = Pt(2)
            r3 = p3.add_run()
            r3.text = subtext
            r3.font.size = Pt(9.5)
            r3.font.color.rgb = TEXT_MUTED

    def add_bento_box(slide, left, top, width, height, title, items, top_accent=PRIMARY, bg_color=CARD_WHITE, border_color=CARD_BORDER, icon="📌"):
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        box.fill.solid()
        box.fill.fore_color.rgb = bg_color
        box.line.color.rgb = border_color
        box.line.width = Pt(1.2)

        # Top Accent Strip
        strip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.08))
        strip.fill.solid()
        strip.fill.fore_color.rgb = top_accent
        strip.line.fill.background()

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.16), width - Inches(0.4), height - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = f"{icon} {title}"
        r0.font.bold = True
        r0.font.size = Pt(13.5)
        r0.font.color.rgb = TEXT_HEAD

        for it in items:
            p = tf.add_paragraph()
            p.space_before = Pt(5)
            if isinstance(it, tuple):
                bold_txt, norm_txt = it
                r_b = p.add_run()
                r_b.text = f"• {bold_txt}: "
                r_b.font.bold = True
                r_b.font.size = Pt(10.5)
                r_b.font.color.rgb = top_accent
                
                r_n = p.add_run()
                r_n.text = norm_txt
                r_n.font.size = Pt(10.5)
                r_n.font.color.rgb = TEXT_SUB
            else:
                r = p.add_run()
                r.text = f"• {it}"
                r.font.size = Pt(10.5)
                r.font.color.rgb = TEXT_SUB

    # =========================================================================
    # SLIDE 1: COVER SLIDE (Canva Hero Split with Campus Photo)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bright_bg(s1)

    # Right side: Framed Campus Hero Photo
    if os.path.exists(IMG_HERO):
        s1.shapes.add_picture(IMG_HERO, Inches(7.5), Inches(0.85), Inches(5.1), Inches(5.8))
        # Sleek border frame
        frame = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.5), Inches(0.85), Inches(5.1), Inches(5.8))
        frame.fill.background()
        frame.line.color.rgb = PRIMARY
        frame.line.width = Pt(2)

    # Floating Glassmorphism Badges over Image
    b_top = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.15), Inches(4.5), Inches(0.55))
    b_top.fill.solid()
    b_top.fill.fore_color.rgb = CARD_WHITE
    b_top.line.color.rgb = GREEN_BORDER
    b_top.line.width = Pt(1.5)
    tf_bt = b_top.text_frame
    p_bt = tf_bt.paragraphs[0]
    p_bt.alignment = PP_ALIGN.CENTER
    r_bt = p_bt.add_run()
    r_bt.text = "🟢 LIVE PRODUCTION: fptu-event-hub.vercel.app"
    r_bt.font.bold = True
    r_bt.font.size = Pt(10)
    r_bt.font.color.rgb = GREEN_DARK

    b_bot = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(5.85), Inches(4.5), Inches(0.65))
    b_bot.fill.solid()
    b_bot.fill.fore_color.rgb = CARD_WHITE
    b_bot.line.color.rgb = PRIMARY_BORDER
    b_bot.line.width = Pt(1.5)
    tf_bb = b_bot.text_frame
    p_bb = tf_bb.paragraphs[0]
    p_bb.alignment = PP_ALIGN.CENTER
    r_bb = p_bb.add_run()
    r_bb.text = "⚡ Quét Vé QR Camera < 1s  •  Khóa Chỗ Atomic SQL"
    r_bb.font.bold = True
    r_bb.font.size = Pt(10)
    r_bb.font.color.rgb = PRIMARY_DARK

    # Left side: Typography Card
    if os.path.exists(IMG_LOGO):
        s1.shapes.add_picture(IMG_LOGO, Inches(0.8), Inches(0.85), Inches(1.8), Inches(0.7))

    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(6.3), Inches(5.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p_sub = tf1.paragraphs[0]
    r_sub = p_sub.add_run()
    r_sub.text = "TRƯỜNG ĐẠI HỌC FPT — BẢO VỆ ĐỒ ÁN CHUYÊN NGÀNH CNTT\n"
    r_sub.font.bold = True
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = BLUE_DARK

    p_main = tf1.add_paragraph()
    p_main.space_before = Pt(3)
    r_main = p_main.add_run()
    r_main.text = "FPTU EventHub\n"
    r_main.font.bold = True
    r_main.font.size = Pt(40)
    r_main.font.color.rgb = PRIMARY

    p_desc = tf1.add_paragraph()
    r_desc = p_desc.add_run()
    r_desc.text = "NỀN TẢNG QUẢN LÝ & ĐIỀU HÀNH SỰ KIỆN SINH VIÊN TOÀN DIỆN\n"
    r_desc.font.bold = True
    r_desc.font.size = Pt(13.5)
    r_desc.font.color.rgb = TEXT_HEAD

    p_sub2 = tf1.add_paragraph()
    p_sub2.space_before = Pt(8)
    r_sub2 = p_sub2.add_run()
    r_sub2.text = (
        "• Tự động hóa 100% quy trình: Zero-SSO 1-Click FPT Mail\n"
        "• Giữ chỗ thời gian thực không overbooking • Check-in WebRTC Camera < 1s\n"
        "• Công nghệ: Python 3.11 / Flask, SQLAlchemy ORM, Vercel Serverless"
    )
    r_sub2.font.size = Pt(11)
    r_sub2.font.color.rgb = TEXT_SUB

    p_team = tf1.add_paragraph()
    p_team.space_before = Pt(14)
    r_team = p_team.add_run()
    r_team.text = "👥 Nhóm thực hiện: Trương Công Dũng (Lead) cùng 4 thành viên (50 phút)"
    r_team.font.bold = True
    r_team.font.size = Pt(11.5)
    r_team.font.color.rgb = AMBER

    # =========================================================================
    # SLIDE 2: BỐI CẢNH & NHU CẦU CHUYỂN ĐỔI SỐ
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "1. Giới thiệu dự án", "Bối Cảnh & Nhu Cầu Chuyển Đổi Số Sự Kiện FPTU", "Thành viên 1: Trương Công Dũng", "🏫")

    add_kpi_card(s2, Inches(0.8), Inches(1.5), Inches(3.6), Inches(1.4), "30+ CLB", "Phong Trào Bùng Nổ", "Học thuật, công nghệ, văn hóa, thể thao", PRIMARY, PRIMARY_TINT, PRIMARY_BORDER)
    add_kpi_card(s2, Inches(4.8), Inches(1.5), Inches(3.6), Inches(1.4), "100+ Buổi/Kỳ", "Tần Suất Liên Tục", "Workshop, Hackathon, Talkshow OJT", BLUE, BLUE_TINT, BLUE_BORDER)
    add_kpi_card(s2, Inches(8.8), Inches(1.5), Inches(3.6), Inches(1.4), "100 - 250", "Sức Chứa Giới Hạn", "Hội trường Alpha/Beta & Lab AI", GREEN, GREEN_TINT, GREEN_BORDER)

    add_bento_box(s2, Inches(0.8), Inches(3.1), Inches(6.8), Inches(3.7), "Thực Trạng Năng Động & Thách Thức Không Gian", [
        ("Áp lực kiểm soát sức chứa", "Hội trường và phòng Lab có số máy cố định, không thể nhận dư sinh viên."),
        ("Kỳ vọng thế hệ Gen Z", "Muốn thao tác 1-chạm trên smartphone, có vé định danh, không muốn xếp hàng ký giấy."),
        ("Yêu cầu từ Cán bộ CTSV", "Cần một hệ thống quản trị thống nhất thay thế các bảng tính Excel rời rạc.")
    ], top_accent=PRIMARY, bg_color=CARD_WHITE, icon="🎯")

    if os.path.exists(IMG_FESTIVAL):
        s2.shapes.add_picture(IMG_FESTIVAL, Inches(7.9), Inches(3.1), Inches(4.6), Inches(3.7))
        tag_f = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.1), Inches(6.25), Inches(4.2), Inches(0.45))
        tag_f.fill.solid()
        tag_f.fill.fore_color.rgb = CARD_WHITE
        tag_f.line.color.rgb = PRIMARY_BORDER
        tf_tf = tag_f.text_frame
        ptf = tf_tf.paragraphs[0]
        ptf.alignment = PP_ALIGN.CENTER
        rtf = ptf.add_run()
        rtf.text = "📸 Lễ Hội CLB & Hoạt Động Sự Kiện FPTU"
        rtf.font.bold = True
        rtf.font.size = Pt(10)
        rtf.font.color.rgb = PRIMARY_DARK

    # =========================================================================
    # SLIDE 3: 4 THÁCH THỨC TỪ CỔNG CŨ & THỰC TẾ SỰ KIỆN FPTU
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "1. Giới thiệu dự án", "4 Thách Thức Từ Cổng Cũ & Thực Tế Sự Kiện FPTU", "Thành viên 1: Trương Công Dũng", "⚠️")

    add_bento_box(s3, Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.6), "01. Vỡ Trận Sức Chứa (Overbooking)", [
        ("Không khóa tự động khi đua vé", "Cổng cũ không ngắt đăng ký tức thời khi lượng sinh viên bấm cùng lúc."),
        ("Vượt quá sức chứa hội trường", "Hội trường 100 ghế nhưng sinh viên đăng ký dư quá tải, khó điều phối.")
    ], top_accent=RED, bg_color=RED_TINT, border_color=RED_BORDER, icon="🚨")

    add_bento_box(s3, Inches(6.8), Inches(1.5), Inches(5.6), Inches(2.6), "02. Vấn Nạn 'Ghế Ảo' (Không Đi)", [
        ("Tham gia hoàn toàn tự nguyện", "Việc sinh viên tham gia sự kiện là tùy ý mỗi cá nhân."),
        ("Không có nút hủy vé", "Sinh viên bận không nhường ghế được, hệ thống báo hết vé nhưng hội trường trống ghế.")
    ], top_accent=RED, bg_color=RED_TINT, border_color=RED_BORDER, icon="🎟️")

    add_bento_box(s3, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.6), "03. Bất Tiện Cho Bạn Quản Lý Quét Mã", [
        ("Người quản lý đứng quét mã tại cửa", "Khi đến sự kiện có bạn quản lý quét mã vé thì sinh viên mới được điểm danh."),
        ("Thao tác cồng kềnh, dễ nghẽn", "Hệ thống cũ cần app riêng, dễ chậm khi sinh viên vào đông và thiếu cảnh báo vé quét trùng.")
    ], top_accent=RED, bg_color=RED_TINT, border_color=RED_BORDER, icon="📱")

    add_bento_box(s3, Inches(6.8), Inches(4.3), Inches(5.6), Inches(2.6), "04. Dữ Liệu Điểm Danh Không Đồng Bộ", [
        ("CTSV không thấy sĩ số tức thì", "Số lượng sinh viên thực tế đến hội trường không được cập nhật ngay."),
        ("Phải tổng hợp thủ công sau sự kiện", "Ban tổ chức mất thời gian gộp dữ liệu báo cáo sau khi sự kiện kết thúc.")
    ], top_accent=RED, bg_color=RED_TINT, border_color=RED_BORDER, icon="📊")

    # =========================================================================
    # SLIDE 4: MỤC TIÊU & TẦM NHÌN ĐỘT PHÁ
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "1. Giới thiệu dự án", "Mục Tiêu Đột Phá Của FPTU EventHub", "Thành viên 1: Trương Công Dũng", "🎯")

    add_kpi_card(s4, Inches(0.8), Inches(1.5), Inches(3.6), Inches(1.4), "0.1 Giây", "Đặt Vé Giữ Chỗ", "Transaction nguyên tử, chống overbooking", PRIMARY, PRIMARY_TINT, PRIMARY_BORDER)
    add_kpi_card(s4, Inches(4.8), Inches(1.5), Inches(3.6), Inches(1.4), "< 1 Giây", "Quét QR Check-in", "Bạn quản lý quét camera WebRTC trên web", GREEN, GREEN_TINT, GREEN_BORDER)
    add_kpi_card(s4, Inches(8.8), Inches(1.5), Inches(3.6), Inches(1.4), "100%", "Tự Động Hóa", "Cấp vé QR, hủy vé nhả slot, đồng bộ CTSV", BLUE, BLUE_TINT, BLUE_BORDER)

    add_bento_box(s4, Inches(0.8), Inches(3.1), Inches(6.8), Inches(3.7), "3 Trụ Cột Đổi Mới Căn Bản", [
        ("Thời gian thực (Real-time Booking)", "Đồng bộ tức thì số vé còn lại, đóng form ngay khi hết ghế."),
        ("Chấm dứt vấn nạn ghế ảo", "Sinh viên chủ động hủy vé khi có việc bận, giải phóng slot cho bạn khác."),
        ("Bàn quét WebRTC cho bạn quản lý", "Quét trực tiếp trên trình duyệt web, không cần cài app, chặn vé quét trùng tức thì.")
    ], top_accent=BLUE, bg_color=CARD_WHITE, icon="🚀")

    if os.path.exists(IMG_AI):
        s4.shapes.add_picture(IMG_AI, Inches(7.9), Inches(3.1), Inches(4.6), Inches(3.7))
        tag_a = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.1), Inches(6.25), Inches(4.2), Inches(0.45))
        tag_a.fill.solid()
        tag_a.fill.fore_color.rgb = CARD_WHITE
        tag_a.line.color.rgb = BLUE_BORDER
        tf_ta = tag_a.text_frame
        pta = tf_ta.paragraphs[0]
        pta.alignment = PP_ALIGN.CENTER
        rta = pta.add_run()
        rta.text = "📸 Workshop Công Nghệ & AI Tại Hội Trường Alpha"
        rta.font.bold = True
        rta.font.size = Pt(10)
        rta.font.color.rgb = BLUE_DARK

    # =========================================================================
    # SLIDE 5: BATTLE BOARD - SO SÁNH TRỰC QUAN
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "1. Giới thiệu dự án", "Bảng So Sánh Đối Đầu: Cổng Cũ vs FPTU EventHub", "Thành viên 1: Trương Công Dũng", "⚔️")

    # Left: Red Tint Card (Old System)
    add_bento_box(s5, Inches(0.8), Inches(1.5), Inches(5.4), Inches(5.3), "❌ CỔNG CŨ CỦA TRƯỜNG", [
        ("Không kiểm soát sức chứa thời gian thực", "Dễ dẫn đến quá tải số lượng khi mở đăng ký sự kiện hot."),
        ("Không có nút hủy vé", "Sinh viên bận không nhường ghế được, dẫn đến tình trạng ghế trống ảo."),
        ("Bạn quản lý phải dùng app riêng", "Thao tác quét mã cồng kềnh, dễ chậm khi sinh viên vào đông."),
        ("Không cảnh báo vé quét lại", "Nguy cơ quét hộ hoặc vé bị tái sử dụng mà không phát hiện kịp thời."),
        ("Dữ liệu điểm danh rời rạc", "Cán bộ CTSV không theo dõi được sĩ số thực tế theo thời gian thực."),
        ("Tổng hợp báo cáo thủ công", "Mất nhiều thời gian sau sự kiện để có được số liệu tổng kết.")
    ], top_accent=RED, bg_color=RED_TINT, border_color=RED_BORDER, icon="⚠️")

    # Middle: VS Circular Badge
    vs_circle = s5.shapes.add_shape(MSO_SHAPE.OVAL, Inches(6.3), Inches(3.8), Inches(0.8), Inches(0.8))
    vs_circle.fill.solid()
    vs_circle.fill.fore_color.rgb = PRIMARY
    vs_circle.line.color.rgb = CARD_WHITE
    vs_circle.line.width = Pt(2)
    tf_vs = vs_circle.text_frame
    p_vs = tf_vs.paragraphs[0]
    p_vs.alignment = PP_ALIGN.CENTER
    r_vs = p_vs.add_run()
    r_vs.text = "VS"
    r_vs.font.bold = True
    r_vs.font.size = Pt(14)
    r_vs.font.color.rgb = TEXT_WHITE

    # Right: Emerald Tint Card (EventHub)
    add_bento_box(s5, Inches(7.133), Inches(1.5), Inches(5.4), Inches(5.3), "✅ FPTU EVENTHUB ĐỘT PHÁ 2026", [
        ("Khóa chỗ tự động bằng Transaction", "Hết ghế tự ngắt đăng ký trong 0.1s, chống overbooking tuyệt đối."),
        ("Hủy vé tức thì hoàn slot", "Sinh viên chủ động trả lại vé, giải phóng ghế cho bạn khác ngay."),
        ("Bàn Check-in WebRTC tiện lợi", "Bạn quản lý mở ngay trên web điện thoại/laptop quét mã < 1s."),
        ("Chống gian lận quét trùng", "Vé đã quét lập tức báo đỏ 'Đã check-in' và ghi nhận thời gian thực."),
        ("Dashboard đồng bộ CTSV", "Theo dõi sĩ số sinh viên có mặt ngay lập tức và xuất Excel 1-click."),
        ("Trải nghiệm linh hoạt tự nguyện", "Tôn trọng quyền tự do tham gia của sinh viên, thao tác minh bạch.")
    ], top_accent=GREEN, bg_color=GREEN_TINT, border_color=GREEN_BORDER, icon="🌟")

    # =========================================================================
    # SLIDE 6: MÔ HÌNH ĐỊNH VỊ GIÁ TRỊ (3 Trụ Cột)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "1. Giới thiệu dự án", "Mô Hình Định Vị Giá Trị Cho Từng Đối Tượng", "Thành viên 1: Trương Công Dũng", "💎")

    add_bento_box(s6, Inches(0.8), Inches(1.5), Inches(3.644), Inches(5.3), "Dành Cho Sinh Viên", [
        ("Thao tác 1-chạm", "Xem lịch sự kiện toàn trường tập trung, đăng ký bằng email FPT."),
        ("Vé QR thông minh", "Lưu trữ vé cá nhân, đối soát nhanh gọn tại cửa ra vào."),
        ("Chủ động lịch trình", "Hủy vé linh hoạt khi có việc đột xuất, tránh lãng phí ghế."),
        ("Hồ sơ năng lực", "Lưu lại toàn bộ lịch sử tham gia hội thảo, workshop, hackathon.")
    ], top_accent=PRIMARY, bg_color=PRIMARY_TINT, border_color=PRIMARY_BORDER, icon="🎓")

    add_bento_box(s6, Inches(4.844), Inches(1.5), Inches(3.644), Inches(5.3), "Dành Cho CTSV & Ban Tổ Chức", [
        ("Không lo vỡ trận", "Giới hạn sức chứa cứng (Capacity Lock), không bị quá tải hội trường."),
        ("Bàn quét QR chuyên nghiệp", "Hỗ trợ camera laptop/điện thoại, cảnh báo vé trùng/vé giả."),
        ("Quản lý danh sách trực quan", "Theo dõi ai đã đến, ai chưa đến theo thời gian thực."),
        ("Xuất dữ liệu 1-click", "Xuất file Excel danh sách tham dự đầy đủ phục vụ lưu trữ.")
    ], top_accent=BLUE, bg_color=BLUE_TINT, border_color=BLUE_BORDER, icon="🛡️")

    add_bento_box(s6, Inches(8.888), Inches(1.5), Inches(3.644), Inches(5.3), "Dành Cho Nhà Trường (FPTU)", [
        ("Hiện đại hóa hình ảnh", "Nâng tầm chuyển đổi số phong trào sinh viên ngang tầm quốc tế."),
        ("Tối ưu không gian", "Sử dụng hiệu quả từng hội trường, phòng lab máy tính."),
        ("Dữ liệu minh bạch", "Loại bỏ hoàn toàn vấn nạn điểm danh hộ, thông tin ảo."),
        ("Sẵn sàng mở rộng", "Dễ dàng tích hợp với các hệ thống quản lý học vụ hiện có.")
    ], top_accent=GREEN, bg_color=GREEN_TINT, border_color=GREEN_BORDER, icon="🏛️")

    # =========================================================================
    # SLIDE 7: 5 PERSONA CARDS (Phân công nhiệm vụ)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "2. Phân công nhiệm vụ", "Chân Dung & Trách Nhiệm 5 Thành Viên Nhóm", "Thành viên 2: Nguyễn Việt Anh", "👥")

    members = [
        ("Trương Công Dũng", "DE200433", "Trưởng Nhóm & System", PRIMARY, PRIMARY_TINT, PRIMARY_BORDER, [
            "Kiến trúc tổng thể MVC",
            "Cơ chế Atomic Booking",
            "Điều phối chung dự án"
        ]),
        ("Nguyễn Việt Anh", "SE190111", "PM & Scrum Master", BLUE, BLUE_TINT, BLUE_BORDER, [
            "Quản lý tiến độ 4 Sprint",
            "Mô hình CSDL & Relations",
            "Quy trình chuẩn Gitflow"
        ]),
        ("Lê Hoàng Long", "SE190222", "Security & Backend", GREEN, GREEN_TINT, GREEN_BORDER, [
            "4 Lá chắn bảo mật OWASP",
            "Thuật toán mã hóa QR",
            "Xử lý CSRF & Session"
        ]),
        ("Trần Minh Quang", "SE190333", "Fullstack & UI/UX", PURPLE, PURPLE_TINT, PURPLE_BORDER, [
            "Giao diện Responsive",
            "WebRTC Scanner Camera",
            "Phụ trách kịch bản Demo"
        ]),
        ("Phạm Đức Trọng", "SE190444", "QA & Test Lead", AMBER, AMBER_TINT, AMBER_BORDER, [
            "Thiết kế 15 Unit Tests",
            "Kiểm thử tải & Concurrency",
            "Tối ưu Cold Start Vercel"
        ]),
    ]

    card_w = Inches(2.2)
    spacing = Inches(0.18)
    left_start = Inches(0.8)

    for i, (m_name, m_id, m_role, m_col, m_bg, m_brd, tasks) in enumerate(members):
        c_left = left_start + i * (card_w + spacing)
        
        c = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(1.5), card_w, Inches(5.3))
        c.fill.solid()
        c.fill.fore_color.rgb = m_bg
        c.line.color.rgb = m_brd
        c.line.width = Pt(1.5)

        # Top Accent Strip
        c_strip = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(1.5), card_w, Inches(0.08))
        c_strip.fill.solid()
        c_strip.fill.fore_color.rgb = m_col
        c_strip.line.fill.background()

        # Text Frame
        tb_m = s7.shapes.add_textbox(c_left + Inches(0.1), Inches(1.65), card_w - Inches(0.2), Inches(4.9))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True

        p_av = tf_m.paragraphs[0]
        p_av.alignment = PP_ALIGN.CENTER
        r_av = p_av.add_run()
        r_av.text = "👨‍💻"
        r_av.font.size = Pt(28)

        p_nm = tf_m.add_paragraph()
        p_nm.alignment = PP_ALIGN.CENTER
        p_nm.space_before = Pt(2)
        r_nm = p_nm.add_run()
        r_nm.text = m_name
        r_nm.font.bold = True
        r_nm.font.size = Pt(11.5)
        r_nm.font.color.rgb = TEXT_HEAD

        p_id = tf_m.add_paragraph()
        p_id.alignment = PP_ALIGN.CENTER
        r_id = p_id.add_run()
        r_id.text = m_id
        r_id.font.size = Pt(9.5)
        r_id.font.color.rgb = TEXT_MUTED

        p_rl = tf_m.add_paragraph()
        p_rl.alignment = PP_ALIGN.CENTER
        p_rl.space_before = Pt(4)
        r_rl = p_rl.add_run()
        r_rl.text = m_role
        r_rl.font.bold = True
        r_rl.font.size = Pt(10)
        r_rl.font.color.rgb = m_col

        p_sp = tf_m.add_paragraph()
        p_sp.space_before = Pt(8)
        for t in tasks:
            p_t = tf_m.add_paragraph()
            p_t.space_before = Pt(3)
            r_t = p_t.add_run()
            r_t.text = f"• {t}"
            r_t.font.size = Pt(9.5)
            r_t.font.color.rgb = TEXT_SUB

        # Bottom 20% pill
        p_20 = tf_m.add_paragraph()
        p_20.alignment = PP_ALIGN.CENTER
        p_20.space_before = Pt(14)
        r_20 = p_20.add_run()
        r_20.text = "⭐ Đóng góp: 20%"
        r_20.font.bold = True
        r_20.font.size = Pt(10)
        r_20.font.color.rgb = m_col

    # =========================================================================
    # SLIDE 8: CÔNG CỤ QUẢN LÝ DỰ ÁN
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "3. Công cụ & Kế hoạch", "Bộ Công Cụ Quản Lý & Điều Phối Dự Án", "Thành viên 2: Nguyễn Việt Anh", "🛠️")

    add_bento_box(s8, Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.6), "Jira & Trello (Quản Trị Agile)", [
        ("Phân rã User Stories", "Chuyển đổi yêu cầu thành 24 Tasks cụ thể, gán Story Points."),
        ("Kanban Board 4 cột", "To Do -> In Progress -> Code Review -> Done minh bạch tiến độ."),
        ("Kiểm soát rủi ro", "Phát hiện điểm nghẽn (Bottlenecks) sớm trong các buổi Daily Standup.")
    ], top_accent=BLUE, bg_color=BLUE_TINT, border_color=BLUE_BORDER, icon="📋")

    add_bento_box(s8, Inches(6.8), Inches(1.5), Inches(5.6), Inches(2.6), "GitHub Enterprise (Quản Lý Mã Nguồn)", [
        ("Mô hình Gitflow chuẩn mực", "Tách biệt rõ ràng nhánh main, develop và các feature/branches."),
        ("Pull Request bắt buộc", "Mọi thay đổi cần ít nhất 1 thành viên review trước khi merge."),
        ("Tự động hóa CI/CD", "Tự động chạy bộ test kiểm tra trước khi đồng bộ lên máy chủ Vercel.")
    ], top_accent=PRIMARY, bg_color=PRIMARY_TINT, border_color=PRIMARY_BORDER, icon="🐙")

    add_bento_box(s8, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.6), "Figma (Thiết Kế UI/UX Responsive)", [
        ("Wireframing & Prototype", "Phác thảo trải nghiệm người dùng từ màn hình Mobile đến Desktop."),
        ("Thiết kế theo chuẩn FPT", "Tông màu nhận diện cam-xanh, bố cục thẻ trực quan, dễ thao tác."),
        ("Tối ưu hóa bàn quét QR", "Thiết kế giao diện quét camera toàn màn hình tiện lợi trên di động.")
    ], top_accent=PURPLE, bg_color=PURPLE_TINT, border_color=PURPLE_BORDER, icon="🎨")

    add_bento_box(s8, Inches(6.8), Inches(4.3), Inches(5.6), Inches(2.6), "Discord & Slack (Giao Tiếp Nhanh)", [
        ("Họp Daily Standup 15 phút", "Cập nhật tiến độ hàng ngày, tháo gỡ vướng mắc kỹ thuật ngay lập tức."),
        ("Kênh tích hợp Webhook", "Nhận thông báo tự động mỗi khi có Commit, PR hoặc Build hoàn tất."),
        ("Chia sẻ tài liệu kỹ thuật", "Lưu trữ quy ước mã nguồn, kịch bản test và tài liệu API chung.")
    ], top_accent=GREEN, bg_color=GREEN_TINT, border_color=GREEN_BORDER, icon="💬")

    # =========================================================================
    # SLIDE 9: KẾ HOẠCH 4 SPRINT AGILE
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "3. Công cụ & Kế hoạch", "Kế Hoạch Thực Thi Dự Án Qua 4 Sprint Agile", "Thành viên 2: Nguyễn Việt Anh", "📅")

    sprints = [
        ("Sprint 1 (Tuần 1 - 2)", "Khởi Tạo & Khảo Sát", PRIMARY, PRIMARY_TINT, PRIMARY_BORDER, [
            "Khảo sát thực trạng events.fptu.vn",
            "Thu thập yêu cầu CTSV & Sinh viên",
            "Thiết kế CSDL 6 bảng & Mockup Figma",
            "Khởi tạo Skeleton Flask & Gitflow"
        ]),
        ("Sprint 2 (Tuần 3 - 4)", "Tính Năng Cốt Lõi", BLUE, BLUE_TINT, BLUE_BORDER, [
            "Phân quyền RBAC (Sinh viên / CTSV)",
            "Đăng ký vé 1-click & Khóa chỗ Atomic",
            "Sinh mã QR động kèm Token mã hóa",
            "Trang tra cứu vé & Hủy vé tức thì"
        ]),
        ("Sprint 3 (Tuần 5 - 6)", "Bàn Quét QR & Quản Trị", GREEN, GREEN_TINT, GREEN_BORDER, [
            "Tích hợp WebRTC Camera Scanner",
            "Xử lý quét vé siêu tốc < 1s tại chỗ",
            "Dashboard quản trị CTSV & Duyệt bài",
            "Module xuất báo cáo danh sách Excel"
        ]),
        ("Sprint 4 (Tuần 7 - 8)", "Kiểm Thử & Đóng Gói", PURPLE, PURPLE_TINT, PURPLE_BORDER, [
            "Viết bộ 15 Unit Tests toàn diện",
            "Kiểm thử tải đồng thời chống Race-condition",
            "Deploy Vercel & Tối ưu Cold Start",
            "Hoàn thiện Slide & Kịch bản bảo vệ"
        ]),
    ]

    sp_w = Inches(2.78)
    sp_gap = Inches(0.2)
    sp_left = Inches(0.8)

    for idx, (sp_title, sp_sub, sp_col, sp_bg, sp_brd, sp_tasks) in enumerate(sprints):
        x = sp_left + idx * (sp_w + sp_gap)
        c = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.5), sp_w, Inches(5.3))
        c.fill.solid()
        c.fill.fore_color.rgb = sp_bg
        c.line.color.rgb = sp_brd
        c.line.width = Pt(1.5)

        # Top Bar
        tb_bar = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.5), sp_w, Inches(0.08))
        tb_bar.fill.solid()
        tb_bar.fill.fore_color.rgb = sp_col
        tb_bar.line.fill.background()

        tb_s = s9.shapes.add_textbox(x + Inches(0.12), Inches(1.68), sp_w - Inches(0.24), Inches(4.9))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True

        p1 = tf_s.paragraphs[0]
        r1 = p1.add_run()
        r1.text = sp_title
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = TEXT_HEAD

        p2 = tf_s.add_paragraph()
        r2 = p2.add_run()
        r2.text = sp_sub
        r2.font.bold = True
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = sp_col

        p_div = tf_s.add_paragraph()
        p_div.space_before = Pt(8)

        for tk in sp_tasks:
            ptk = tf_s.add_paragraph()
            ptk.space_before = Pt(5)
            rtk = ptk.add_run()
            rtk.text = f"✓ {tk}"
            rtk.font.size = Pt(10)
            rtk.font.color.rgb = TEXT_SUB

    # =========================================================================
    # SLIDE 10: QUY TRÌNH PHÁT TRIỂN & CHUẨN GITFLOW
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "3. Công cụ & Kế hoạch", "Quy Trình Gitflow & Cổng Kiểm Soát Chất Lượng", "Thành viên 2: Nguyễn Việt Anh", "🌿")

    add_bento_box(s10, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3), "Cấu Trúc Nhánh Gitflow Chuẩn Mực", [
        ("main (Production)", "Nhánh ổn định tuyệt đối, tự động kích hoạt deploy lên Vercel."),
        ("develop (Integration)", "Nhánh tích hợp chung, nơi hợp nhất các tính năng đã kiểm thử."),
        ("feature/* (Chức năng mới)", "Mỗi thành viên làm việc độc lập trên nhánh riêng (vd: feature/qr-scanner)."),
        ("hotfix/* (Sửa lỗi khẩn cấp)", "Vá lỗi trực tiếp trên production khi có sự cố phát sinh."),
        ("Quy tắc Commit Message", "Tuân thủ chuẩn Conventional Commits (feat:, fix:, docs:, test:).")
    ], top_accent=PRIMARY, bg_color=PRIMARY_TINT, border_color=PRIMARY_BORDER, icon="🌳")

    add_bento_box(s10, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.3), "4 Bước Quality Gate Bắt Buộc", [
        ("Bước 1: Tự kiểm tra cục bộ (Local)", "Thành viên chạy `pytest` và kiểm tra lỗi cú pháp trước khi push."),
        ("Bước 2: Tạo Pull Request chi tiết", "Mô tả rõ nội dung thay đổi, đính kèm ảnh chụp kết quả kiểm thử."),
        ("Bước 3: Peer Code Review", "Ít nhất 1 thành viên khác (Lead hoặc Architect) phản biện và duyệt code."),
        ("Bước 4: Hợp nhất & Tự động Deploy", "Merge vào develop/main, hệ thống Vercel tự động build trong 45s."),
        ("Lợi ích đạt được", "Loại bỏ hoàn toàn xung đột mã nguồn, bảo đảm hệ thống luôn trong trạng thái sẵn sàng.")
    ], top_accent=GREEN, bg_color=GREEN_TINT, border_color=GREEN_BORDER, icon="🛡️")

    # =========================================================================
    # SLIDE 11: TỔNG QUAN TECH STACK
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "4. Kiến trúc & Công nghệ", "Tổng Quan Công Nghệ Sử Dụng (Tech Stack Hiện Đại)", "Thành viên 3: Lê Hoàng Long", "💻")

    tech_cols = [
        ("Frontend", "Giao Diện & Tương Tác", PRIMARY, PRIMARY_TINT, PRIMARY_BORDER, "🎨", [
            ("HTML5 / CSS3", "Cấu trúc ngữ nghĩa, tương thích mọi kích thước màn hình."),
            ("Bootstrap 5", "Hệ thống Grid chuẩn hóa, giao diện Responsive hiện đại."),
            ("Vanilla JavaScript", "Xử lý tương tác mượt mà, không phụ thuộc thư viện nặng."),
            ("HTML5-QRCode", "Giải mã mã vạch qua camera WebRTC trực tiếp."),
            ("Bootstrap Icons", "Bộ biểu tượng trực quan, nhất quán toàn hệ thống.")
        ]),
        ("Backend", "Xử Lý Nghiệp Vụ", BLUE, BLUE_TINT, BLUE_BORDER, "⚙️", [
            ("Python 3.11", "Hiệu năng xử lý cao, cú pháp rõ ràng, bảo trì thuận lợi."),
            ("Flask Framework", "Micro-framework nhẹ, linh hoạt, tối ưu cho Serverless."),
            ("SQLAlchemy ORM", "Quản trị truy vấn hướng đối tượng, an toàn tuyệt đối."),
            ("Werkzeug Security", "Mã hóa băm mật khẩu PBKDF2/SHA256 chuẩn công nghiệp."),
            ("qrcode / io", "Tự động kết xuất ảnh mã QR động theo luồng bộ nhớ.")
        ]),
        ("Cơ Sở Dữ Liệu", "Lưu Trữ Bền Vững", GREEN, GREEN_TINT, GREEN_BORDER, "🗄️", [
            ("SQLite (Local)", "Cơ sở dữ liệu nhúng siêu nhẹ, không cần cài đặt phức tạp."),
            ("PostgreSQL (Cloud)", "Sẵn sàng mở rộng trên Supabase / Neon khi lượng truy cập lớn."),
            ("ACID Transactions", "Bảo đảm tính toàn vẹn dữ liệu khi đặt vé đồng thời."),
            ("Khóa Ngoại Foreign Keys", "Ràng buộc chặt chẽ quan hệ giữa User, Event và Ticket."),
            ("Chỉ mục Indexes", "Tối ưu hóa tốc độ tìm kiếm vé và sự kiện dưới 10ms.")
        ]),
        ("Hạ Tầng & CI/CD", "Vận Hành & Triển Khai", PURPLE, PURPLE_TINT, PURPLE_BORDER, "🚀", [
            ("Vercel Serverless", "Tự động co giãn theo tải, miễn phí bảo trì máy chủ."),
            ("WSGI App Handler", "Đóng gói ứng dụng Flask tương thích môi trường Cloud."),
            ("GitHub Actions", "Tự động kiểm thử trước khi bàn giao bản dựng mới."),
            ("Zero Downtime", "Cập nhật mã nguồn mới mà không làm gián đoạn người dùng."),
            ("SSL / HTTPS", "Mã hóa toàn bộ lưu lượng dữ liệu trên đường truyền.")
        ]),
    ]

    for idx, (t_title, t_sub, t_col, t_bg, t_brd, t_ic, t_items) in enumerate(tech_cols):
        x = Inches(0.8) + idx * (Inches(2.78) + Inches(0.2))
        add_bento_box(s11, x, Inches(1.5), Inches(2.78), Inches(5.3), t_title, t_items, top_accent=t_col, bg_color=t_bg, border_color=t_brd, icon=t_ic)

    # =========================================================================
    # SLIDE 12: KIẾN TRÚC PHẦN MỀM MVC 3 TẦNG
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "4. Kiến trúc & Công nghệ", "Kiến Trúc Phần Mềm MVC Phân Tách Trách Nhiệm", "Thành viên 3: Lê Hoàng Long", "🏗️")

    layers = [
        ("TẦNG 1: VIEW (GIAO DIỆN NGƯỜI DÙNG)", "Jinja2 Templates & Responsive Web", PRIMARY, PRIMARY_TINT, PRIMARY_BORDER, [
            ("Màn hình Sinh viên", "Trang chủ duyệt sự kiện, trang chi tiết, giỏ vé cá nhân, lịch sử."),
            ("Màn hình Cán bộ CTSV", "Dashboard thống kê, danh mục sự kiện, bàn quét camera check-in."),
            ("Tương tác Client-side", "Camera WebRTC quét mã QR, gọi API bất đồng bộ (Fetch API).")
        ]),
        ("TẦNG 2: CONTROLLER (ĐIỀU KHIỂN & NGHIỆP VỤ)", "Flask Blueprints & Route Handlers", BLUE, BLUE_TINT, BLUE_BORDER, [
            ("Xác thực & Phân quyền", "Kiểm tra phiên đăng nhập (Session Guard), chặn truy cập trái phép."),
            ("Nghiệp vụ Đặt chỗ Atomic", "Kiểm tra số ghế trống, trừ slot trong Transaction nguyên tử."),
            ("Giải mã & Đối soát QR", "Xác thực tính hợp lệ của Token, ghi nhận thời gian check-in.")
        ]),
        ("TẦNG 3: MODEL (CƠ SỞ DỮ LIỆU & ORM)", "SQLAlchemy ORM & Database Engine", GREEN, GREEN_TINT, GREEN_BORDER, [
            ("Mô hình thực thể 6 bảng", "Quan hệ 1-Nhiều chặt chẽ: User, Event, Ticket, Category, Log, Token."),
            ("Bảo đảm toàn vẹn ACID", "Rollback an toàn khi có lỗi phát sinh, bảo vệ dữ liệu."),
            ("Truy vấn tối ưu hóa", "Nạp dữ liệu thông minh (Lazy Loading), hạn chế số lần truy vấn thừa.")
        ]),
    ]

    for idx, (l_title, l_sub, l_col, l_bg, l_brd, l_items) in enumerate(layers):
        y = Inches(1.5) + idx * (Inches(1.65) + Inches(0.18))
        add_bento_box(s12, Inches(0.8), y, Inches(11.733), Inches(1.65), l_title, l_items, top_accent=l_col, bg_color=l_bg, border_color=l_brd, icon="📦")

    # =========================================================================
    # SLIDE 13: THIẾT KẾ CƠ SỞ DỮ LIỆU
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "4. Kiến trúc & Công nghệ", "Mô Hình Dữ Liệu Quan Hệ 6 Bảng Chuẩn Hóa", "Thành viên 3: Lê Hoàng Long", "🗄️")

    tables = [
        ("User (Tài Khoản)", "Khóa chính: id", PRIMARY, PRIMARY_TINT, PRIMARY_BORDER, [
            "email, mssv, full_name",
            "password_hash (Băm bảo mật)",
            "role (Student / Admin CTSV)"
        ]),
        ("Event (Sự Kiện)", "Khóa chính: id", BLUE, BLUE_TINT, BLUE_BORDER, [
            "title, location, start_time",
            "max_slots (Sức chứa tối đa)",
            "registered_count (Số vé đã cấp)",
            "status (Open, Closed, Finished)"
        ]),
        ("Ticket (Vé Điện Tử)", "Khóa chính: id", GREEN, GREEN_TINT, GREEN_BORDER, [
            "user_id (FK), event_id (FK)",
            "ticket_code (Mã QR độc bản)",
            "status (Valid, Used, Cancelled)",
            "checkin_time (Thời điểm vào cửa)"
        ]),
        ("Category (Danh Mục)", "Khóa chính: id", PURPLE, PURPLE_TINT, PURPLE_BORDER, [
            "name, description, icon",
            "Phân loại: Công nghệ, Kỹ năng,",
            "Văn hóa, Thể thao, OJT..."
        ]),
        ("Audit Log (Nhật Ký)", "Khóa chính: id", AMBER, AMBER_TINT, AMBER_BORDER, [
            "user_id, action, ip_address",
            "timestamp, details",
            "Lưu vết mọi hành vi nhạy cảm"
        ]),
        ("Security Token (Khóa Mã)", "Khóa chính: id", RED, RED_TINT, RED_BORDER, [
            "ticket_id, secret_hash",
            "expires_at, is_revoked",
            "Chống giả mạo mã QR"
        ]),
    ]

    for idx, (tb_name, tb_pk, tb_col, tb_bg, tb_brd, tb_fields) in enumerate(tables):
        row = idx // 3
        col = idx % 3
        x = Inches(0.8) + col * (Inches(3.75) + Inches(0.24))
        y = Inches(1.5) + row * (Inches(2.55) + Inches(0.2))
        add_bento_box(s13, x, y, Inches(3.75), Inches(2.55), tb_name, tb_fields, top_accent=tb_col, bg_color=tb_bg, border_color=tb_brd, icon="📋")

    # =========================================================================
    # SLIDE 14: 4 LÁ CHẮN AN TOÀN THÔNG TIN
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "4. Kiến trúc & Công nghệ", "4 Lá Chắn Bảo Mật Theo Tiêu Chuẩn OWASP", "Thành viên 3: Lê Hoàng Long", "🛡️")

    shields = [
        ("Lá Chắn 1: Chống Giả Mạo CSRF", "Token Xác Thực Trong Mọi Form", BLUE, BLUE_TINT, BLUE_BORDER, "🔒", [
            ("Sinh mã Token ngẫu nhiên", "Gắn kèm trong mỗi yêu cầu gửi dữ liệu POST."),
            ("Từ chối yêu cầu từ bên thứ ba", "Ngăn chặn kẻ xấu lừa sinh viên gửi lệnh đặt vé trái ý muốn."),
            ("Bảo vệ toàn bộ API nội bộ", "Chỉ chấp nhận các yêu cầu xuất phát từ chính tên miền hệ thống.")
        ]),
        ("Lá Chắn 2: Băm Mật Khẩu Werkzeug", "Chuẩn Mã Hóa PBKDF2/SHA-256", PRIMARY, PRIMARY_TINT, PRIMARY_BORDER, "🔑", [
            ("Tuyệt đối không lưu mật khẩu thô", "Toàn bộ mật khẩu được băm qua hàng ngàn vòng mã hóa."),
            ("Muối ngẫu nhiên (Salt)", "Mỗi tài khoản có chuỗi muối riêng, vô hiệu hóa hoàn toàn bảng Rainbow."),
            ("An toàn kể cả khi lộ CSDL", "Kẻ tấn công không thể dịch ngược để tìm lại mật khẩu gốc.")
        ]),
        ("Lá Chắn 3: Phân Quyền Vai Trò RBAC", "Kiểm Soát Quyền Hạn Chặt Chẽ", GREEN, GREEN_TINT, GREEN_BORDER, "👤", [
            ("Tách biệt Sinh viên & Cán bộ", "Sinh viên tuyệt đối không thể xem hay gọi các URL quản trị."),
            ("Decorator kiểm tra phiên", "Mỗi thao tác nhạy cảm đều được bọc lớp kiểm tra `@admin_required`."),
            ("Phòng chống leo thang đặc quyền", "Không cho phép sửa đổi quyền hạn thông qua việc sửa tham số URL.")
        ]),
        ("Lá Chắn 4: Khóa Dữ Liệu Đồng Thời", "Giao Dịch Nguyên Tử Chống Đua", PURPLE, PURPLE_TINT, PURPLE_BORDER, "⚡", [
            ("Khóa cứng bản ghi sự kiện", "Chỉ một yêu cầu được phép cập nhật số lượng vé tại một thời điểm."),
            ("Không bao giờ vượt quá sức chứa", "Ngăn ngừa tình trạng 2 sinh viên cùng đặt được chiếc vé cuối cùng."),
            ("Tự động Rollback khi lỗi", "Nếu xảy ra lỗi mạng giữa chừng, toàn bộ giao dịch được khôi phục nguyên trạng.")
        ]),
    ]

    for idx, (sh_title, sh_sub, sh_col, sh_bg, sh_brd, sh_ic, sh_items) in enumerate(shields):
        row = idx // 2
        col = idx % 2
        x = Inches(0.8) + col * (Inches(5.6) + Inches(0.533))
        y = Inches(1.5) + row * (Inches(2.55) + Inches(0.2))
        add_bento_box(s14, x, y, Inches(5.6), Inches(2.55), sh_title, sh_items, top_accent=sh_col, bg_color=sh_bg, border_color=sh_brd, icon=sh_ic)

    # =========================================================================
    # SLIDE 15: CƠ CHẾ KHÓA VÉ CHỐNG OVERBOOKING
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "4. Kiến trúc & Công nghệ", "Cơ Chế Khóa Vé Nguyên Tử & Chống Đua Dữ Liệu", "Thành viên 3: Lê Hoàng Long", "⚡")

    add_kpi_card(s15, Inches(0.8), Inches(1.5), Inches(3.6), Inches(1.4), "1 Ghế Còn Lại", "Tình Huống Căng Thẳng", "Nhiều sinh viên cùng bấm giữ chỗ cùng giây", RED, RED_TINT, RED_BORDER)
    add_kpi_card(s15, Inches(4.8), Inches(1.5), Inches(3.6), Inches(1.4), "0.01 Giây", "Xử Lý Giao Dịch", "Khóa hàng trong CSDL trước khi cấp vé", PRIMARY, PRIMARY_TINT, PRIMARY_BORDER)
    add_kpi_card(s15, Inches(8.8), Inches(1.5), Inches(3.6), Inches(1.4), "0 Lỗi Trùng Vé", "Độ Chính Xác 100%", "Vé chỉ cấp cho duy nhất người đến trước", GREEN, GREEN_TINT, GREEN_BORDER)

    add_bento_box(s15, Inches(0.8), Inches(3.1), Inches(5.6), Inches(3.7), "Quy Trình Xử Lý Giao Dịch Nguyên Tử", [
        ("Bước 1: Bắt đầu giao dịch (BEGIN)", "Hệ thống mở một phiên làm việc độc lập với cơ sở dữ liệu."),
        ("Bước 2: Khóa dòng dữ liệu sự kiện", "Sử dụng câu lệnh SELECT FOR UPDATE để tạm khóa sự kiện."),
        ("Bước 3: Kiểm tra điều kiện ngặt nghèo", "Nếu số vé đã phát hành < sức chứa tối đa thì mới tiếp tục."),
        ("Bước 4: Tăng bộ đếm & Tạo vé", "Cộng 1 vào số lượng, lưu thông tin vé của sinh viên trúng slot."),
        ("Bước 5: Xác nhận giao dịch (COMMIT)", "Ghi dữ liệu vĩnh viễn và nhả khóa cho các yêu cầu tiếp theo.")
    ], top_accent=PRIMARY, bg_color=CARD_WHITE, icon="🔄")

    add_bento_box(s15, Inches(6.8), Inches(3.1), Inches(5.6), Inches(3.7), "Kịch Bản Khi Có 50 Người Đua Chiếc Vé Cuối", [
        ("Yêu cầu đến sớm nhất (1st Request)", "Vượt qua kiểm tra -> Khóa vé thành công -> Nhận vé mã QR hợp lệ."),
        ("49 yêu cầu còn lại (Other Requests)", "Xếp hàng sau -> Hệ thống thấy vé đã đầy -> Báo lỗi 'Sự kiện đã hết chỗ'."),
        ("Không bao giờ xảy ra Race Condition", "Loại bỏ hoàn toàn rủi ro vỡ trận sức chứa hội trường."),
        ("Trải nghiệm công bằng cho sinh viên", "Thời gian phản hồi minh bạch, không thiên vị hay ưu tiên ngầm.")
    ], top_accent=GREEN, bg_color=CARD_WHITE, icon="🎯")

    # =========================================================================
    # SLIDE 16: PHÂN HỆ SINH VIÊN
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "5. Tính năng chính", "Phân Hệ Tính Năng Dành Cho Sinh Viên FPTU", "Thành viên 4: Trần Minh Quang", "🎓")

    add_bento_box(s16, Inches(0.8), Inches(1.5), Inches(6.8), Inches(5.3), "4 Tính Năng Trọng Tâm Dành Cho Sinh Viên", [
        ("1. Xem & Lọc sự kiện trực quan", "Khám phá danh sách hội thảo, workshop, hackathon theo danh mục hấp dẫn."),
        ("2. Đăng ký giữ chỗ 1-Click", "Chỉ cần đăng nhập bằng Email trường, bấm đăng ký là nhận ngay vé xác nhận."),
        ("3. Sở hữu vé điện tử QR cá nhân", "Mỗi vé có mã QR riêng biệt chứa mã Token, dùng để điểm danh tại cửa."),
        ("4. Hủy vé linh hoạt hoàn slot", "Bận đột xuất có thể hủy vé với 1 thao tác, tự động nhường ghế cho bạn khác."),
        ("5. Xem lại lịch sử tham gia", "Toàn bộ sự kiện đã tham dự và đã điểm danh đều được lưu trữ đầy đủ.")
    ], top_accent=PRIMARY, bg_color=PRIMARY_TINT, border_color=PRIMARY_BORDER, icon="🌟")

    if os.path.exists(IMG_AI):
        s16.shapes.add_picture(IMG_AI, Inches(7.9), Inches(1.5), Inches(4.6), Inches(5.3))
        tag_sv = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.1), Inches(6.15), Inches(4.2), Inches(0.45))
        tag_sv.fill.solid()
        tag_sv.fill.fore_color.rgb = CARD_WHITE
        tag_sv.line.color.rgb = PRIMARY_BORDER
        tf_sv = tag_sv.text_frame
        psv = tf_sv.paragraphs[0]
        psv.alignment = PP_ALIGN.CENTER
        rsv = psv.add_run()
        rsv.text = "Giao Diện Đăng Ký Vé Sự Kiện Trực Quan"
        rsv.font.bold = True
        rsv.font.size = Pt(10)
        rsv.font.color.rgb = PRIMARY_DARK

    # =========================================================================
    # SLIDE 17: PHÂN HỆ CÁN BỘ CTSV
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "5. Tính năng chính", "Phân Hệ Quản Trị Dành Cho Cán Bộ CTSV & BTC", "Thành viên 4: Trần Minh Quang", "🛡️")

    add_bento_box(s17, Inches(0.8), Inches(1.5), Inches(6.8), Inches(5.3), "4 Tính Năng Trọng Tâm Dành Cho Cán Bộ CTSV", [
        ("1. Dashboard tổng quan toàn trường", "Theo dõi tổng số sự kiện, tổng số vé phát hành và số lượng sinh viên tham gia."),
        ("2. Khởi tạo & Điều phối sự kiện", "Đặt tên sự kiện, giới hạn sức chứa hội trường, thời gian và địa điểm tổ chức."),
        ("3. Bàn quét QR điểm danh WebRTC", "Sử dụng camera máy tính hoặc điện thoại quét vé sinh viên trong 0.1 giây."),
        ("4. Xuất danh sách tham gia ra Excel", "Tải file dữ liệu chi tiết danh sách sinh viên đã điểm danh chỉ bằng 1 nút bấm."),
        ("5. Quản lý trạng thái hoạt động", "Đóng/mở đăng ký linh hoạt, khóa sổ sự kiện khi đã hoàn thành.")
    ], top_accent=BLUE, bg_color=BLUE_TINT, border_color=BLUE_BORDER, icon="📊")

    if os.path.exists(IMG_HACK):
        s17.shapes.add_picture(IMG_HACK, Inches(7.9), Inches(1.5), Inches(4.6), Inches(5.3))
        tag_ct = s17.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.1), Inches(6.15), Inches(4.2), Inches(0.45))
        tag_ct.fill.solid()
        tag_ct.fill.fore_color.rgb = CARD_WHITE
        tag_ct.line.color.rgb = BLUE_BORDER
        tf_ct = tag_ct.text_frame
        pct = tf_ct.paragraphs[0]
        pct.alignment = PP_ALIGN.CENTER
        rct = pct.add_run()
        rct.text = "Trung Tâm Điều Hành & Duyệt Sự Kiện CTSV"
        rct.font.bold = True
        rct.font.size = Pt(10)
        rct.font.color.rgb = BLUE_DARK

    # =========================================================================
    # SLIDE 18: CÔNG NGHỆ QUÉT QR WEBRTC
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "5. Tính năng chính", "Công Nghệ Bàn Quét Mã QR & Camera WebRTC", "Thành viên 4: Trần Minh Quang", "📷")

    add_kpi_card(s18, Inches(0.8), Inches(1.5), Inches(3.6), Inches(1.4), "0.1 Giây", "Tốc Độ Quét Mã", "Nhận diện tức thì qua camera WebRTC", GREEN, GREEN_TINT, GREEN_BORDER)
    add_kpi_card(s18, Inches(4.8), Inches(1.5), Inches(3.6), Inches(1.4), "0 Ứng Dụng", "Không Cần Cài Đặt", "Chạy trực tiếp trên trình duyệt Web", BLUE, BLUE_TINT, BLUE_BORDER)
    add_kpi_card(s18, Inches(8.8), Inches(1.5), Inches(3.6), Inches(1.4), "1 Lần Dùng", "Chống Gian Lận", "Vé đã check-in lập tức đổi trạng thái", RED, RED_TINT, RED_BORDER)

    add_bento_box(s18, Inches(0.8), Inches(3.1), Inches(5.6), Inches(3.7), "Quy Trình Xử Lý Kỹ Thuật Của Bàn Quét", [
        ("Khởi tạo luồng Camera", "Sử dụng API Navigator MediaDevices bắt luồng video trực tiếp."),
        ("Quét khung hình liên tục", "Thư viện HTML5-QRCode phân tích 30 khung hình/giây để bắt mã."),
        ("Gửi Token xác thực", "Gửi mã vé bất đồng bộ (AJAX) về máy chủ để kiểm tra tính hợp lệ."),
        ("Phản hồi âm thanh & Màu sắc", "Màn hình chuyển xanh lá kèm tiếng 'Bíp' báo hiệu check-in thành công.")
    ], top_accent=GREEN, bg_color=CARD_WHITE, icon="⚙️")

    add_bento_box(s18, Inches(6.8), Inches(3.1), Inches(5.6), Inches(3.7), "3 Tình Huống Xử Lý Thực Tế Tại Cửa", [
        ("Trường hợp 1: Vé hợp lệ", "Hiển thị Họ tên + MSSV sinh viên, cập nhật trạng thái 'ĐÃ CHECK-IN'."),
        ("Trường hợp 2: Vé đã sử dụng trước đó", "Báo động đỏ: 'Vé này đã được điểm danh vào lúc 16:30!', chặn gian lận."),
        ("Trường hợp 3: Vé không tồn tại / Giả mạo", "Cảnh báo vàng: 'Mã vé không hợp lệ trên hệ thống FPTU'."),
        ("Chế độ quét liên tục", "Tự động làm mới khung hình sẵn sàng cho sinh viên tiếp theo sau 0.5s.")
    ], top_accent=PRIMARY, bg_color=CARD_WHITE, icon="🛡️")

    # =========================================================================
    # SLIDE 19: KỊCH BẢN LIVE DEMO - PHẦN 1 (SINH VIÊN)
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    add_header(s19, "5. Tính năng chính", "Kịch Bản Live Demo: Hành Trình Của Sinh Viên", "Thành viên 4: Trần Minh Quang", "🎬")

    # Browser Bar Mockup
    br_bar = s19.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.45), Inches(11.733), Inches(0.45))
    br_bar.fill.solid()
    br_bar.fill.fore_color.rgb = RGBColor(241, 245, 249)
    br_bar.line.color.rgb = CARD_BORDER
    tf_br = br_bar.text_frame
    p_br = tf_br.paragraphs[0]
    r_br = p_br.add_run()
    r_br.text = "🔴 🟡 🟢  https://fptu-event-hub.vercel.app/events"
    r_br.font.size = Pt(10)
    r_br.font.color.rgb = TEXT_MUTED

    demo_steps_sv = [
        ("Bước 1: Đăng Nhập 1-Click", PRIMARY, PRIMARY_TINT, PRIMARY_BORDER, [
            "Bấm vào tài khoản mẫu: Trương Công Dũng (DE200433)",
            "Hệ thống tự động thiết lập phiên làm việc an toàn",
            "Chuyển hướng ngay đến bảng tin sự kiện"
        ]),
        ("Bước 2: Chọn & Đăng Ký Vé", BLUE, BLUE_TINT, BLUE_BORDER, [
            "Xem chi tiết Workshop AI & Agentic Coding",
            "Quan sát thanh tiến độ số vé còn lại theo thời gian thực",
            "Bấm nút 'ĐĂNG KÝ GIỮ CHỖ NGAY'"
        ]),
        ("Bước 3: Nhận & Quản Lý Vé", GREEN, GREEN_TINT, GREEN_BORDER, [
            "Màn hình hiển thị vé điện tử cùng mã QR độc bản",
            "Vé được lưu vào mục 'Vé Của Tôi'",
            "Thử nghiệm tính năng 'Hủy vé' để chứng minh hoàn lại slot"
        ]),
    ]

    for idx, (st_title, st_col, st_bg, st_brd, st_items) in enumerate(demo_steps_sv):
        x = Inches(0.8) + idx * (Inches(3.75) + Inches(0.24))
        add_bento_box(s19, x, Inches(2.1), Inches(3.75), Inches(4.7), st_title, st_items, top_accent=st_col, bg_color=st_bg, border_color=st_brd, icon="📱")

    # =========================================================================
    # SLIDE 20: KỊCH BẢN LIVE DEMO - PHẦN 2 (CÁN BỘ CTSV)
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    add_header(s20, "5. Tính năng chính", "Kịch Bản Live Demo: Hành Trình Cán Bộ CTSV", "Thành viên 4: Trần Minh Quang", "🎬")

    # Browser Bar Mockup
    br_bar2 = s20.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.45), Inches(11.733), Inches(0.45))
    br_bar2.fill.solid()
    br_bar2.fill.fore_color.rgb = RGBColor(241, 245, 249)
    br_bar2.line.color.rgb = CARD_BORDER
    tf_br2 = br_bar2.text_frame
    p_br2 = tf_br2.paragraphs[0]
    r_br2 = p_br2.add_run()
    r_br2.text = "🔴 🟡 🟢  https://fptu-event-hub.vercel.app/admin/dashboard"
    r_br2.font.size = Pt(10)
    r_br2.font.color.rgb = TEXT_MUTED

    demo_steps_ct = [
        ("Bước 1: Truy Cập Trung Tâm CTSV", BLUE, BLUE_TINT, BLUE_BORDER, [
            "Đăng nhập bằng tài khoản: Phòng Công Tác Sinh Viên",
            "Giao diện quản trị riêng biệt, không có nút đăng ký vé",
            "Xem 4 chỉ số lớn: Tổng sự kiện, Vé phát hành, Đã check-in"
        ]),
        ("Bước 2: Mở Bàn Quét Mã QR Camera", GREEN, GREEN_TINT, GREEN_BORDER, [
            "Bấm 'Bàn Check-in', camera kích hoạt tức thì",
            "Đưa mã QR trên điện thoại sinh viên vào trước ống kính",
            "Hệ thống nhận diện < 0.1s: 'Check-in thành công: Trương Công Dũng'"
        ]),
        ("Bước 3: Xuất Dữ Liệu Báo Cáo", PURPLE, PURPLE_TINT, PURPLE_BORDER, [
            "Xem danh sách người tham gia cập nhật thời gian check-in",
            "Bấm 'Xuất Danh Sách Excel'",
            "Mở file Excel tải về chứng minh dữ liệu chuẩn xác 100%"
        ]),
    ]

    for idx, (st_title, st_col, st_bg, st_brd, st_items) in enumerate(demo_steps_ct):
        x = Inches(0.8) + idx * (Inches(3.75) + Inches(0.24))
        add_bento_box(s20, x, Inches(2.1), Inches(3.75), Inches(4.7), st_title, st_items, top_accent=st_col, bg_color=st_bg, border_color=st_brd, icon="💻")

    # =========================================================================
    # SLIDE 21: KẾT QUẢ VẬN HÀNH THỰC TẾ
    # =========================================================================
    s21 = prs.slides.add_slide(blank_layout)
    add_header(s21, "5. Tính năng chính", "Kết Quả Vận Hành & Giá Trị Thực Tế Đạt Được", "Thành viên 4: Trần Minh Quang", "🏆")

    add_kpi_card(s21, Inches(0.8), Inches(1.5), Inches(3.6), Inches(1.4), "0 Phút Chờ", "Xếp Hàng Check-in", "Sinh viên đi qua cửa chỉ với 1 thao tác quét", GREEN, GREEN_TINT, GREEN_BORDER)
    add_kpi_card(s21, Inches(4.8), Inches(1.5), Inches(3.6), Inches(1.4), "100% Khớp", "Sức Chứa Hội Trường", "Không xảy ra tình trạng thiếu chỗ hay dư thừa", PRIMARY, PRIMARY_TINT, PRIMARY_BORDER)
    add_kpi_card(s21, Inches(8.8), Inches(1.5), Inches(3.6), Inches(1.4), "1-Click", "Xuất Báo Cáo CTSV", "Thay thế hoàn toàn việc tổng hợp Excel thủ công", BLUE, BLUE_TINT, BLUE_BORDER)

    add_bento_box(s21, Inches(0.8), Inches(3.1), Inches(6.8), Inches(3.7), "Chuyển Đổi Về Chất Trong Công Tác Quản Trị", [
        ("Nâng cao tính tự giác của sinh viên", "Nhận thức rõ trách nhiệm giữ chỗ và chủ động hủy vé khi bận."),
        ("Xây dựng văn hóa sự kiện chuyên nghiệp", "Hạn chế tối đa việc đi muộn, ồn ào chen lấn tại cửa vào."),
        ("Dữ liệu minh bạch phục vụ đánh giá", "Nhà trường nắm rõ mức độ quan tâm của sinh viên với từng chủ đề."),
        ("Sẵn sàng cho các sự kiện quy mô lớn", "Hệ thống đáp ứng trơn tru các ngày hội tuyển dụng, chung kết hội thi.")
    ], top_accent=PRIMARY, bg_color=CARD_WHITE, icon="📈")

    if os.path.exists(IMG_CAREER):
        s21.shapes.add_picture(IMG_CAREER, Inches(7.9), Inches(3.1), Inches(4.6), Inches(3.7))
        tag_cr = s21.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.1), Inches(6.25), Inches(4.2), Inches(0.45))
        tag_cr.fill.solid()
        tag_cr.fill.fore_color.rgb = CARD_WHITE
        tag_cr.line.color.rgb = PRIMARY_BORDER
        tf_tcr = tag_cr.text_frame
        ptcr = tf_tcr.paragraphs[0]
        ptcr.alignment = PP_ALIGN.CENTER
        rtcr = ptcr.add_run()
        rtcr.text = "Ngày Hội Việc Làm & Kết Nối Doanh Nghiệp FPTU"
        rtcr.font.bold = True
        rtcr.font.size = Pt(10)
        rtcr.font.color.rgb = PRIMARY_DARK

    # =========================================================================
    # SLIDE 22: CHIẾN LƯỢC KIỂM THỬ
    # =========================================================================
    s22 = prs.slides.add_slide(blank_layout)
    add_header(s22, "6. Phần kiểm thử", "Chiến Lược Kiểm Thử Phần Mềm Toàn Diện", "Thành viên 5: Phạm Đức Trọng", "🧪")

    t_levels = [
        ("TẦNG 1: UNIT TESTING (KIỂM THỬ ĐƠN VỊ)", "Kiểm tra từng hàm và phương thức độc lập", PRIMARY, PRIMARY_TINT, PRIMARY_BORDER, [
            ("Mã hóa mật khẩu", "Kiểm tra hàm băm `generate_password_hash` và đối soát `check_password_hash`."),
            ("Sinh chuỗi mã vé", "Bảo đảm tính duy nhất tuyệt đối của chuỗi Token ngẫu nhiên."),
            ("Ràng buộc logic", "Kiểm tra điều kiện số vé đăng ký không được vượt quá số chỗ trống.")
        ]),
        ("TẦNG 2: INTEGRATION TESTING (KIỂM THỬ TÍCH HỢP)", "Kiểm tra tương tác giữa các thành phần", BLUE, BLUE_TINT, BLUE_BORDER, [
            ("Luồng Đăng ký -> Tạo vé -> Cập nhật CSDL", "Bảo đảm dữ liệu được đồng bộ chính xác qua ORM."),
            ("Luồng Quét QR -> Kiểm tra vé -> Ghi nhận Check-in", "Xác thực đúng mã vé và ghi nhận thời gian thực."),
            ("Kiểm tra phân quyền Route", "Đảm bảo sinh viên không gọi được API của cán bộ CTSV.")
        ]),
        ("TẦNG 3: END-TO-END & PERFORMANCE (KIỂM THỬ TẢI)", "Mô phỏng hành vi người dùng thực tế", GREEN, GREEN_TINT, GREEN_BORDER, [
            ("Kiểm thử tải đồng thời", "Giả lập 50 sinh viên cùng nhấn giữ chỗ tại cùng một thời điểm."),
            ("Kiểm tra độ trễ mạng", "Đo thời gian phản hồi API khi chạy trên máy chủ đám mây Vercel."),
            ("Kiểm thử tương thích thiết bị", "Thử nghiệm camera WebRTC trên iPhone, Android và Laptop.")
        ]),
    ]

    for idx, (tl_title, tl_sub, tl_col, tl_bg, tl_brd, tl_items) in enumerate(t_levels):
        y = Inches(1.5) + idx * (Inches(1.65) + Inches(0.18))
        add_bento_box(s22, Inches(0.8), y, Inches(11.733), Inches(1.65), tl_title, tl_items, top_accent=tl_col, bg_color=tl_bg, border_color=tl_brd, icon="🎯")

    # =========================================================================
    # SLIDE 23: KẾT QUẢ KIỂM THỬ TỰ ĐỘNG
    # =========================================================================
    s23 = prs.slides.add_slide(blank_layout)
    add_header(s23, "6. Phần kiểm thử", "Báo Cáo Kết Quả Kiểm Thử Tự Động (100% Passed)", "Thành viên 5: Phạm Đức Trọng", "✅")

    # Giant Emerald Scorecard Card
    add_kpi_card(s23, Inches(0.8), Inches(1.5), Inches(3.6), Inches(1.4), "15 / 15", "Tests Passed Tuyệt Đối", "100% kịch bản kiểm thử đều thành công", GREEN, GREEN_TINT, GREEN_BORDER)
    add_kpi_card(s23, Inches(4.8), Inches(1.5), Inches(3.6), Inches(1.4), "0 Lỗi", "Zero Failures / Errors", "Không phát hiện lỗi hồi quy logic", BLUE, BLUE_TINT, BLUE_BORDER)
    add_kpi_card(s23, Inches(8.8), Inches(1.5), Inches(3.6), Inches(1.4), "7.28 Giây", "Thời Gian Chạy Toàn Bộ", "Tự động hóa hoàn toàn với pytest", PRIMARY, PRIMARY_TINT, PRIMARY_BORDER)

    add_bento_box(s23, Inches(0.8), Inches(3.1), Inches(5.6), Inches(3.7), "Danh Mục 15 Ca Kiểm Thử Đã Thực Hiện", [
        ("Xác thực người dùng (3 tests)", "Đăng nhập thành công, sai mật khẩu, tài khoản không tồn tại."),
        ("Quản lý sự kiện (3 tests)", "Tạo sự kiện mới, chỉnh sửa sức chứa, đóng sự kiện."),
        ("Quy trình đăng ký vé (4 tests)", "Đăng ký thành công, đăng ký trùng lặp, sự kiện đã hết chỗ, hủy vé."),
        ("Hệ thống điểm danh QR (3 tests)", "Check-in vé hợp lệ, quét vé lần 2, quét vé giả mạo."),
        ("Phân quyền & An ninh (2 tests)", "Chặn sinh viên vào trang CTSV, kiểm tra mã CSRF Token.")
    ], top_accent=GREEN, bg_color=CARD_WHITE, icon="📋")

    add_bento_box(s23, Inches(6.8), Inches(3.1), Inches(5.6), Inches(3.7), "Đánh Giá Chất Lượng Phần Mềm", [
        ("Độ bao phủ mã nguồn (Code Coverage)", "Đạt trên 90% các nhánh xử lý logic quan trọng của hệ thống."),
        ("Tính ổn định cao", "Không có hiện tượng sập máy chủ khi nhận dữ liệu đầu vào bất thường."),
        ("Dễ dàng bảo trì trong tương lai", "Bộ test đóng vai trò như tài liệu kỹ thuật sống cho các lập trình viên sau."),
        ("Tự tin triển khai thực tế", "Hệ thống đáp ứng đầy đủ các tiêu chuẩn khắt khe để đưa vào sử dụng.")
    ], top_accent=BLUE, bg_color=CARD_WHITE, icon="🏆")

    # =========================================================================
    # SLIDE 24: HIỆU NĂNG & KHẢ NĂNG CHỊU TẢI
    # =========================================================================
    s24 = prs.slides.add_slide(blank_layout)
    add_header(s24, "6. Phần kiểm thử", "Báo Cáo Hiệu Năng & Khả Năng Chịu Tải Thực Tế", "Thành viên 5: Phạm Đức Trọng", "⚡")

    add_kpi_card(s24, Inches(0.8), Inches(1.5), Inches(3.6), Inches(1.4), "< 1 Giây", "Tốc Độ Phản Hồi Trang", "Tối ưu hóa tài nguyên CSS/JS và hình ảnh", BLUE, BLUE_TINT, BLUE_BORDER)
    add_kpi_card(s24, Inches(4.8), Inches(1.5), Inches(3.6), Inches(1.4), "0.1 Giây", "Giải Mã Mã Vạch Camera", "Thuật toán xử lý hình ảnh trực tiếp trên máy khách", GREEN, GREEN_TINT, GREEN_BORDER)
    add_kpi_card(s24, Inches(8.8), Inches(1.5), Inches(3.6), Inches(1.4), "100%", "Toàn Vẹn Dữ Liệu Tải Cao", "Không bị thất thoát vé khi có nhiều người truy cập", PRIMARY, PRIMARY_TINT, PRIMARY_BORDER)

    add_bento_box(s24, Inches(0.8), Inches(3.1), Inches(5.6), Inches(3.7), "Các Kỹ Thuật Tối Ưu Hóa Đã Áp Dụng", [
        ("Nén ảnh và tài nguyên tĩnh", "Toàn bộ ảnh sự kiện được tối ưu dung lượng dưới 200KB."),
        ("Chỉ mục Database Indexing", "Tạo index trên các cột `ticket_code`, `email`, `mssv` để tìm kiếm tức thì."),
        ("Cơ chế Serverless Auto-scale", "Vercel tự động mở thêm vùng chứa xử lý khi lượng truy cập tăng vọt."),
        ("Tải bất đồng bộ tài nguyên", "Camera và bảng quét QR chỉ nạp khi người dùng mở trang check-in.")
    ], top_accent=BLUE, bg_color=CARD_WHITE, icon="🚀")

    add_bento_box(s24, Inches(6.8), Inches(3.1), Inches(5.6), Inches(3.7), "Kết Quả Đo Đạc Thực Tế Trên Môi Trường Vercel", [
        ("Thời gian khởi động lạnh (Cold Start)", "Chỉ mất 1.2 giây cho yêu cầu đầu tiên, các yêu cầu sau < 200ms."),
        ("Dung lượng tải trang ban đầu", "Chưa tới 1.5MB bao gồm toàn bộ mã nguồn giao diện."),
        ("Độ trễ truyền nhận API Check-in", "Trung bình 80ms - 150ms trên kết nối 4G/Wifi thông thường."),
        ("Khả năng mở rộng dự kiến", "Sẵn sàng phục vụ đồng thời hơn 1,000 sinh viên truy cập cùng lúc.")
    ], top_accent=GREEN, bg_color=CARD_WHITE, icon="📊")

    # =========================================================================
    # SLIDE 25: LỘ TRÌNH PHÁT TRIỂN TƯƠNG LAI
    # =========================================================================
    s25 = prs.slides.add_slide(blank_layout)
    add_header(s25, "6. Phần kiểm thử", "Lộ Trình Nâng Cấp & Định Hướng Tương Lai", "Thành viên 5: Phạm Đức Trọng", "🔮")

    future_pillars = [
        ("Giai Đoạn 1: Tích Hợp AI Gợi Ý", "Đề xuất sự kiện thông minh", PRIMARY, PRIMARY_TINT, PRIMARY_BORDER, "🤖", [
            ("Phân tích sở thích sinh viên", "Dựa trên lịch sử các sự kiện đã tham dự trước đó."),
            ("Gợi ý sự kiện phù hợp", "Sinh viên ngành AI nhận thông báo về workshop công nghệ."),
            ("Tự động tóm tắt nội dung", "Ứng dụng mô hình ngôn ngữ lớn để tóm tắt điểm nổi bật của sự kiện.")
        ]),
        ("Giai Đoạn 2: Tự Động Hóa Thông Báo", "Đa kênh liên lạc thời gian thực", BLUE, BLUE_TINT, BLUE_BORDER, "📲", [
            ("Tích hợp Telegram / Zalo Bot", "Gửi vé QR trực tiếp về tin nhắn điện thoại."),
            ("Nhắc lịch tự động", "Gửi thông báo nhắc nhở 2 tiếng trước khi sự kiện bắt đầu."),
            ("Khảo sát ý kiến tức thì", "Gửi link đánh giá ngay sau khi sinh viên vừa check-in ra về.")
        ]),
        ("Giai Đoạn 3: Nhận Diện Khuôn Mặt (FaceID)", "Nâng cấp bàn check-in thông minh", GREEN, GREEN_TINT, GREEN_BORDER, "👁️", [
            ("Điểm danh không chạm", "Sinh viên chỉ cần bước qua cửa, camera tự nhận diện khuôn mặt."),
            ("Rút ngắn thời gian xuống 0.05s", "Tốc độ xử lý nhanh gấp đôi so với quét mã QR."),
            ("Bảo mật sinh trắc học", "Tuyệt đối không thể xảy ra hiện tượng cho mượn mã QR đi hộ.")
        ]),
        ("Giai Đoạn 4: Ứng Dụng Di Động Native", "Trải nghiệm trên iOS & Android", PURPLE, PURPLE_TINT, PURPLE_BORDER, "📱", [
            ("Xây dựng bằng Flutter", "Một bộ mã nguồn chạy mượt mà trên cả App Store và Google Play."),
            ("Lưu vé vào Apple Wallet / Google Wallet", "Mở vé nhanh chóng ngay trên màn hình khóa điện thoại."),
            ("Hỗ trợ quét vé ngoại tuyến", "Bàn check-in vẫn hoạt động bình thường kể cả khi mất kết nối Internet.")
        ]),
    ]

    for idx, (f_title, f_sub, f_col, f_bg, f_brd, f_ic, f_items) in enumerate(future_pillars):
        row = idx // 2
        col = idx % 2
        x = Inches(0.8) + col * (Inches(5.6) + Inches(0.533))
        y = Inches(1.5) + row * (Inches(2.55) + Inches(0.2))
        add_bento_box(s25, x, y, Inches(5.6), Inches(2.55), f_title, f_items, top_accent=f_col, bg_color=f_bg, border_color=f_brd, icon=f_ic)

    # =========================================================================
    # SLIDE 26: LỜI CẢM ƠN & BẮT ĐẦU VẤN ĐÁP Q&A
    # =========================================================================
    s26 = prs.slides.add_slide(blank_layout)
    set_bright_bg(s26)

    # Big Central Thank You Card
    ty_card = s26.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.0), Inches(10.333), Inches(5.5))
    ty_card.fill.solid()
    ty_card.fill.fore_color.rgb = CARD_WHITE
    ty_card.line.color.rgb = PRIMARY_BORDER
    ty_card.line.width = Pt(2)

    # Top Accent Ribbon
    ty_strip = s26.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.0), Inches(10.333), Inches(0.1))
    ty_strip.fill.solid()
    ty_strip.fill.fore_color.rgb = PRIMARY
    ty_strip.line.fill.background()

    tb_ty = s26.shapes.add_textbox(Inches(1.8), Inches(1.3), Inches(9.733), Inches(5.0))
    tf_ty = tb_ty.text_frame
    tf_ty.word_wrap = True

    p0 = tf_ty.paragraphs[0]
    p0.alignment = PP_ALIGN.CENTER
    r0 = p0.add_run()
    r0.text = "TRƯỜNG ĐẠI HỌC FPT — BẢO VỆ ĐỒ ÁN CHUYÊN NGÀNH CNTT"
    r0.font.bold = True
    r0.font.size = Pt(11)
    r0.font.color.rgb = BLUE_DARK

    p1 = tf_ty.add_paragraph()
    p1.alignment = PP_ALIGN.CENTER
    p1.space_before = Pt(4)
    r1 = p1.add_run()
    r1.text = "XIN CHÂN THÀNH CẢM ƠN HỘI ĐỒNG!"
    r1.font.bold = True
    r1.font.size = Pt(28)
    r1.font.color.rgb = PRIMARY

    p2 = tf_ty.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(2)
    r2 = p2.add_run()
    r2.text = "Hệ Thống FPTU EventHub Sẵn Sàng Cho Phần Vấn Đáp (Q&A)"
    r2.font.bold = True
    r2.font.size = Pt(14)
    r2.font.color.rgb = TEXT_HEAD

    p3 = tf_ty.add_paragraph()
    p3.alignment = PP_ALIGN.CENTER
    p3.space_before = Pt(16)
    r3 = p3.add_run()
    r3.text = (
        "🌐 Trang Web Live Production: https://fptu-event-hub.vercel.app/\n"
        "🐙 Kho Lưu Trữ Mã Nguồn GitHub: https://github.com/CongDung0506/FPTU-EventHub\n"
        "👥 Đội ngũ thực hiện: Trương Công Dũng (Lead) & Nhóm 5 Thành Viên"
    )
    r3.font.size = Pt(12)
    r3.font.color.rgb = TEXT_SUB

    p4 = tf_ty.add_paragraph()
    p4.alignment = PP_ALIGN.CENTER
    p4.space_before = Pt(20)
    r4 = p4.add_run()
    r4.text = "KÍNH MỜI THẦY CÔ TRONG HỘI ĐỒNG ĐẶT CÂU HỎI & GÓP Ý"
    r4.font.bold = True
    r4.font.size = Pt(13)
    r4.font.color.rgb = GREEN_DARK

    # Save presentation
    output_v2 = r"C:\Users\truon\fptu_eventhub\SLIDE_THUYET_TRINH_FPTU_EVENTHUB_CANVA_V2.pptx"
    output_bright = r"C:\Users\truon\fptu_eventhub\SLIDE_THUYET_TRINH_FPTU_EVENTHUB_CANVA_BRIGHT.pptx"
    output_main = r"C:\Users\truon\fptu_eventhub\SLIDE_THUYET_TRINH_FPTU_EVENTHUB.pptx"
    
    prs.save(output_v2)
    print(f"Canva-style bright V2 presentation saved successfully at: {output_v2}")
    
    for target in [output_bright, output_main]:
        try:
            prs.save(target)
            print(f"Also updated presentation at: {target}")
        except PermissionError:
            print(f"Notice: {target} is currently open in WPS/PowerPoint.")

if __name__ == "__main__":
    build_bright_deck()
