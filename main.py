import json
from flask import Flask
from flask import request
from satelites import satelites

app = Flask(__name__)

#Busco la configuracion de las coordenadas de los satelites
with open('coordenadas_satelites.json') as f:
    config = json.load(f)

    x1=config['coordenadas_kenobi'][0]
    y1=config['coordenadas_kenobi'][1]
    x2=config['coordenadas_skywalker'][0]
    y2=config['coordenadas_skywalker'][1]
    x3=config['coordenadas_sato'][0]
    y3=config['coordenadas_sato'][1]

#Inicializo con las coordenadas de los satelites
satelites_full = satelites(x1, y1, x2, y2, x3, y3)
satelites_split = satelites(x1, y1, x2, y2, x3, y3)



@app.route('/app/v1/topsecret/', methods=['POST'])
def topsecret():

    try:

        data = request.get_json()

        #Verifico datos, envio tipo de verificacion 1 para verificar datos cuando viene un POST con la carga de de los datos de los 3 satelites
        satelites_full.Verifica_datos(data)
  
        #Seteo los datos de los 3 satelites (distancia, mensaje)
        satelites_full.set_kenobi(data['satellites'][0]['distance'], data['satellites'][0]['message'])
        satelites_full.set_skywalker(data['satellites'][1]['distance'], data['satellites'][1]['message'])
        satelites_full.set_sato(data['satellites'][2]['distance'], data['satellites'][2]['message'])

        #Desifro mensaje
        mesnaje_secreto = satelites_full.GetMessage(satelites_full.get_kenobi_mensaje( ), satelites_full.get_skywalker_mensaje(), satelites_full.get_sato_mensaje())

        #Calculo posición de la nave mediante trilateración
        x, y = satelites_full.GetLocation(satelites_full.get_kenobi_distacia(), satelites_full.get_skywalker_distacia(), satelites_full.get_sato_distacia())

        #Creo Json de respuesta
        respuesta = {'position': {'x':  "{:.1f}".format(x), 'y': "{:.1f}".format(y)}, 'message': mesnaje_secreto}

        response = app.response_class(
            response=json.dumps(respuesta),
            status=200,
            mimetype='application/json'
        )
       
    except ValueError as e:
        respuesta = {'error': str(e)}
        response = app.response_class(response=json.dumps( respuesta), status=400, mimetype='application/json')
         
    return response
 

@app.route('/app/v1/topsecret_split/<string:satellite_name>', methods=['POST', 'GET'])
def topsecret_split(satellite_name):
 
    if request.method == 'POST':

  
        try:

            data = request.get_json()

            #Verrifico datos, envio tipo de verificacion 2 para verificar datos cuando viene un POST con la carga de datos de 1 satelite
            satelites_split.Verifica_datos( data)

            distancia = data['distance']
            mensaje = data['message']


            #Seteo datos de los satelites
            if satellite_name == 'kenobi':
                satelites_split.set_kenobi(distancia, mensaje)

            if satellite_name == 'skywalker':
                satelites_split.set_skywalker(distancia, mensaje)

            if satellite_name == 'sato':
                satelites_split.set_sato(distancia, mensaje)

            response = app.response_class(status=200)

        except ValueError as e:
            respuesta = {'error': str(e)}
            response = app.response_class(response=json.dumps(respuesta), status=400, mimetype='application/json')

        return response
    
    #Recibe GET
    if request.method == 'GET':

        try:

            #Desifro mensaje
            mesnaje_secreto = satelites_full.GetMessage(satelites_split.get_kenobi_mensaje(), satelites_split.get_skywalker_mensaje(), satelites_split.get_sato_mensaje())

            #Calculo posición de la nave mediante trilateración
            x, y = satelites_split.GetLocation(satelites_split.get_kenobi_distacia(), satelites_split.get_skywalker_distacia(), satelites_split.get_sato_distacia())

            #Creo Json de respuesta
            respuesta = {'position': {'x':  "{:.1f}".format(x), 'y': "{:.1f}".format(y)}, 'message': mesnaje_secreto}

            response = app.response_class(
                response=json.dumps(respuesta),
                status=200,
                mimetype='application/json'
            )

        except ValueError as e:
            respuesta = {'error': str(e)}
            response = app.response_class(response=json.dumps(respuesta), status=400, mimetype='application/json')

        return response

    
    
if __name__ == '__main__':
    app.run(debug=True, port=8080)
