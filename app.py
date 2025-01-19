from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

app = Flask(__name__)
def load_data_from_csv(file_path):
    df = pd.read_csv(file_path)
    # Претворање на DataFrame во список од речници
    data = df.to_dict(orient='records')
    return data
csv_file_path = 'all_issuers_data_last_10_years.csv'

all_issuers_data_last_10_years = load_data_from_csv(csv_file_path)

# Рута за прикажување на главната страница
@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    if request.method == 'POST':
        # Get the search inputs
        code = request.form.get('code', '').strip()
        date_from = request.form.get('date_from', '')
        date_to = request.form.get('date_to', '')

        # Load the CSV file
        df = pd.read_csv('technical_analysis_results.csv')

        # Filter by code if provided
        if code:
            df = df[df['Issuer Code'].str.contains(code, case=False, na=False)]

        # Filter by date range if provided
        if date_from:
            df = df[df['Date'] >= date_from]
        if date_to:
            df = df[df['Date'] <= date_to]

        data = df.to_dict(orient='records')

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

import requests

@app.route('/api/load_data', methods=['POST'])
def load_data_from_service():
    file_path = request.json.get('file_path')
    response = requests.post('http://localhost:5001/load_data', json={'file_path': file_path})
    return response.json()

@app.route('/api/calculate_indicators', methods=['POST'])
def calculate_indicators_from_service():
    file_path = request.json.get('file_path')
    response = requests.post('http://localhost:5001/calculate_indicators', json={'file_path': file_path})
    return response.json()

@app.route('/api/plot_graph', methods=['POST'])
def plot_graph_from_service():
    file_path = request.json.get('file_path')
    issuer = request.json.get('issuer')
    response = requests.post('http://localhost:5001/plot_graph', json={'file_path': file_path, 'issuer': issuer})
    return response.content  # Return the image or handle it as needed


if __name__ == '__main__':
    app.run(debug=True)
