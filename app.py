from flask import Flask

from routes.main_bp import main_bp
from routes.movie_list_bp import movie_list_bp
from routes.movies_bp import movies_bp

app = Flask(__name__)
# SERVER_NAME = PF4630GS\SQLEXPRESS

# Flask - Blueprints
app.register_blueprint(main_bp, url_prefix="/")
app.register_blueprint(movies_bp, url_prefix="/movies")
app.register_blueprint(movie_list_bp, url_prefix="/movie-list")


if __name__ == "__main__":
    app.run(debug=True)
