import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


class DataAnalisis:

    def apply_pca(self, df):

        columnas_pca = [

            'monto',
            'edad',
            'gasto_mensual',
            'monto_escalado',
            'gasto_mensual_escalado'

        ]

        # Esto solo para validar si las columnas del PCA realmente existen

        columnas_existentes = [
            col for col in columnas_pca
            if col in df.columns
        ]

        comportamiento = (df[columnas_existentes].fillna(0))

        # Aquí el estandarizado

        scaler = StandardScaler()

        comportamiento_escalado = scaler.fit_transform(comportamiento)

        # Formar el PCA

        pca = PCA(n_components=3)

        n_componentes = pca.fit_transform(comportamiento_escalado)

        # Componentes principales

        df['PCA_1'] = n_componentes[:, 0]
        df['PCA_2'] = n_componentes[:, 1]
        df['PCA_3'] = n_componentes[:, 2]

        # Varianza explicada

        varianza = sum(pca.explained_variance_ratio_)

        print(f"Varianza explicada por PCA: {varianza:.2%}")

        return df