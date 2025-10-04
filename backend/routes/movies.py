from models.movie_model import create_movie, delete_movie, get_movie_by_id, get_movies_by_filter, update_movie
from flask import Blueprint, request, jsonify

movies_bp = Blueprint("movies", __name__)

def validar_entero(valor):
    if valor is None or valor == '':
        return None
    try:
        return int(valor) # "1992" -> 1992
    except (ValueError, TypeError):
        return None
    
def validar_float(valor):
    if valor is None or valor == '':
        return None
    try:
        return float(valor) # 4 -> 4.0
    except (ValueError, TypeError):
        return None

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
    year_from = validar_entero(request.args.get("year_from"))
    year_to = validar_entero(request.args.get("year_to"))
    min_rating = validar_float(request.args.get("min_rating"))
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
    anio = validar_entero(data.get("anio"))
    rating = validar_float(data.get("rating"))
    genero = data.get("genero")
    imagen = data.get("imagen")

    if anio is None:
        return jsonify({
            "message": "El año debe ser un número entero válido"
        }), 400

    if not titulo or not director is None:
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

@movies_bp.route("/<int:id>", methods=["PUT"])
def edit_movie(id):
    data = request.json
    movie = get_movie_by_id(id)
    
    if not movie:
        return jsonify({
            "message": "Película no encontrada"
        }), 404
    
    titulo = data.get("titulo")
    director = data.get("director")
    anio = validar_entero(data.get("anio"))
    rating = validar_float(data.get("rating"))
    genero = data.get("genero")
    imagen = data.get("imagen")

    if anio is None:
        return jsonify({
            "message": "El año debe ser un número entero válido"
        }), 400
    
    if rating is None and rating not in (None, ""):
        return jsonify({
            "message": "Rating debe ser número válido"
        }), 400
    
    result = update_movie(id, titulo, director, anio, rating, genero, imagen)
    if result:
        return jsonify({
            "message": "Película actualizada"
        })
    else:
        return jsonify({
            "error": "Faltan valores"
        }), 400
    
@movies_bp.route("/<int:id>", methods=["DELETE"])
def remove_movie(id):
    movie = get_movie_by_id(id)
    if not movie:
        return jsonify({
            "message": "Película no encontrada"
        }), 404
    
    if delete_movie(id):
        return jsonify({
            "message": "Película eliminada"
        })
    else:
        return jsonify({
            "message": "Error al eliminar película"
        }), 400