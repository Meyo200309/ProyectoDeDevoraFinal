from fase1_extraccion import DataExtractor
from fase2_transformacion import DataTransformer
from fase3_analisis import DataAnalisis
from fase4_visualizacion import DataVisualizer
from pymongo import MongoClient
import pyarrow
import pymysql

if __name__ == "__main__":

    print("Iniciando el Pipeline ETL...")

    # Insertamos credenciales para inicializar la conexión a bases de datos antes de ->

    sql_conn = "mysql+pymysql://root:PASSWORD@localhost:3306/PPDProyectoDB"
    mongo_conn = "mongodb://localhost:27017/"
    cliente_mongo = MongoClient(mongo_conn)

    # Llamar a la clase extractor del otro archivo

    extractor = DataExtractor(sql_conn, mongo_conn)

    try:
        with extractor.sql_engine_connect() as conn:
            print("Conexión a MYSQL.")
    except Exception as e:
        print(f"Error MySQL: {e}")

    try: # Intento de que conecte a Mongo
        cliente_mongo.admin.command('ping')
        print("Conexión a mongo exitosa. Carita feliz.")
    except Exception as e:
        print(f"Error conectando a Mongo: {e}")

    # Primera fase: Extracción desde diversas fuentes

    # De MySQL

    df_ventas_hist = extractor.extraer_sql(table_name="ventas_historicas", last_id=0)

    # En MongoDB

    df_perf_usuarios = extractor.extraer_mongo(db_name="PPDProyectoDB",collection_name="perfiles_usuarios")

    # Desde CSV

    df_inv = extractor.extraer_csv("Inventario_Omnilife_ETL.csv")

    # Ahora con los datos extraídos, procedemos a la transformación

    transformer = DataTransformer() # Como la película, otra vez pfff

    df_inv_limpio, df_ventas_hist_limpio, df_perf_usuarios_limpio = (transformer.limpiar_data(df_inv, df_ventas_hist, df_perf_usuarios))

    df_master = transformer.normalizar_estandarizar(df_ventas_hist_limpio, df_perf_usuarios_limpio)

    # Sigue la fase de análisis donde se hace el PCA

    analyzer = DataAnalisis()
    df_master_pca = analyzer.apply_pca(df_master)

    # Aquí el proceso de visualización, donde veremos algunas gráficas en base a lo anteriora

    visualizer = DataVisualizer()
    visualizer.generar_dashboard(df_master_pca)
    visualizer.plot_sankey(df_master_pca)

    # Final, donde transformamos el DataFrame completo, junto con el PCA
    # para exportarlo a archivo tipo PARQUET y CSV (ya era hora)

    df_master_pca.to_parquet('data_master_clean.parquet', index=False)
    df_master_pca.to_csv('data_master_clean.csv', index=False)
    print("Pipeline completado exitosamente.")