from datetime import date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    # Game-related profile
    avatar = db.Column(db.String(50), default="piggy")
    level = db.Column(db.Integer, default=1)       # 1–5 demo
    xp = db.Column(db.Integer, default=0)
    streak = db.Column(db.Integer, default=0)
    last_active_date = db.Column(db.Date, nullable=True)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def add_xp(self, amount: int):
        LEVEL_MAX = 5
        XP_PER_LEVEL = 100  # simple rule for demo
        self.xp += amount
        # Level up logic (simple for hackathon)
        while self.level < LEVEL_MAX and self.xp >= self.level * XP_PER_LEVEL:
            self.level += 1

    def update_streak(self):
        today = date.today()
        if self.last_active_date is None:
            self.streak = 1
        else:
            delta = (today - self.last_active_date).days
            if delta == 1:
                self.streak += 1
            elif delta > 1:
                self.streak = 1
        self.last_active_date = today


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False)        # 1–5
    topic = db.Column(db.String(40), nullable=False)     # basic, personal, scams, banking, govt
    text = db.Column(db.String(300), nullable=False)
    option_a = db.Column(db.String(200), nullable=False)
    option_b = db.Column(db.String(200), nullable=False)
    option_c = db.Column(db.String(200), nullable=False)
    option_d = db.Column(db.String(200), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)  # "A"/"B"/"C"/"D"


def seed_questions():
    """Seed a small bank of kid-level questions if empty."""
    if Question.query.first():
        return

    questions = [
        # Basic finance
        Question(
            level=1,
            topic="basic",
            text="You get pocket money of ₹200. What is the BEST first step?",
            option_a="Spend it all on snacks right now",
            option_b="Plan how much to spend and how much to save",
            option_c="Hide it and never touch it",
            option_d="Lend it all to a friend",
            correct_option="B",
        ),
        Question(
            level=1,
            topic="basic",
            text="What is a 'budget'?",
            option_a="A secret code for rich people",
            option_b="Money your parents keep at the bank",
            option_c="A simple plan for how you’ll use your money",
            option_d="An app on your phone",
            correct_option="C",
        ),
        # Personal finance
        Question(
            level=2,
            topic="personal",
            text="You want new headphones. What is a smart move?",
            option_a="Borrow money from 5 friends",
            option_b="Use all your savings at once",
            option_c="Set a savings goal and save a bit every week",
            option_d="Wait for your parents to randomly buy it",
            correct_option="C",
        ),
        # Scam awareness
        Question(
            level=2,
            topic="scams",
            text="A stranger messages: 'You won ₹1,00,000! Send your bank details.' What should you do?",
            option_a="Send details quickly before offer ends",
            option_b="Ignore and tell a trusted adult",
            option_c="Ask for half the money first",
            option_d="Send your friend’s account instead",
            correct_option="B",
        ),
        # Banking system
        Question(
            level=3,
            topic="banking",
            text="Why do people keep money in a bank?",
            option_a="So they can't see it again",
            option_b="To keep it safe and sometimes earn interest",
            option_c="Because cash is illegal",
            option_d="Because banks give free food",
            correct_option="B",
        ),
        # Govt schemes (kid-level)
        Question(
            level=3,
            topic="govt",
            text="Why does the government give scholarships or saving schemes for students?",
            option_a="So children buy more toys",
            option_b="To help families save for education and future",
            option_c="To make schools richer",
            option_d="So kids don't eat outside food",
            correct_option="B",
        ),
        # A couple of higher-level demo Qs
        Question(
            level=4,
            topic="scams",
            text="Someone asks for your OTP for 'verification'. What do you do?",
            option_a="Share it if their profile picture looks real",
            option_b="Share it only if they say they’re from the bank",
            option_c="Never share, OTP is secret",
            option_d="Share it if they promise a reward",
            correct_option="C",
        ),
        Question(
            level=5,
            topic="personal",
            text="What is an 'emergency fund'?",
            option_a="Money only for buying gadgets",
            option_b="Money kept for surprise needs like health or travel",
            option_c="Money to lend to friends",
            option_d="Money for online games only",
            correct_option="B",
        ),
    ]

    db.session.add_all(questions)
    db.session.commit()
    print(f"Seeded {len(questions)} questions.")
