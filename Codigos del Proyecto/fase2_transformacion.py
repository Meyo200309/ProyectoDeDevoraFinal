# Importar las librerías para el código de limpieza y transformación

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class DataTransformer: # <- Como la película

    @staticmethod
    def parsear_fecha(valor):

        formatos = [
            '%Y-%m-%d %H:%M:%S',   
            '%Y-%m-%d',            
            '%d/%m/%y',            
            '%d/%m/%Y',            
        ]
        for fmt in formatos:
            try:
                return pd.to_datetime(valor, format=fmt)
            except (ValueError, TypeError):
                continue
        return pd.NaT
    
    @staticmethod
    def rellenar_nulos(df):

        for col in df.columns:
            if df[col].isnull().sum() == 0:
                continue
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].fillna(pd.Timestamp('1000-01-01 00:00:00'))
            elif pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(0)
            elif pd.api.types.is_string_dtype(df[col]) or df[col].dtype == object:
                df[col] = df[col].fillna('Desconocido')
        return df

    # A iniciar la limpieza

    def limpiar_data(self, df_inventario, df_sql, df_mongo):

        # Comenzamos con MYSQL eliminando duplicados de transacciones

        df_sql = df_sql.drop_duplicates(subset=['id_transaccion'])

        # Ahora el inventario que está en el archivo CSV,
        # aquí se va a rellenar categorías nulas

        df_inventario = self.rellenar_nulos(df_inventario)
        
        # Y eliminar duplicados

        df_inventario = df_inventario.drop_duplicates()

        # Ahora le toca a Mongo, comenzando con normalizar el texto,
        # convertimos texto a minúsculas antes de mapear

        df_mongo['pais'] = df_mongo['geolocalizacion'].apply(lambda x: x.get('pais') if isinstance(x, dict) else None)

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

        df_mongo['pais'] = (df_mongo['pais'].astype(str).str.lower().str.strip().map(mapeo_paises).fillna('Desconocido'))

        return df_inventario, df_sql, df_mongo

    # Ahora toca l a normalización

    def normalizar_estandarizar(self, df_sql, df_mongo):

        # Normalizar las fechas, para que sea compatible con varios formatos de fecha

        df_sql['fecha'] = df_sql['fecha'].apply(self.parsear_fecha)

        nulos_fecha = df_sql['fecha'].isna().sum()
        print(f"Fechas sin parse: {nulos_fecha}") # <- Esto fue solo para testear si aparecían nulos al final

        # Hacer merge entre MySQL y MongoDB para formar un DataFrame con más datos

        df_master = pd.merge(df_sql, df_mongo, left_on='id_cliente', right_on='Customer_ID', how='right')
        df_master = self.rellenar_nulos(df_master)

        # Hacer segmentación de clientes

        condiciones = [
            (df_master['monto'] > 1000 ) & (df_master['edad'] < 30),
            (df_master['monto'] > 1000) & (df_master['edad'] >= 30),
            (df_master['monto'] <= 1000) & (df_master['edad'] < 30),
            (df_master['monto'] <= 1000) & (df_master['edad'] >= 30)
        ]

        segmentos = [
            'Premium Joven',
            'Premium Regular',
            'Estándar Joven',
            'Estándar Regular'
        ]

        df_master['segmento_cliente'] = np.select(condiciones, segmentos, default='Desconocido')

        # Escalado

        scaler = MinMaxScaler()
        columna_numerica = ['monto']
        df_master[['monto_escalado']] = scaler.fit_transform(df_master[columna_numerica])

        return df_master