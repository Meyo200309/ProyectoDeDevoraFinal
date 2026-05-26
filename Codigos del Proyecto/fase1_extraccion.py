import pandas as pd
from sqlalchemy import create_engine
from pymongo import MongoClient

# Esta clase es la que hace el verdadero trabajo de extraer los datos

class DataExtractor:

    def __init__(self, sql_conn_str, mongo_conn_str):

        # MYSQL

        self.sql_engine = create_engine(sql_conn_str)

        # MongoDB

        self.mongo_client = MongoClient(mongo_conn_str)

    # Aquí la extracción directa a MySQL

    def extraer_sql(self, table_name, last_id=0):

        query = f""" SELECT * FROM {table_name} WHERE id_transaccion > {last_id} """

        df = pd.read_sql(query, self.sql_engine)

        return df

    # Aquí la extracción estilo NoSQL (en Mongo)

    def extraer_mongo(self, db_name, collection_name):

        db = self.mongo_client[db_name]

        collection = db[collection_name]

        data = list(collection.find({}, {"_id": 0}))

        df = pd.DataFrame(data)

        return df

    # Lector del archivo CSV

    def extraer_csv(self, csv_path):

        df = pd.read_csv(csv_path)

        return df

    # Intento de API simulada (llorar a veces es bueno)
    
    def extract_api_scraping(self):

        return 17.50