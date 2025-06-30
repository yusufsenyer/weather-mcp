from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

def get_weather_data(city):
    # Örnek sabit veri döndürüyoruz, gerçek API’ye bağlanabilirsin
    return {
        "city": city,
        "temperature": 26,
        "feels_like": 27,
        "description": "Parçalı bulutlu"
    }

@app.route("/weather", methods=["GET"])
def weather_get():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "Lütfen 'city' parametresi gönderin."}), 400
    data = get_weather_data(city)
    return jsonify(data)

@app.route("/agent/weather", methods=["POST"])
def weather_post():
    content = request.json
    city = content.get("city", "")
    if not city:
        return jsonify({"error": "city bilgisi eksik"}), 400
    data = get_weather_data(city)
    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
