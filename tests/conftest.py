import pytest
from flask import Flask
from src.rutas import crea_rutas


@pytest.fixture()
def app():
    app = Flask(__name__)
    app.config.update({
        "TESTING": True,
    })
    
    crea_rutas(app)

    

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()
