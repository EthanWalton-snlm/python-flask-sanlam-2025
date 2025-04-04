import json

from flask import Blueprint, render_template
from flask_login import login_required

main_bp = Blueprint("main_bp", __name__)

name = "Ethan"
hobbies = ["Gaming", "Reading", "Soccer", "Ballet", "Gyming", "Yoga"]


@main_bp.get("/")
def hello_world():
    return render_template("home.html")


@main_bp.get("/about")
@login_required
def about_page():
    return render_template("about.html", name=name, hobbies=hobbies)


@main_bp.get("/profile")
@login_required
def profile_page():
    with open("profiles.json", "r") as file:
        profiles = json.load(file)

    return render_template("profile.html", profiles=profiles)
