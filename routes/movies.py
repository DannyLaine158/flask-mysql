from models.movie_model import create_movie, get_movie_by_id, get_movies_by_filter
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
    order_by = request.args.get("order_by")
    desc = request.args.get("desc")

    movies = get_movies_by_filter(genre=genero, year_from=year_from, 
        year_to=year_to, min_rating=min_rating, order_by=order_by, desc=desc)
    
    return jsonify(movies)

@movies_bp.route("/", methods=["POST"])
def add_movie():
    # Recibimos los datos como JSON
    data = request.json

    titulo = data.get("titulo")
    director = data.get("director")
    anio = data.get("anio")
    rating = data.get("rating")
    genero = data.get("genero")
    imagen = data.get("imagen")

    if not titulo or not director or anio is None:
        return jsonify({
            "message": "Titulo, director y año son obligatorios"
        }), 400
    
    if rating is None and rating not in (None, ""):
        return jsonify({
            "message": "Rating debe ser número válido"
        }), 400
    
    new_id = create_movie(titulo, director, anio, rating, genero, imagen)
    return jsonify({
        "message": "Película registrada",
        "id": new_id
    }), 201