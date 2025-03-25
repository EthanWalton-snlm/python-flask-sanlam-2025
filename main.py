from flask import Flask, render_template

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


# Flask - Blueprints
app.register_blueprint(movies_bp, url_prefix="/movies")


if __name__ == "__main__":
    app.run(debug=True)
