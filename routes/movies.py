from flask import Blueprint, request
from database import get_db
import mysql.connector

movies_bp = Blueprint("movies", __name__)

@movies_bp.route("/")
def saludar():
    return { "Movie": "Pon una pelicula en la URL" }

@movies_bp.route("/list")
def listMovies():
    conn = None
    cursor = None
    try:
        # 1. Conectamos con mysql
        conn = get_db()
        # 2. Pedimos las tablas en forma de diccionario
        cursor = conn.cursor(dictionary=True)
        # 3. Crear la consulta a mysql
        query = "SELECT * FROM peliculas;"
        # 4. Ejecutar la consulta
        cursor.execute(query)
        # 5. Recibir las tablas
        rows = cursor.fetchall() # Obtiene todas las filas
        # 6. Retornar la información
        return rows
    except mysql.connector.Error as err:
        print("Error al traer peliculas ", err)
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()