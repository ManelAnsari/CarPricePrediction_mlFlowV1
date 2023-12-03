from flask import Flask, render_template, request, jsonify
import requests
import json
from fastapi import FastAPI, Request
from fastapi.middleware.wsgi import WSGIMiddleware

app = Flask(__name__, template_folder='client', static_folder='client')


fastapi = FastAPI()

API_URL = "http://127.0.0.1:8000"

fuels = ['Diesel', 'Petrol', 'CNG', 'LPG']
owners = ['Un', 'Deux', 'Trois et plus']

@app.route('/')
def index():
    return render_template('index.html', Pred = '0.00')  # Remplacez nom

@app.route('/prediction', methods=['POST'])
def predict():
    json_data = request.get_json()
    transmission = json_data.get('transmission', '')
    fuel = json_data.get('fuel', '')
    owner = json_data.get('owner', '')
    year = int(json_data.get('year', 0))
    km_driven = float(json_data.get('km_driven', 0))
    engine = float(json_data.get('engine', 0))
    max_power = float(json_data.get('max_power', 0))

    transmission = 2 if transmission == 'Manual' else  1

    owner = owners.index(owner)
    
    fuel = fuels.index(fuel)+1

    data = {
        "transmission": transmission,
        "fuel": fuel,
        "owner": owner,
        "year": year,
        "km_driven": km_driven,
        "engine": engine,
        "max_power": max_power
    }

    # Send data to the FastAPI endpoint
    response = requests.post(f"{API_URL}/predict", json=data)

    if response.status_code == 200:
        result = response.json()
        print(result)
        return jsonify({"Predict": result['Predict']})
    else:
        return jsonify({"error": "Unable to get a prediction"})
        
        


if __name__ == '__main__':
    fastapi.mount("/", WSGIMiddleware(app))
    app.run(debug=True, host='0.0.0.0', port=80)
