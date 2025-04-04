from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

from extensions import db
from models.movies import Movie

movie_list_bp = Blueprint("movie_list_bp", __name__)


def get_all_movies():
    movies = Movie.query.all()
    return [movie.to_dict() for movie in movies]


@movie_list_bp.get("/")
@login_required
def movies_page():
    return render_template("movie-list.html", movies=get_all_movies())


@movie_list_bp.get("/<id>")
@login_required
def movie_details_page(id):
    movie = Movie.query.get(id)

    if movie is None:
        return render_template("not-found.html")

    return render_template("movie-details.html", movie=movie.to_dict())


@movie_list_bp.get("/new")
@login_required
def add_movie():
    return render_template("add-movie.html")


@movie_list_bp.post("/")
@login_required
def create_movie():
    data = {
        "name": request.form.get("name"),
        "poster": request.form.get("poster"),
        "rating": request.form.get("rating"),
        "summary": request.form.get("summary"),
        "trailer": request.form.get("trailer"),
    }
    new_movie = Movie(**data)

    try:
        db.session.add(new_movie)
        db.session.commit()

        # return {
        #     "message": "Movie created successfully",
        #     "data": new_movie.to_dict(),
        # }, STATUS_CODE["CREATED"]
        return redirect(url_for("movie_list_bp.movies_page"))
    except Exception:
        db.session.rollback()  # restores data, cannot be done after commit()
        return redirect(url_for("movie_list_bp.add_movie"))


@movie_list_bp.post("/<id>")
@login_required
def delete_movie_by_id(id):
    movie = Movie.query.get(id)

    if movie is None:
        return render_template("not-found.html")

    try:
        db.session.delete(movie)
        db.session.commit()

        print("Deleted", id)
        return redirect(url_for("movie_list_bp.movies_page"))
    except Exception:
        db.session.rollback()  # restores data, cannot be done after commit()
        return redirect(url_for("movie_list_bp.movies_page"))
