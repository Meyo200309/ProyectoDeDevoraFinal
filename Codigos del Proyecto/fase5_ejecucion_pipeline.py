from fase1_extraccion import DataExtractor
from fase2_transformacion import DataTransformer
from fase3_analisis import DataAnalyzer
from fase4_visualizacion import DataVisualizer
import pyarrow

if __name__ == "__main__": # Función principal para incializar el Pipeline (por fin)
    print("Iniciando el Pipeline ETL...")
    extractor = DataExtractor("sqlite:///:memory:", "mongodb://localhost:27017/")
    
    # FASE 1: Extracción
    df_sql = extractor.extract_sql_incremental()
    df_mongo = extractor.extract_nosql()
    df_inv = extractor.extract_csv()
    
    # FASE 2: Transformación
    transformer = DataTransformer()
    df_inv_clean, df_sql_clean, df_mongo_clean = transformer.clean_data(df_inv, df_sql, df_mongo)
    df_master = transformer.normalize_and_enrich(df_sql_clean, df_mongo_clean)
    
    # FASE 3: Análisis
    analyzer = DataAnalyzer()
    df_master_pca = analyzer.apply_pca(df_master)
    
    # FASE 4: Visualización
    visualizer = DataVisualizer()
    visualizer.generate_dashboard(df_master_pca)
    visualizer.plot_sankey()
    
    # SALIDA
    df_master_pca.to_parquet('data_master_clean.parquet', index=False)
    print("Pipeline completado. Archivo data_master_clean.parquet generado exitosamente.")