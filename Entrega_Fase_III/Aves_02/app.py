import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = 'iktbj3fe2u9q'  # Sustituye 'tu_api_key' por tu propia API Key de Ebird
region_cundinamarca = 'CO-CUN'
region_boyaca = 'CO-BOY'

def obtener_datos_avistamientos(region_code, api_key):
    url = f'https://api.ebird.org/v2/data/obs/{region_code}/recent'
    headers = {'X-eBirdApiToken': api_key}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error al obtener los datos: {response.status_code}')
        return []

datos_cundinamarca = obtener_datos_avistamientos(region_cundinamarca, API_KEY)
datos_boyaca = obtener_datos_avistamientos(region_boyaca, API_KEY)

df_cundinamarca = pd.DataFrame(datos_cundinamarca)
df_boyaca = pd.DataFrame(datos_boyaca)

df_cundinamarca['region'] = 'Cundinamarca'
df_boyaca['region'] = 'Boyacá'

df_avistamientos = pd.concat([df_cundinamarca, df_boyaca])

def generar_analisis_con_numpy(df):
    if 'comName' in df.columns and 'howMany' in df.columns:
        # Agrupar por especie (comName) y sumar el número de avistamientos (howMany)
        avistamientos_por_especie = df.groupby('comName')['howMany'].sum()
    else:
        print("Las columnas 'comName' o 'howMany' no están disponibles. Verifica los nombres.")
        return pd.Series(), 0, 0

    total_avistamientos = avistamientos_por_especie.values
    media = np.mean(total_avistamientos)
    desviacion_estandar = np.std(total_avistamientos)

    return avistamientos_por_especie, media, desviacion_estandar

def generar_grafica_especies(avistamientos_por_especie):
    if avistamientos_por_especie.empty:
        print("No se pueden generar gráficos, no hay datos disponibles.")
        return None

    top_10_especies = avistamientos_por_especie.nlargest(10)

    fig, ax = plt.subplots(figsize=(10, 7))
    top_10_especies.plot(kind='bar', ax=ax)
    plt.title('Top 10 especies más avistadas', fontsize=14)
    plt.xlabel('Especie', fontsize=12)
    plt.ylabel('Número de avistamientos', fontsize=12)
    plt.xticks(rotation=60, ha='right', fontsize=10)  # Rotar las etiquetas en el eje X para mejor legibilidad

    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode('utf8')
    
    return graph_url

@app.route('/')
def index():
    region = request.args.get('region', 'Todas')
    
    if region == 'Cundinamarca':
        df_filtrado = df_avistamientos[df_avistamientos['region'] == 'Cundinamarca']
    elif region == 'Boyacá':
        df_filtrado = df_avistamientos[df_avistamientos['region'] == 'Boyacá']
    else:
        df_filtrado = df_avistamientos

    avistamientos_por_especie, media_avistamientos, desviacion_estandar = generar_analisis_con_numpy(df_filtrado)
    
    grafica_especies = generar_grafica_especies(avistamientos_por_especie)
    
    if not grafica_especies:
        return "<h1>No hay datos disponibles para mostrar.</h1>"

    return render_template('index.html', grafica_especies=grafica_especies, 
                           media_avistamientos=media_avistamientos, 
                           desviacion_estandar=desviacion_estandar,
                           region=region)

if __name__ == '__main__':
    app.run(debug=True, port=5020)
