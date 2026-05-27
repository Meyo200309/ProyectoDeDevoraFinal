import pandas as pd
from sqlalchemy import create_engine
from pymongo import MongoClient

# Esta clase es la que hace el verdadero trabajo de extraer los datos

class DataExtractor:

    def __init__(self, sql_conn, mongo_conn):

        # MYSQL

        self.sql_engine = create_engine(sql_conn)

        # MongoDB

        self.mongo_client = MongoClient(mongo_conn)

    # Aquí la extracción directa a MySQL

    def extraer_sql(self, nombre_tabla, ult_id=0):

        query = f""" SELECT * FROM {nombre_tabla} WHERE id_transaccion > {ult_id} """

        df = pd.read_sql(query, self.sql_engine)

        return df

    # Aquí la extracción estilo NoSQL (en Mongo)

    def extraer_mongo(self, nombre_db, nombre_coleccion):

        db = self.mongo_client[nombre_db]
        collection = db[nombre_coleccion]
        data = list(collection.find({}, {"_id": 0}))
        df = pd.DataFrame(data)

        return df

    # Lector del archivo CSV

    def extraer_csv(self, ruta_csv):

        df = pd.read_csv(ruta_csv, encoding='utf-8')

        return df

    # Intento de API simulada (llorar a veces es bueno)
    
    def extraer_api_scraping(self):

        return 17.50