from flask import Flask
from src.rutas import crea_rutas


app = Flask(__name__)

crea_rutas(app)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
