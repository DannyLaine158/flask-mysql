from flask import Blueprint, request

movies_bp = Blueprint("movies", __name__)

@movies_bp.route("/")
def saludar():
    return { "Movie": "Pon una pelicula en la URL" }

@movies_bp.route("/list")
def listMovies():
    data = request.args.get("movie")
    print(data)
    return { "Movie": data }