from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def obtener_clima(region):
    # URL con parámetro de idioma establecido a español
    url = f'https://wttr.in/{region}?format=%l:+%C+%t+%c&lang=es'
    respuesta = requests.get(url)
    return respuesta.text

@app.route('/', methods=['GET', 'POST'])
def clima():
    clima_cundinamarca = obtener_clima('Cundinamarca')
    clima_boyaca = obtener_clima('Boyaca')
    clima_ciudad = ""
    ciudad = ""

    if request.method == 'POST':
        ciudad = request.form.get('ciudad')
        if ciudad:
            clima_ciudad = obtener_clima(ciudad)

    return render_template('index.html', clima_cundinamarca=clima_cundinamarca, 
                           clima_boyaca=clima_boyaca, clima_ciudad=clima_ciudad, ciudad=ciudad)

if __name__ == '__main__':
    app.run(debug=True)
