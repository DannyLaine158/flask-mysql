from models.movie_model import get_movie_by_id, get_movies_by_filter, listMovies
from flask import Blueprint, request, jsonify

movies_bp = Blueprint("movies", __name__)

@movies_bp.route("/<int:id>", methods=["GET"])
def get_movie(id):
    movie = get_movie_by_id(id)
    if not movie:
        return jsonify({
            "message": "No encontrado"
        }), 404
    return jsonify(movie)

@movies_bp.route("/", methods=["GET"])
def get_movies_filter():
    genero = request.args.get("genero")
    year_from = request.args.get("year_from")
    year_to = request.args.get("year_to")
    min_rating = request.args.get("min_rating")

    movies = get_movies_by_filter(genre=genero, year_from=year_from, 
        year_to=year_to, min_rating=min_rating)
    
    return jsonify(movies)