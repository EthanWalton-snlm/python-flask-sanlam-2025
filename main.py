from flask import Flask

from routes.movies_bp import movies_bp

app = Flask(__name__)


@app.get("/")
def hello_world():
    return "<h2>hey, flask!!</h2>"


# Flask - Blueprints
app.register_blueprint(movies_bp)


if __name__ == "__main__":
    app.run(debug=True)
