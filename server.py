from flask import Flask, request, jsonify

app = Flask(__name__)

# MCP için JSON-RPC metodu simülasyonu
@app.route("/agent/weather", methods=["POST"])
def agent_weather():
    data = request.get_json(force=True)
    # JSON-RPC yapısında "method" ve "params" beklenir
    method = data.get("method")
    params = data.get("params", {})

    if method == "get_weather":
        city = params.get("city")
        if not city:
            return jsonify(error="City parameter is required", id=data.get("id")), 400

        # Basit Open-Meteo API çağrısı
        weather = get_weather_data(city)
        response = {
            "jsonrpc": "2.0",
            "result": weather,
            "id": data.get("id")
        }
        return jsonify(response)
    else:
        return jsonify(error="Method not found", id=data.get("id")), 404

def get_weather_data(city):
    import requests
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geo_res = requests.get(geo_url)
    geo_data = geo_res.json()

    if "results" not in geo_data or len(geo_data["results"]) == 0:
        return {"error": "City not found"}

    latitude = geo_data["results"][0]["latitude"]
    longitude = geo_data["results"][0]["longitude"]

    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    weather_res = requests.get(weather_url)
    weather_data = weather_res.json()

    if "current_weather" not in weather_data:
        return {"error": "Weather data not found"}

    current = weather_data["current_weather"]

    return {
        "city": city,
        "temperature": current["temperature"],
        "feels_like": current["temperature"],
        "description": f"Wind speed {current['windspeed']} km/h, weather code {current['weathercode']}"
    }

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
