from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

url = "mongodb://localhost:27017"

try:
        cliente = MongoClient(url, serverSelectionTimeoutMS=2000)
        cliente.server_info()
        print("Conexión exitosa!!!")

        db = cliente["PPDProyectoDB"]
        coleccion = db["perfiles_usuarios"]
        doc = coleccion.find_one()

        if doc:
                print("\nDocumento encontrado:")
                print(doc)
        else:
                print("No se encontró documento.")
except ConnectionFailure:
        print("Error al conectar al Mongol.")
finally:
        cliente.close()
        print("Conexión terminada.")