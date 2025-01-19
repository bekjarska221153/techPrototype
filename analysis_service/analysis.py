import pandas as pd
import matplotlib.pyplot as plt
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator, StochasticOscillator, WilliamsRIndicator
from ta.trend import CCIIndicator

def load_data(file_path):
    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    data['High'] = data['Last Transaction Price'].rolling(window=5).max()
    data['Low'] = data['Last Transaction Price'].rolling(window=5).min()
    data['Last Transaction Price'] = pd.to_numeric(data['Last Transaction Price'], errors='coerce')
    data.dropna(subset=['Last Transaction Price'], inplace=True)
    return data

def calculate_indicators(data):
    data['SMA_20'] = SMAIndicator(data['Last Transaction Price'], window=20).sma_indicator()
    data['EMA_20'] = EMAIndicator(data['Last Transaction Price'], window=20).ema_indicator()
    data['RSI'] = RSIIndicator(data['Last Transaction Price'], window=14).rsi()
    data['Stochastic_%K'] = StochasticOscillator(data['High'], data['Low'], data['Last Transaction Price']).stoch()
    data['MACD'] = MACD(data['Last Transaction Price']).macd()
    data['Williams_%R'] = WilliamsRIndicator(data['High'], data['Low'], data['Last Transaction Price']).williams_r()
    return data

def filter_data(data, issuer, start_date, end_date):
    filtered_data = data[data['Issuer'] == issuer]
    return filtered_data[(filtered_data.index >= start_date) & (filtered_data.index <= end_date)]

def plot_graph(data, issuer):
    plt.figure(figsize=(14, 8))
    plt.plot(data.index, data['Last Transaction Price'], label=f'{issuer} Stock Price', color='blue')
    plt.title(f"Technical Analysis for {issuer}")
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    plt.savefig('static/graph.png')  # Save graph to file
