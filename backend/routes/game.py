from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from ..db import db
from ..models import Question, User
import random

game_bp = Blueprint("game", __name__, url_prefix="/app")


@game_bp.route("/dashboard")
@login_required
def dashboard():
    # ensure streak updated whenever they visit dashboard
    current_user.update_streak()
    db.session.commit()

    # For demo: count total questions per level
    levels = {}
    for lvl in range(1, 6):
        levels[lvl] = Question.query.filter_by(level=lvl).count()

    return render_template(
        "dashboard.html",
        user=current_user,
        levels=levels,
    )


@game_bp.route("/play/<int:level>", methods=["GET"])
@login_required
def play_level(level):
    if level < 1 or level > 5:
        return redirect(url_for("game.dashboard"))

    # Simple rule: for demo, pick up to 5 questions for this level
    questions = Question.query.filter_by(level=level).limit(5).all()

    return render_template(
        "play.html",
        user=current_user,
        level=level,
        questions=questions,
    )


@game_bp.route("/submit", methods=["POST"])
@login_required
def submit_answers():
    level = int(request.form.get("level"))
    correct_count = 0
    total = 0

    for key, value in request.form.items():
        if not key.startswith("q_"):
            continue
        qid = int(key.split("_", 1)[1])
        selected = value
        q = Question.query.get(qid)
        if not q:
            continue
        total += 1
        if selected == q.correct_option:
            correct_count += 1

    # Simple XP logic: 10 XP per correct
    gained_xp = correct_count * 10
    current_user.add_xp(gained_xp)
    current_user.update_streak()
    db.session.commit()

    return render_template(
        "play.html",
        user=current_user,
        level=level,
        result={"correct": correct_count, "total": total, "xp": gained_xp},
        questions=Question.query.filter_by(level=level).limit(5).all(),
    )


@game_bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@game_bp.route("/avatar", methods=["POST"])
@login_required
def change_avatar():
    avatar = request.json.get("avatar")
    if avatar not in ["piggy", "rocket", "shield", "lightbulb"]:
        return jsonify({"status": "error", "message": "Invalid avatar"}), 400

    current_user.avatar = avatar
    db.session.commit()
    return jsonify({"status": "ok"})


@game_bp.route("/daily", methods=["GET"])
@login_required
def daily_questions():
    """Return today's daily set for the current user's level (simple demo)."""
    user_level = current_user.level
    questions = Question.query.filter_by(level=user_level).limit(3).all()
    data = []
    for q in questions:
        data.append(
            {
                "id": q.id,
                "text": q.text,
                "options": {
                    "A": q.option_a,
                    "B": q.option_b,
                    "C": q.option_c,
                    "D": q.option_d,
                },
            }
        )
    return jsonify(
        {
            "date": date.today().isoformat(),
            "level": user_level,
            "questions": data,
        }
    )

@game_bp.route("/minigame", methods=["GET"])
@login_required
def minigame():
    scenarios = [
        {
            "id": 1,
            "title": "Birthday Blast 🎂",
            "amount": 500,
            "text": "You got ₹500 as birthday gift money. Plan how much to use for fun, how much to save for a future gadget, and how much to keep for emergencies."
        },
        {
            "id": 2,
            "title": "Festival Bonus 🪔",
            "amount": 800,
            "text": "You received ₹800 during a festival. You want some snacks, maybe a small toy, but also want to save for a school trip later."
        },
        {
            "id": 3,
            "title": "Monthly Pocket Money 💸",
            "amount": 300,
            "text": "You get ₹300 pocket money each month. Split it so you can enjoy now and still be smart for later."
        },
    ]
    scenario = random.choice(scenarios)
    return render_template("minigame.html", user=current_user, scenario=scenario)


@game_bp.route("/minigame_result", methods=["POST"])
@login_required
def minigame_result():
    data = request.get_json() or {}
    xp = int(data.get("xp", 0))
    if xp < 0:
        xp = 0

    current_user.add_xp(xp)
    current_user.update_streak()
    db.session.commit()

    return jsonify(
        {
            "status": "ok",
            "new_xp": current_user.xp,
            "level": current_user.level,
            "streak": current_user.streak,
            "xp_added": xp,
        }
    )

