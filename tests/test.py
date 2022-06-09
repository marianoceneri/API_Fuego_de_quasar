import pytest
from flask import request
from src.satelites import satelites
import json

#Testeo ruta /app/v1/topsecret/ POST
def test_topsecret(client):

    url = "/app/v1/topsecret/"

    jsonData = {'satellites': [
        {
            'name': 'kenobi',
            'distance': 100.0,
            'message': ['', '', 'Este', 'es', 'un', 'mensaje', 'secreto']
        },
        {
            'name': 'skywalker',
            'distance': 115.5,
            'message': ['', 'Este', 'es', 'un', '', 'secreto']
        },
        {
            'name': 'sato',
            'distance': 142.7,
            'message': ['', '', '', '', '', 'Este', '', 'un', 'mensaje', 'secreto']
        }

    ]
    }

    response = client.post(url,  json=jsonData)

    assert response.status_code == 200
    assert b"El mensaje no puede ser descifrado" not in response.data
    
#Testteo de carga via POST kenobi
def test_topsecret_split_post_kenobi(client):

    url = "/app/v1/topsecret_split/kenobi"

    jsonData = {
        "distance": 100.0,
        "message": ["Este", "es", "", "mensaje", "secreto"]
    }

    response = client.post(url,  json=jsonData)

    assert response.status_code == 200
    assert b"Error. La estructura de datos json no es valida" not in response.data
    assert b"Satelite cargado" in response.data
    
#Testteo de carga via POST skywalker
def test_topsecret_split_post_skywalker(client):

    url = "/app/v1/topsecret_split/skywalker"

    jsonData = {
        "distance": 100.0,
        "message": ["Este", "es", "un", "mensaje", "secreto"]
    }

    response = client.post(url,  json=jsonData)

    assert response.status_code == 200
    assert b"Error. La estructura de datos json no es valida" not in response.data
    assert b"Satelite cargado" in response.data

#Testteo de carga via POST sato
def test_topsecret_split_post_sato(client):

    url = "/app/v1/topsecret_split/sato"

    jsonData = {
        "distance": 100.0,
        "message": ["Este", "es", "un", "", "secreto"]
    }

    response = client.post(url,  json=jsonData)

    assert response.status_code == 200
    assert b"Error. La estructura de datos json no es valida" not in response.data
    assert b"Satelite cargado" in response.data

"""
def test_topsecret_split_get(client):

    url = "/app/v1/topsecret_split/"

    response = client.get(url)

    #assert response.status_code == 200
    assert b"Error. Uno de los mensajes esta vacio." not in response.data
    assert b"Satelite cargado" in response.data

"""

#Testeo función de verificacion de mensajes
def test_Verifica_datos():

    #Busco la configuracion de las coordenadas de los satelites
    with open('src/coordenadas_satelites.json') as f:
        config = json.load(f)

        x1 = config['coordenadas_kenobi'][0]
        y1 = config['coordenadas_kenobi'][1]
        x2 = config['coordenadas_skywalker'][0]
        y2 = config['coordenadas_skywalker'][1]
        x3 = config['coordenadas_sato'][0]
        y3 = config['coordenadas_sato'][1]

    #Inicializo con las coordenadas de los satelites
    satelites_full = satelites(x1, y1, x2, y2, x3, y3)

    jsonData = {'satellites': [
        {
            'name': 'kenobi',
            'distance': 14.0,
            'message': ['', '', 'Este', 'es', 'un', 'mensaje', 'secreto']
        },
        {
            'name': 'skywalker',
            'distance': 115.5,
            'message': ['', 'Este', 'es', 'un', '', 'secreto']
        },
        {
            'name': 'sato',
            'distance': 142.7,
            'message': ['', '', '', '', '', 'Este', '', 'un', 'mensaje', 'secreto']
        }

    ]
    }

    try:

        resultado = satelites_full.Verifica_datos(jsonData)

    except Exception as exc:
        assert False, f"'Verifica_datos()' genero una excepción {exc}"

    

    assert resultado == 1

#Testeo función GetMessage
mensajes = [
    (["", "", "Este", "es", "un", "mensaje", "secreto"]
    , ["", "Este", "es", "un", "", ""]
    , ["", "", "", "", "", "Este", "", "un", "mensaje", "secreto"]),
    (["", "", "Este", "es", "un", "mensaje", "secreto"]
    , ["", "Este", "es", "", "", ""]   
    , ["Este", "", "un", "mensaje", "secreto"])
   ]


@pytest.mark.parametrize("msg1, msg2, msg3", mensajes)
def test_GetMessage(msg1, msg2, msg3):
    #Inicializo con las coordenadas de los satelites
    satelites_full = satelites(10, 10, 20, 20, 30, 30)

    try:
        #Desifro mensaje
        mesnaje_secreto = satelites_full.GetMessage(msg1, msg2, msg3)

    except Exception as exc:
        assert False, f"'GetMessage()' genero una excepción {exc}"

    assert len(mesnaje_secreto) >= 1


#Testeo función GetLocation
distancias = [
    (14.0 , 125.1 , 200.5 , -212.88 , 964.38)
    ,(456.0 , 58.1 , 20.1 , -29.53 , 666.5)
    , (40.3, 59.5, 78.9, -201.6 , 996.48)
]


@pytest.mark.parametrize("d1, d2, d3, rX, rY", distancias)
def test_GetLocation(d1,d2,d3,rX,rY):

    #Inicializo con las coordenadas de los satelites
    satelites_full = satelites(-500, -100, 100, -100, 500, 100)

    try:
        #Calculo posición de la nave mediante trilateración
        x, y = satelites_full.GetLocation(d1, d2, d3)

    except Exception as exc:
        assert False, f"'GetMessage()' genero una excepción {exc}"

    assert round(x,2) == rX
    assert round(y,2) == rY
    

