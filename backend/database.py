import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()  # carga .env si existe

def get_db_connection():
    cfg = {
        "host": os.environ.get("DB_HOST", "localhost"),
        "user": os.environ.get("DB_USER", "root"),
        "password": os.environ.get("DB_PASSWORD", ""),
        "database": os.environ.get("DB_NAME", "peliculas_db"),
    }

    conn = mysql.connector.connect(**cfg)
    return conn
