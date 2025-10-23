from database import get_db_connection
import mysql.connector

def create_movie(titulo, director, anio, rating, genero, imagen):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO peliculas (titulo, director, anio, rating, genero, imagen)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (titulo, director, anio, rating, genero, imagen)
        )
        conn.commit()
        last_id = cursor.lastrowid
        return last_id
    except mysql.connector.Error as err:
        print(f"Error en create_movie: {err}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def get_movie_by_id(id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM peliculas WHERE id = %s", (id,))
        row = cursor.fetchone()
        return row
    except mysql.connector.Error as err:
        print(f"Error en get_movie_by_id: {err}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def get_movies(order_by=None, genre=None, year_from=None, year_to=None, min_rating=None):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM peliculas"
        parts = []
        params = []

        # filtros opcionales
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

        if parts:
            query += " WHERE " + " AND ".join(parts)

        if order_by in ["titulo", "anio", "genero", "rating", "director"]:
            query += f" ORDER BY {order_by}"

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as err:
        print(f"Error en get_movies: {err}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def update_movie(id, titulo, director, anio, rating, genero, imagen):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
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
        print(f"Error en update_movie: {err}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def delete_movie(id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM peliculas WHERE id=%s", (id,))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        print(f"Error en delete_movie: {err}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
