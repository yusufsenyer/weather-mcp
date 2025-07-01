from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_weather_data(city: str) -> dict:
    try:
        # 1. Şehri koordinata çevir
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_res = requests.get(geo_url, timeout=5)
        geo_res.raise_for_status()
        geo_data = geo_res.json()

        if "results" not in geo_data or len(geo_data["results"]) == 0:
            return {"error": "Şehir bulunamadı"}

        latitude = geo_data["results"][0]["latitude"]
        longitude = geo_data["results"][0]["longitude"]

        # 2. Hava durumu verisini al
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}&longitude={longitude}&current_weather=true"
        )
        weather_res = requests.get(weather_url, timeout=5)
        weather_res.raise_for_status()
        weather_data = weather_res.json()

        if "current_weather" not in weather_data:
            return {"error": "Hava durumu verisi alınamadı"}

        current = weather_data["current_weather"]

        # Open-Meteo kodlarını açıklamak istersen harici bir map ekleyebilirsin
        description = f"Hız: {current['windspeed']} km/h, Kod: {current['weathercode']}"

        return {
            "city": city,
            "temperature": current["temperature"],
            "feels_like": current["temperature"],  # Open-Meteo 'feels like' vermiyor, sıcaklık olarak kullanıyoruz
            "description": description,
        }
    except requests.exceptions.RequestException as e:
        return {"error": "Dış API isteği başarısız: " + str(e)}
    except Exception as e:
        return {"error": "Sunucu hatası: " + str(e)}


@app.route("/agent/weather", methods=["POST"])
def agent_weather():
    if not request.is_json:
        return jsonify({"error": "İstek JSON formatında olmalı"}), 400

    data = request.get_json()
    city = data.get("city")

    if not city or not isinstance(city, str):
        return jsonify({"error": "Geçerli bir şehir adı girin"}), 400

    result = get_weather_data(city.strip())
    if "error" in result:
        return jsonify(result), 400

    return jsonify(result)


if __name__ == "__main__":
    # Host 0.0.0.0 yaparak dış bağlantılara açıyoruz
    app.run(debug=True, host="0.0.0.0", port=5000)
