from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..db import db
from ..models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def landing():
    if current_user.is_authenticated:
        return redirect(url_for("game.dashboard"))
    return render_template("landing.html")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        avatar = request.form.get("avatar", "piggy")

        if not username or not password:
            flash("Please fill all fields.", "error")
            return redirect(url_for("auth.signup"))

        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "error")
            return redirect(url_for("auth.signup"))

        user = User(username=username, avatar=avatar)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for("game.dashboard"))

    return render_template("landing.html", show_signup=True)


@auth_bp.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        flash("Invalid username or password", "error")
        return redirect(url_for("auth.landing"))

    login_user(user)
    return redirect(url_for("game.dashboard"))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.landing"))
