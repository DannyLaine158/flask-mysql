import os # Hacer funcionar cosas del sistema operativo
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

def get_db():
    try:
        # Configuración:
        cfg = {
            "host": os.environ["DB_HOST"],
            "user": os.environ["DB_USER"],
            "password": os.environ["DB_PASSWORD"],
            "database": os.environ["DB_NAME"]
        }

        # Conexion a mysql
        conn = mysql.connector.connect(**cfg)
        if conn.is_connected():
            print("Conexión establecida a mysql")
            return conn
    
    except Error as e:
        print("Error al conectarse ", e)
        return None