
class satelites:
    
    def __init__(self, sat_1_x, sat_1_y,sat_2_x, sat_2_y, sat_3_x, sat_3_y ): 
        self.__sat_1_x = sat_1_x
        self.__sat_1_y = sat_1_y
        self.__sat_2_x = sat_2_x
        self.__sat_2_y = sat_2_y
        self.__sat_3_x = sat_3_x
        self.__sat_3_y = sat_3_y

        #Discancias del emisor a cada satelite
        self.__distacia_kenobi = 0
        self.__distacia_skywalker = 0
        self.__distacia_sato = 0

        #Mensajes de los satelites
        self.__mensaje_kenobi = ''
        self.__mensaje_skywalker = ''
        self.__mensaje_sato = ''


    #Setters
    def set_kenobi(self,distacia, mensaje):
        self.__distacia_kenobi = distacia
        self.__mensaje_kenobi = mensaje
    
    def set_skywalker(self,distacia, mensaje):
        self.__distacia_skywalker = distacia
        self.__mensaje_skywalker = mensaje

    def set_sato(self,distacia, mensaje):
        self.__distacia_sato = distacia
        self.__mensaje_sato = mensaje

    #getters
    def get_kenobi_distacia(self):
        return self.__distacia_kenobi

    def get_skywalker_distacia(self):
        return self.__distacia_skywalker
    
    def get_sato_distacia(self):
        return self.__distacia_sato

    def get_kenobi_mensaje(self):
        return self.__mensaje_kenobi
    
    def get_skywalker_mensaje(self):
        return self.__mensaje_skywalker

    def get_sato_mensaje(self):
        return self.__mensaje_sato  

    #Función que aplica fórmulas de trilateración para devolver el punto de intersección (x,y) de tres círculos
    def GetLocation(self,r1,r2,r3):

        try:
            #verifico distancias
            if r1 == 0 or r2 == 0 or r3 == 0:
                raise ValueError('Falta determinar una distancia.')

            x1 = self.__sat_1_x
            y1 = self.__sat_1_y
            x2 = self.__sat_2_x
            y2 = self.__sat_2_y
            x3 = self.__sat_3_x
            y3 = self.__sat_3_y

            A = 2*x2 - 2*x1
            B = 2*y2 - 2*y1
            C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
            D = 2*x3 - 2*x2
            E = 2*y3 - 2*y2
            F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2
            x = (C*E - F*B) / (E*A - B*D)
            y = (C*D - A*F) / (B*D - A*E)
        except Exception as exc:
            raise ValueError('Error. No se pudo determinar la posición. (' + str(exc) + ")")

        return x, y

    #Funcion que decifra el mensaje, como argumentos de entrada recibe un arreglo string de cada satelite y devuelve el mensaje decifrado si es posible
    def GetMessage(self,msg1,msg2,msg3):

        #Verifico si tengo mensajes para procesar.
        if len(msg1) == 0 or len(msg2) == 0 or len(msg3) == 0:
            raise ValueError('Error. Uno de los mensajes esta vacio. - No hay suficiente información para descifrar el mensaje')

        cant_elementos_maxima = 0
        mensaje_secreto = [""]
        mensaje_secreto_str = ""

        #Obtengo el tamano de la lista de mayor cantidad de elementos
        cant_elementos_maxima = max({len(msg1), len(msg2), len(msg3)})

        #Igualo las dimensiones de las lsitas de mensajes a la dimensión cant_elementos_maxima (igualo desplazamientos)
        for i in range(cant_elementos_maxima - len(msg1)):
            msg1.insert(0, '')

        for i in range(cant_elementos_maxima - len(msg2)):
            msg2.insert(0, '')

        for i in range(cant_elementos_maxima - len(msg3)):
            msg3.insert(0, '')

        #Invierto los mensajes
        msg1.reverse()
        msg2.reverse()
        msg3.reverse()

        #Completo el mensajes recorriendo los elementos de las 3 listas de mensajes, completando con al posisiones que tengan valor
        for i in range(cant_elementos_maxima):
            if len(str(msg1[i])) > 0:
                mensaje_secreto.append(str(msg1[i]).encode('utf-8'))
            elif len(str(msg2[i])) > 0:
                mensaje_secreto.append(str(msg2[i]).encode('utf-8'))
            elif len(str(msg3[i])) > 0:
                mensaje_secreto.append(str(msg3[i]).encode('utf-8'))
            else:
                # Si no hay dato para la posición (i) en ninguno de las 3 listas,
                # verifico si el en resto de la posicoines hay valores para recuperar
                # de ser asi no sera posible descifrar el mensaje el mensaje; si no hay mas valores lo tomo como final de mensaje
                for x in range(i, cant_elementos_maxima):
                    if len(str(msg1[x])) > 0:
                        raise ValueError("El mensaje no puede ser descifrado")
                    elif len(str(msg2[x])) > 0:
                        raise ValueError("El mensaje no puede ser descifrado")
                    elif len(str(msg3[x])) > 0:
                        raise ValueError("El mensaje no puede ser descifrado")

                break

        mensaje_secreto.reverse()

        # Remuevo espacios en blanco
        mensaje_secreto = [i for i in mensaje_secreto if i]

        #Convierto la lista en un string
        mensaje_secreto = b' '.join(mensaje_secreto).decode('utf-8')
        mensaje_secreto_str = str(mensaje_secreto)

        return mensaje_secreto_str

    #Funcion de verificaion de datos y estructura JSON
    def Verifica_datos(self, data):
        try:
            #Determino si la estructura de datos tiene el nodo satellites, de no ser asi lo verifico como json de entrada de la ruta split
            if 'satellites' in str(data):

                distacia_kenobi = data['satellites'][0]['distance']
                distacia_skywalker = data['satellites'][1]['distance']
                distacia_sato = data['satellites'][2]['distance']

                mensaje_kenobi = data['satellites'][0]['message']
                mensaje_skywalker = data['satellites'][1]['message']
                mensaje_sato = data['satellites'][2]['message']

                #Verifico datos
                if type(distacia_kenobi) != float or type(distacia_skywalker) != float or type(distacia_sato) != float:
                    raise ValueError('El valor de distancia debe ser un float')

                if len(mensaje_kenobi) == 0 or len(mensaje_skywalker) == 0 or len(mensaje_sato) == 0:
                    raise ValueError( 'Uno de los mensaje de lo satelites estan vacio.')
            
            else:
    
                distancia = data['distance']
                mensaje = data['message']
                
                #Verifico datos
                if type(distancia) != float:
                    raise ValueError('El valor de distancia debe ser un float')

                if len(mensaje) == 0:
                    raise ValueError('Uno de los mensaje de lo satelites estan vacio.')
        except:
            raise ValueError('Error. La estructura de datos json no es valida')

        return 1