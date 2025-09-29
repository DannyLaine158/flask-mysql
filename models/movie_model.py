from database import get_db
import mysql.connector

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

# Obtener una pelicula por su id
def get_movie_by_id(id):
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM peliculas WHERE id = %s", (id,))
        row = cursor.fetchone()
        return row
    except mysql.connector.Error as err:
        print("Error al obtener pelicula ", {err})
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# Obtener peliculas con filtros personalizados
def get_movies_by_filter(genre=None, year_from=None, year_to=None, min_rating=None):
    conn = None
    cursor = None
    try:
        conn = get_db()
        query = "SELECT * FROM peliculas"
        cursor = conn.cursor(dictionary=True)
        parts = [] # Filtros
        params = []

        if genre:
            parts.append("genero = %s")
            params.append(genre)
        if year_from:
            parts.append("anio >= %s")
            params.append(year_from)
        if year_to:
            parts.append("anio <= %s")
            params.append(year_to)
        if min_rating:
            parts.append("rating >= %s")
            params.append(min_rating)

        # Si vienen filtros del WHERE
        if parts:
            query += " WHERE " + " OR ".join(parts)

        # print(query)

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as err:
        print("Error con los filtros ", {err})
    finally:
        if cursor: cursor.close()
        if conn: conn.close()