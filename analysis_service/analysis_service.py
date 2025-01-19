from flask import Flask, request, jsonify, send_file
from analysis import load_data, calculate_indicators, filter_data, plot_graph
import os

app = Flask(__name__)


@app.route('/load_data', methods=['POST'])
def load_data_api():
    file_path = request.json.get('file_path')
    data = load_data(file_path)
    return jsonify({'message': 'Data loaded successfully', 'data_head': data.head().to_dict()})


@app.route('/calculate_indicators', methods=['POST'])
def calculate_indicators_api():
    file_path = request.json.get('file_path')
    data = load_data(file_path)
    data_with_indicators = calculate_indicators(data)
    return jsonify(
        {'message': 'Indicators calculated successfully', 'indicators_head': data_with_indicators.head().to_dict()})


@app.route('/filter_data', methods=['POST'])
def filter_data_api():
    file_path = request.json.get('file_path')
    issuer = request.json.get('issuer')
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')

    data = load_data(file_path)
    filtered = filter_data(data, issuer, start_date, end_date)
    return jsonify({'message': 'Data filtered successfully', 'filtered_data': filtered.to_dict()})


@app.route('/plot_graph', methods=['POST'])
def plot_graph_api():
    file_path = request.json.get('file_path')
    issuer = request.json.get('issuer')

    data = load_data(file_path)
    data_with_indicators = calculate_indicators(data)
    plot_graph(data_with_indicators, issuer)

    # Return the graph file as a response
    graph_path = os.path.join('static', 'graph.png')
    return send_file(graph_path, mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
