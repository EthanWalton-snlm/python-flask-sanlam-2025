from flask import Blueprint, render_template

from models.movies import Movie

movie_list_bp = Blueprint("movie_list_bp", __name__)


def get_all_movies():
    movies = Movie.query.all()
    return [movie.to_dict() for movie in movies]


@movie_list_bp.get("/")
def movies_page():
    return render_template("movie-list.html", movies=get_all_movies())


@movie_list_bp.get("/<id>")
def movie_details_page(id):
    movie = Movie.query.get(id)

    if movie is None:
        return render_template("not-found.html")

    return render_template("movie-details.html", movie=movie.to_dict())
