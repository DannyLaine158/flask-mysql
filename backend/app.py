from flask import Flask
from flask_cors import CORS
from routes.movies import movies_bp
from database import get_db_connection

app = Flask(__name__)
CORS(app)

app.register_blueprint(movies_bp, url_prefix="/movies")

@app.route("/")
def hello():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT NOW()")  # comando de prueba
        result = cursor.fetchone()
        conn.close()
        return {"status": "ok", "db_time": str(result[0])}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    # return {"Clave": "API Películas: /movies"}

if __name__ == "__main__":
    app.run(debug=True)
