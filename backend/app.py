from flask import Flask
from routes.movies import movies_bp

# Instancia de Flask
app = Flask(__name__)

# Registro de blueprints:
app.register_blueprint(movies_bp, url_prefix="/movies")

# Endpoint root
@app.route("/")
def hello():
    return {"Hola": "Este es un saludo"}

# Punto de partida:
if __name__ == "__main__":
    app.run(debug=True)