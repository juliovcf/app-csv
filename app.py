from flask import Flask
from modules.views import configure_routes
from modules.database import init_db

app = Flask(__name__)
app.secret_key = 'jperecab'  # Añade una clave secreta

# Inicializa la base de datos
init_db()

# Configura las rutas
configure_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
