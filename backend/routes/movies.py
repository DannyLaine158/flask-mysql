from flask import Blueprint, request, jsonify
from models.movie_model import create_movie, get_movies, get_movie_by_id, update_movie, delete_movie

movies_bp = Blueprint("movies", __name__)

# 🔹 Funciones auxiliares de validación
def validar_entero(valor):
    try:
        return int(valor)
    except (ValueError, TypeError):
        return None

def validar_float(valor):
    if valor is None or valor == "":
        return None
    try:
        return float(valor)
    except (ValueError, TypeError):
        return None


# 📌 GET: Listar películas (con filtros opcionales)
@movies_bp.route("/", methods=["GET"])
def list_movies():
    order_by = request.args.get("order_by")
    genero = request.args.get("genero")
    year_from = validar_entero(request.args.get("year_from"))
    year_to = validar_entero(request.args.get("year_to"))
    min_rating = validar_float(request.args.get("min_rating"))

    movies = get_movies(order_by=order_by, genre=genero,
                        year_from=year_from, year_to=year_to, min_rating=min_rating)
    return jsonify(movies)


# 📌 GET: Obtener película por ID
@movies_bp.route("/<int:id>", methods=["GET"])
def get_movie(id):
    m = get_movie_by_id(id)
    if not m:
        return jsonify({"message": "No encontrado"}), 404
    return jsonify(m)


# 📌 POST: Crear nueva película
@movies_bp.route("/", methods=["POST"])
def add_movie():
    data = request.json
    
    titulo = data.get("titulo")
    director = data.get("director")
    anio = validar_entero(data.get("anio"))
    rating = validar_float(data.get("rating"))
    genero = data.get("genero")
    imagen = data.get("imagen")

    if not titulo or not director or anio is None:
        return jsonify({"message": "Título, director y año son obligatorios"}), 400

    if rating is None and data.get("rating") not in (None, ""):
        return jsonify({"message": "El rating debe ser un número válido"}), 400

    new_id = create_movie(titulo, director, anio, rating, genero, imagen)
    return jsonify({"message": "Película registrada", "id": new_id}), 201


# 📌 PUT: Editar película existente
@movies_bp.route("/<int:id>", methods=["PUT"])
def edit_movie(id):
    data = request.json
    m = get_movie_by_id(id)
    if not m:
        return jsonify({"message": "No encontrado"}), 404

    titulo = data.get("titulo", m["titulo"])
    director = data.get("director", m["director"])
    anio = validar_entero(data.get("anio")) if "anio" in data else m["anio"]
    rating = validar_float(data.get("rating")) if "rating" in data else m.get("rating")
    genero = data.get("genero", m.get("genero"))
    imagen = data.get("imagen", m.get("imagen"))

    if anio is None:
        return jsonify({"message": "El año debe ser un número entero válido"}), 400

    if rating is None and data.get("rating") not in (None, ""):
        return jsonify({"message": "El rating debe ser un número válido"}), 400

    update_movie(id, titulo, director, anio, rating, genero, imagen)
    return jsonify({"message": "Película actualizada"})


# 📌 DELETE: Eliminar película
@movies_bp.route("/<int:id>", methods=["DELETE"])
def remove_movie(id):
    m = get_movie_by_id(id)
    if not m:
        return jsonify({"message": "No encontrado"}), 404
    delete_movie(id)
    return jsonify({"message": "Película eliminada"})
