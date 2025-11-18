from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from pathlib import Path
from .db import db
from .models import User, Question, seed_questions


def create_app():
    base_dir = Path(__file__).resolve().parent.parent

    app = Flask(
        __name__,
        template_folder=str(base_dir / "frontend" / "templates"),
        static_folder=str(base_dir / "frontend" / "static"),
    )

    app.config["SECRET_KEY"] = "dev-rupee-rangers-secret"  # change for prod
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rupee_rangers.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes.auth import auth_bp
    from .routes.game import game_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(game_bp)

    with app.app_context():
        db.create_all()
        if not Question.query.first():
            seed_questions()

    @app.cli.command("init-db")
    def init_db():
        db.create_all()
        seed_questions()
        print("Database initialized and questions seeded.")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
