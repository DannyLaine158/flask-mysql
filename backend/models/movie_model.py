from database import get_db
import mysql.connector

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
def get_movies_by_filter(genre=None, year_from=None, year_to=None, 
        min_rating=None, order_by=None, desc=None):
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

        if order_by in ["titulo", "anio", "genero", "rating", "director"]:
            # print(type(desc))
            if desc == "True":
                query += f" ORDER BY {order_by} DESC"
            else:
                query += f" ORDER BY {order_by}"

        # print(query)

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as err:
        print("Error con los filtros ", {err})
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def create_movie(titulo, director, anio, rating, genero, imagen):
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO peliculas (titulo, director, anio, rating, genero, imagen)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (titulo, director, anio, rating, genero, imagen)
        )
        conn.commit()
        last_id = cursor.lastrowid # Devuelve el ultimo ID
        return last_id
    except mysql.connector.Error as err:
        print("Error al crear película ", {err})
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def update_movie(id, titulo, director, anio, rating, genero, imagen):
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE peliculas
            SET titulo=%s, director=%s, anio=%s, rating=%s, genero=%s, imagen=%s
            WHERE id=%s
            """,
            (titulo, director, anio, rating, genero, imagen, id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        print("Error al actualizar ", {err})
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def delete_movie(id):
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM peliculas WHERE id=%s", (id,))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        print("Error al eliminar ", {err})
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()