# FPTU EventHub: Unit Tests & Regression Verification

import unittest
from datetime import datetime, timedelta
from app import app
from models import db, User, Role, Category, Event, Ticket, Review

class EventHubTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.app_context = app.app_context()
        self.app_context.push()

        db.drop_all()
        db.create_all()
        Role.insert_roles()

        self.role_student = Role.query.filter_by(name="Student").first()
        self.role_organizer = Role.query.filter_by(name="Organizer").first()

        self.user = User(
            student_id="DE200433",
            full_name="Trương Công Dũng",
            email="dungtc@fpt.edu.vn",
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

        self.cat = Category(name="Công Nghệ & AI", slug="tech-ai")

        self.event = Event(
            title="Workshop AI Agent",
            slug="workshop-ai",
            venue="Hội trường Alpha",
            start_time=datetime.now() + timedelta(days=2),
            end_time=datetime.now() + timedelta(days=2, hours=2),
            total_capacity=10,
            available_slots=10,
            pdp_points=15,
            category=self.cat,
            organizer=self.organizer
        )

        db.session.add_all([self.user, self.organizer, self.cat, self.event])
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
        u = User.query.filter_by(student_id="DE200433").first()

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
        u = User.query.filter_by(student_id="DE200433").first()

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

    def test_check_in_and_pdp_points_logic(self):
        ev = Event.query.first()
        u = User.query.filter_by(student_id="DE200433").first()

        t = Ticket(
            ticket_code="FU-2026-TEST01",
            event=ev,
            user=u,
            status="REGISTERED"
        )
        db.session.add(t)
        db.session.commit()

        self.assertIsNone(t.checked_in_at)
        self.assertEqual(u.total_pdp_points, 0)

        # Check-in -> Tich luy diem PDP
        t.status = "CHECKED_IN"
        t.checked_in_at = datetime.utcnow()
        db.session.commit()

        self.assertEqual(t.status, "CHECKED_IN")
        self.assertIsNotNone(t.checked_in_at)
        self.assertEqual(u.total_pdp_points, 15)

    def test_event_review_and_average_rating(self):
        ev = Event.query.first()
        u = User.query.filter_by(student_id="DE200433").first()

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

    def test_user_pdp_rank_levels(self):
        u = self.user
        self.assertEqual(u.total_pdp_points, 0)
        self.assertEqual(u.pdp_rank["title"], "Tân Binh Trường F")
        self.assertEqual(u.pdp_rank["icon"], "🥉")

        # Mock tickets to give 15 points
        t = Ticket(ticket_code="FU-2026-MOCK1", event=self.event, user=u, status="CHECKED_IN")
        db.session.add(t)
        db.session.commit()

        self.assertEqual(u.total_pdp_points, 15)
        self.assertEqual(u.pdp_rank["title"], "Chiến Binh Năng Nổ")
        self.assertEqual(u.pdp_rank["icon"], "🥈")

if __name__ == "__main__":
    unittest.main()
