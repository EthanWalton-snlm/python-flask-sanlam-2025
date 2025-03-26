import json

from flask import Blueprint, render_template

from routes.movies_bp import get_movie_by_id

movie_list_bp = Blueprint("movie_list_bp", __name__)

with open("movies.json", "r") as file:
    movies = json.load(file)


# Task 3
@movie_list_bp.get("/")
def movies_page():
    return render_template("movie-list.html", movies=movies)


# Task 4
@movie_list_bp.get("/<id>")
def movie_page_by_id(id):
    movie = get_movie_by_id(id)

    return render_template("movie-details.html", movie=movie)
