import json

from flask import Flask, render_template

from routes.movie_list_bp import movie_list_bp
from routes.movies_bp import movies_bp

app = Flask(__name__)


@app.get("/")
def hello_world():
    return "<h2>hey, flask!!</h2>"


name = "Ethan"
hobbies = ["Gaming", "Reading", "Soccer", "Ballet", "Gyming", "Yoga"]


@app.get("/about")
def about_page():
    return render_template("about.html", name=name, hobbies=hobbies)


# Task 2 - Create profile page
@app.get("/profile")
def profile_page():
    with open("pokemon.json", "r") as file:
        profiles = json.load(file)

    return render_template("profile.html", profiles=profiles)


# Flask - Blueprints
app.register_blueprint(movies_bp, url_prefix="/movies")
app.register_blueprint(movie_list_bp, url_prefix="/movie-list")


if __name__ == "__main__":
    app.run(debug=True)
