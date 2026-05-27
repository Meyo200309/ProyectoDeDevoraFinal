# Importar las librerías para el código de limpieza y transformación

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class DataTransformer: # <- Como la película

    # A iniciar la limpieza

    def limpiar_data(self, df_inventario, df_sql, df_mongo):

        # Comenzamos con MYSQL eliminando duplicados de transacciones

        df_sql = df_sql.drop_duplicates(subset=['id_transaccion'])

        # Ahora el inventario que está en el archivo CSV,
        # aquí se va a rellenar categorías nulas

        df_inventario['categoria'] = (df_inventario['categoria'].fillna('Desconocido'))

        # Y eliminar duplicados

        df_inventario = df_inventario.drop_duplicates()

        # Ahora le toca a Mongo, comenzando con normalizar el texto,
        # convertimos texto a minúsculas antes de mapear

        df_mongo['geolocalizacion'] = (df_mongo['geolocalizacion'].astype(str).str.lower())

        # Estandarización de países

        mapeo_paises = {
            'mex': 'México',
            'mx': 'México',
            'mexico': 'México',
            'méxico': 'México',
            'usa': 'Estados Unidos', # Agregando esto por si hay datos de geolocalización de Estados Unidos 
            'us': 'Estados Unidos'
        }

        # Por último se realiza el mapeo y se rellenan los nulos que podría haber

        df_mongo['pais'] = (df_mongo['geolocalizacion'].apply(lambda x: x.get('pais') if isinstance(x, dict) else None))
        df_mongo['pais'] = (df_mongo['pais']).astype(str).str.lower()
        df_mongo['pais'] = (df_mongo['pais'].map(mapeo_paises).fillna(df_mongo['pais']))

        return df_inventario, df_sql, df_mongo

    # Ahora toca l a normalización

    def normalizar_estandarizar(self, df_sql, df_mongo):

        # Normalizar las fechas, para que sea compatible con varios formatos de fecha

        df_sql['fecha'] = pd.to_datetime(df_sql['fecha'], errors='coerce', dayfirst=True)

        print(df_sql['fecha'].isna().sum())

        # Hacer merge entre MySQL y MongoDB para formar un DataFrame con más datos

        df_master = pd.merge(df_sql, df_mongo, left_on='id_cliente', right_on='Customer_ID', how='left')

        # Hacer segmentación de clientes

        df_master['segmento_cliente'] = np.where(
            (df_master['monto'] > 1000) &
            (df_master['edad'].fillna(0) < 30),

            'Premium Joven',
            'Estándar'
        )

        # Escalado

        scaler = MinMaxScaler()
        columna_numerica = ['monto']
        df_master[['monto_escalado']] = scaler.fit_transform(df_master[columna_numerica].fillna(0))

        return df_master