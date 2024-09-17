from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/avistamientos', methods=['GET'])
def avistamientos():
    region = request.args.get('region', 'CO-BOY')  # Default a Boyacá
    start = request.args.get('start', '')  # Fecha de inicio
    end = request.args.get('end', '')  # Fecha de fin
    url = f"https://api.ebird.org/v2/data/obs/{region}/recent"
    headers = {'X-eBirdApiToken': 'iktbj3fe2u9q'}
    params = {
        'back': 30,  # Ejemplo: últimos 30 días
        'maxResults': 200,  # Número máximo de resultados
        'startDate': start,
        'endDate': end
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True, port="5010")
