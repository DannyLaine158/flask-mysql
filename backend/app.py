from flask import Flask
from routes.movies import movies_bp
from database import get_db

# Instancia de Flask
app = Flask(__name__)

# Registro de blueprints:
app.register_blueprint(movies_bp, url_prefix="/movies")

# Endpoint root
@app.route("/")
def hello():
    try:
        conn = get_db()
        cursor = conn.cursor()
        # Comando de prueba
        cursor.execute("SELECT NOW();")
        result = cursor.fetchone() # Esperamos 1 fila
        return { "time": str(result[0]) }
    except Exception as e:
        return { "error": str(e) }
    # return {"Hola": "Este es un saludo"}

# Punto de partida:
if __name__ == "__main__":
    app.run(debug=True)