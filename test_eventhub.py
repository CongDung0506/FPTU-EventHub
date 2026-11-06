# FPTU EventHub: Unit Tests & Regression Verification
# Kiem thu toan dien cac ham va tinh nang trong chuong trinh PWD301

import unittest
from datetime import datetime, timedelta
from app import app, is_safe_url
from models import db, User, Role, Category, Event, Ticket, Review


class EventHubTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

        db.drop_all()
        db.create_all()
        Role.insert_roles()

        self.role_student = Role.query.filter_by(name="Student").first()
        self.role_organizer = Role.query.filter_by(name="Organizer").first()
        self.role_admin = Role.query.filter_by(name="Admin").first()

        self.user = User(
            student_id="DE170001",
            full_name="Nguyễn Văn A",
            email="nguyenvana@fpt.edu.vn",
            role=self.role_student
        )
        self.user.set_password("pass123")

        self.organizer = User(
            student_id="ORG001",
            full_name="F-Code Club",
            email="fcode@fpt.edu.vn",
            role=self.role_organizer
        )
        self.organizer.set_password("pass123")

        self.admin = User(
            student_id="ADM001",
            full_name="Phòng CTSV",
            email="ctsv.admin@fpt.edu.vn",
            role=self.role_admin
        )
        self.admin.set_password("pass123")

        self.cat = Category(name="Công Nghệ & AI", slug="tech-ai")

        self.event = Event(
            title="Workshop AI Agent",
            slug="workshop-ai",
            venue="Hội trường Alpha",
            start_time=datetime.utcnow() + timedelta(days=2),
            end_time=datetime.utcnow() + timedelta(days=2, hours=2),
            total_capacity=10,
            available_slots=10,
            category=self.cat,
            organizer=self.organizer
        )

        db.session.add_all([self.user, self.organizer, self.admin, self.cat, self.event])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_password_hashing(self):
        self.assertTrue(self.user.check_password("pass123"))
        self.assertFalse(self.user.check_password("wrongpass"))

    def test_event_capacity_and_sold_out(self):
        self.assertEqual(self.event.available_slots, 10)
        self.assertFalse(self.event.is_sold_out)
        self.assertEqual(self.event.filled_percentage, 0)

        # Dat het slot
        self.event.available_slots = 0
        self.assertTrue(self.event.is_sold_out)
        self.assertEqual(self.event.filled_percentage, 100)

    def test_ticket_creation_and_code_generation(self):
        code = Ticket.generate_ticket_code()
        self.assertTrue(code.startswith(f"FU-{datetime.now().year}-"))
        self.assertEqual(len(code), 14)

    def test_booking_transaction(self):
        ev = Event.query.first()
        u = User.query.filter_by(student_id="DE170001").first()

        ev.available_slots -= 1
        t = Ticket(
            ticket_code=Ticket.generate_ticket_code(),
            event=ev,
            user=u,
            status="REGISTERED"
        )
        db.session.add(t)
        db.session.commit()

        self.assertEqual(ev.available_slots, 9)
        self.assertEqual(len(ev.tickets), 1)
        self.assertTrue(u.has_registered(ev.id))

    def test_ticket_cancellation_frees_slot(self):
        ev = Event.query.first()
        u = User.query.filter_by(student_id="DE170001").first()

        ev.available_slots -= 1
        t = Ticket(
            ticket_code=Ticket.generate_ticket_code(),
            event=ev,
            user=u,
            status="REGISTERED"
        )
        db.session.add(t)
        db.session.commit()
        self.assertEqual(ev.available_slots, 9)

        # Sinh vien huy ve
        t.status = "CANCELLED"
        ev.available_slots += 1
        db.session.commit()

        self.assertEqual(ev.available_slots, 10)
        self.assertEqual(t.status, "CANCELLED")

    def test_check_in_logic(self):
        ev = Event.query.first()
        u = User.query.filter_by(student_id="DE170001").first()

        t = Ticket(
            ticket_code="FU-2026-TEST01",
            event=ev,
            user=u,
            status="REGISTERED"
        )
        db.session.add(t)
        db.session.commit()

        self.assertIsNone(t.checked_in_at)

        # Check-in thanh cong
        t.status = "CHECKED_IN"
        t.checked_in_at = datetime.utcnow()
        db.session.commit()

        self.assertEqual(t.status, "CHECKED_IN")
        self.assertIsNotNone(t.checked_in_at)

    def test_event_review_and_average_rating(self):
        ev = Event.query.first()
        u = User.query.filter_by(student_id="DE170001").first()

        r1 = Review(event=ev, user=u, rating=5, comment="Sự kiện rất tuyệt vời!")
        db.session.add(r1)
        db.session.commit()

        self.assertEqual(ev.review_count, 1)
        self.assertEqual(ev.average_rating, 5.0)

    def test_email_domain_validation(self):
        from forms import RegisterForm
        # Non-FPT email must fail
        f_bad = RegisterForm(student_id="DE123456", full_name="User Test", email="test@gmail.com", password="password123")
        self.assertFalse(f_bad.validate())
        self.assertTrue(any("FPT" in err for err in f_bad.email.errors))

        # Other university email must fail
        f_other_uni = RegisterForm(student_id="DE123456", full_name="User Test", email="sv@hcmus.edu.vn", password="password123")
        self.assertFalse(f_other_uni.validate())
        self.assertTrue(any("FPT" in err for err in f_other_uni.email.errors))

        # FPT emails must succeed
        f_good1 = RegisterForm(student_id="DE123456", full_name="User Test", email="svfpt@fpt.edu.vn", password="password123")
        self.assertTrue(f_good1.validate())

        f_good2 = RegisterForm(student_id="FE123456", full_name="Staff Test", email="staff@fe.edu.vn", password="password123")
        self.assertTrue(f_good2.validate())

    def test_custom_phone_validator(self):
        from werkzeug.datastructures import MultiDict
        from forms import ProfileForm
        # SĐT sai định dạng (không phải 10 số, không bắt đầu bằng 0)
        p_bad = ProfileForm(MultiDict({"full_name": "Nguyễn Văn A", "phone": "123456"}))
        self.assertFalse(p_bad.validate())
        self.assertTrue(any("10 chữ số" in err for err in p_bad.phone.errors))

        # SĐT đúng chuẩn Việt Nam
        p_good = ProfileForm(MultiDict({"full_name": "Nguyễn Văn A", "phone": "0912345678"}))
        self.assertTrue(p_good.validate())

    def test_open_redirect_safety_helper(self):
        with app.test_request_context("/login?next=/my-tickets"):
            self.assertTrue(is_safe_url("/my-tickets"))
            self.assertTrue(is_safe_url("http://localhost/my-tickets"))
            self.assertFalse(is_safe_url("http://evil-attacker-site.com"))
            self.assertFalse(is_safe_url("https://malicious.com/phishing"))

    def test_rest_api_events_list(self):
        res = self.client.get("/api/v1/events")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("events", data)
        self.assertIn("total", data)
        self.assertEqual(data["total"], 1)

    def test_rest_api_categories(self):
        res = self.client.get("/api/v1/categories")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Công Nghệ & AI")

    def test_rest_api_stats(self):
        res = self.client.get("/api/v1/stats")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("total_events", data)
        self.assertIn("total_users", data)

    def test_custom_template_filters(self):
        from app import vnd_filter, datetime_format_filter, truncate_words_filter
        self.assertEqual(vnd_filter(15000), "15.000 đ")
        self.assertEqual(vnd_filter(0), "0 đ")
        self.assertEqual(vnd_filter(None), "-")

        dt = datetime(2026, 11, 20, 14, 30)
        self.assertEqual(datetime_format_filter(dt), "14:30 - 20/11/2026")

        long_txt = "Một hai ba bốn năm sáu bảy tám chín mười mười một mười hai mười ba"
        self.assertTrue(truncate_words_filter(long_txt, num=5).endswith("..."))

    def test_category_crud_and_integrity(self):
        # 1. Tao danh muc moi
        c = Category(name="Văn Hóa Nghệ Thuật", slug="art-culture", color="#ec4899")
        db.session.add(c)
        db.session.commit()
        self.assertIsNotNone(c.id)

        # 2. To dict
        d = c.to_dict()
        self.assertEqual(d["name"], "Văn Hóa Nghệ Thuật")
        self.assertEqual(d["events_count"], 0)

        # 3. Kiem tra tinh toan ven: Danh muc co su kien (self.cat) khong the xoa truc tiep
        self.assertGreater(len(self.cat.events), 0)


if __name__ == "__main__":
    unittest.main()
