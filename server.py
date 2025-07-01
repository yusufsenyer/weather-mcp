from flask import Flask, request, jsonify

app = Flask(__name__)

# MCP JSON-RPC metodları
@app.route("/agent/weather", methods=["POST"])
def mcp_handler():
    data = request.get_json(force=True)
    method = data.get("method")
    id_ = data.get("id")

    if method == "tools/list":
        return jsonify({
            "jsonrpc": "2.0",
            "result": [{"name": "weather_tool", "description": "Get weather data"}],
            "id": id_
        })

    elif method == "resources/list":
        return jsonify({
            "jsonrpc": "2.0",
            "result": [],
            "id": id_
        })

    elif method == "prompts/list":
        return jsonify({
            "jsonrpc": "2.0",
            "result": [],
            "id": id_
        })

    elif method == "get_weather":
        params = data.get("params", {})
        city = params.get("city")
        if not city:
            return jsonify({"jsonrpc": "2.0", "error": {"code": -32602, "message": "City parameter required"}, "id": id_})
        weather = get_weather_data(city)
        return jsonify({"jsonrpc": "2.0", "result": weather, "id": id_})

    else:
        return jsonify({"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": id_})

def get_weather_data(city):
    import requests
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geo_res = requests.get(geo_url)
    geo_data = geo_res.json()
    if "results" not in geo_data or not geo_data["results"]:
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
