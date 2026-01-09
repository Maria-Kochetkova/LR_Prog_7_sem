import math
import multiprocessing
import xml.etree.ElementTree as ET
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_rates():
    """Сервис курсов валют: получает данные от ЦБ РФ и парсит XML."""
    url = "https://www.cbr-xml-daily.ru/daily.xml"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        rates = {"RUB": 1.0}  # Базовая валюта

        for valute in root.findall('Valute'):
            char_code = valute.find('CharCode').text

            nominal = float(valute.find('Nominal').text.replace(',', '.'))

            value = float(valute.find('Value').text.replace(',', '.'))

            rates[char_code] = value / nominal

        return rates
    except Exception as e:
        print(f"Ошибка получения курсов: {e}")
        return {"USD": 90.0, "EUR": 98.0, "RUB": 1.0}

@app.route('/')
def index():
    return jsonify({
        "status": "Microservices are running",
        "endpoints": ["/api/rates", "/api/convert", "/api/analytics"]
    })

@app.route('/api/rates', methods=['GET'])
def rates_service():
    return jsonify(get_rates())


@app.route('/api/convert', methods=['GET', 'POST'])
def convert_service():
    """Сервис конвертации."""
    if request.method == 'POST':
        data = request.get_json() or {}
    else:
        data = request.args

    try:
        amount = float(data.get('amount', 1))
        from_curr = data.get('from', 'USD').upper()
        to_curr = data.get('to', 'RUB').upper()

        rates = get_rates()

        res = (amount * rates[from_curr]) / rates[to_curr]

        return jsonify({
            "status": "success",
            "from": from_curr,
            "to": to_curr,
            "amount": amount,
            "result": round(res, 2)
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


def calculate_trend(x):
    """Тяжелые вычисления для сервиса аналитики."""
    return round(math.sin(x) * 100, 2)


@app.route('/api/analytics', methods=['GET'])
def analytics_service():
    """Сервис аналитики"""
    points = range(20)

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        chart_data = pool.map(calculate_trend, points)

    return jsonify({
        "currency_pair": "USD/RUB",
        "chart_points": chart_data,
        "processing": "multiprocessing_pool"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)