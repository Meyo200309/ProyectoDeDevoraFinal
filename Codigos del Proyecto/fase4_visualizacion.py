import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go


class DataVisualizer:

    "Generación del Dashboard estático y gráficos avanzados."

    # Generamos un dashboard para generar los gráficos de los datos

    def generar_dashboard(self, df):

        # Configuración principal

        plt.figure(figsize=(18, 6))

        # Aquí el Boxplot

        plt.subplot(1, 2, 1)

        sns.boxplot(x='segmento_cliente', y='monto', data=df, hue='segmento_cliente', palette='Set2', legend=False)
        plt.title('Distribución de Ventas por Segmento')
        plt.xlabel('Segmento Cliente')
        plt.ylabel('Monto de Venta')

        # El Scatter del PCA

        plt.subplot(1, 2, 2)
        sns.scatterplot(x='PCA_1', y='PCA_2', hue='segmento_cliente', data=df, palette='viridis')
        plt.title('Distribución de Clientes tras PCA')
        plt.xlabel('PCA 1')
        plt.ylabel('PCA 2')

        # Exportar para visualizar

        plt.tight_layout()
        plt.savefig('dashboard.png')
        plt.close()
        print("Dashboard exportado como dashboard.png")

    # Aquí el esperado diagrama de Sankey

    def plot_sankey(self, df):

        # Conteo de los segmentos antes registrados (o asignados, más bien)

        premium = (df['segmento_cliente'].eq('Premium Joven').sum())
        estandar = (df['segmento_cliente'].eq('Estándar').sum())

        total = len(df) # <--- Por si acaso lo utilizábamos, pero no hizo falta

        # Aquí el desarrollo del diagrama de Sankey

        fig = go.Figure(data=[go.Sankey(node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), 
                        label=["Clientes Totales", "Premium Joven", "Estándar"]),
                        link=dict(source=[0, 0], target=[1, 2], value=[premium, estandar]))])

        fig.update_layout(title_text=("Distribución de Segmentos de Clientes"), font_size=10)

        # Exportar el diagrama de Sankey en formato HTML

        fig.write_html("sankey_diagrama.html")

        print("Diagrama de Sankey exportado como sankey_diagrama.html")