from flask import Flask
from flask_login import LoginManager
from sqlalchemy.sql import text

from config import Config
from extensions import db
from models.user import User
from routes.auth_bp import auth_bp
from routes.main_bp import main_bp
from routes.movie_list_bp import movie_list_bp
from routes.movies_bp import movies_bp


# Flask - Blueprints
def create_app():
    # global movies

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login_page"  # type: ignore

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)  # maintains tokens for specific users

    with app.app_context():
        try:
            result = db.session.execute(text("SELECT 1")).fetchall()
            # movies_objs = Movie.query.all()
            # movies = [movie.to_dict() for movie in movies_objs]
            print("Connection successful:", result)
        except Exception as e:
            print("Error connecting to the database:", e)

    app.register_blueprint(main_bp)
    app.register_blueprint(movies_bp, url_prefix="/movies")
    app.register_blueprint(movie_list_bp, url_prefix="/movie-list")
    app.register_blueprint(auth_bp)

    return app


if __name__ == "__main__":
    app = create_app()

    app.run(debug=True)
