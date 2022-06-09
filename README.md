API rest - Operación Fuego de Quasar

## Pasos para ejecución 

### 1 - Instalar Vitrual ENV
pip install virtualenv

### 2- Crear entonro env 
python -m venv env

### 3 - Acvtivar entorno env (windows)
./venv/Script/activate

### 4 - Acvtivar entorno env (mac)
./venv/bin/activate

### 5 - Instalar dependencias
pip install -r requirements.txt

### 6 - Ejecución
python.exe main.py

### 7- Test Unitarios
pytest tests/test.py -v

*** Api accesible a travez de  http://127.0.0.1:8080 ***

## Swagger 
URL http://127.0.0.1:8080/apidocs/


## Seteos

En el archivo coordenadas_satelites.json se encuentra el seteo de las coordenadsas de los satelites.

## Directorios

./
└── ***requirements.txt*** (Archivo con lista de dependencias del proyecto)

./src/
├──***main.py*** (Archivos principal del proyecto, API endpoint)
├── ***satelites.py*** (Archivo clase satelites con funciones y logistica)
└── ***coordenadas_satelites.jso*** (Archivo con configuracion de los satelites)

./tests/
├── ***conftest.py*** (Configuracion Pytest)
└── ***test.py*** (Test unitario)

./swagger_doc/
├──  ***satelites_split_get.yml** (Archivo Swagger)
├──  ***satelites_split.yml*** (ArchivoSwagger)
└──  ***satelites.yml*** (Archivo Swagger)

./Documentos
├──  ***Ejercicio Fuego de Quasar - GO.pdf*** (Documento con información del desafio)
└──  ***Analisis.txt*** -(Documento con el analisis del proyecto.)

./env/
└── (Entorno virtual)
