import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class DataTransformer:
    "Clase encargada de la calidad, limpieza y normalización."

    def clean_data(self, df_inventario, df_sql, df_mongo):
        "Detecta nulos, elimina duplicados y estandariza strings."
        df_sql = df_sql.drop_duplicates(subset=['id_transaccion'])
        df_inventario['categoria'] = df_inventario['categoria'].fillna('Desconocido')
        df_inventario = df_inventario.drop_duplicates()
        mapeo_paises = {'mex': 'México', 'mx': 'México', 'usa': 'Estados Unidos'}
        df_mongo['geolocalizacion'] = df_mongo['geolocalizacion'].str.lower().map(mapeo_paises).fillna(df_mongo['geolocalizacion'])
        return df_inventario, df_sql, df_mongo

    def normalize_and_enrich(self, df_sql, df_mongo):
        "Normaliza fechas, escala numéricos y une fuentes."
        df_sql['fecha'] = pd.to_datetime(df_sql['fecha'], format='%d/%m/%y', errors='coerce')
        df_master = pd.merge(df_sql, df_mongo, left_on='id_cliente', right_on='Customer_ID', how='left')
        df_master['segmento_cliente'] = np.where(
            (df_master['monto'] > 1000) & (df_master['edad'] < 30), 
            'Premium Joven', 
            'Estándar'
        )
        scaler = MinMaxScaler()
        df_master[['monto_scaled', 'gasto_mensual_scaled']] = scaler.fit_transform(df_master[['monto', 'gasto_mensual']].fillna(0))
        return df_master
