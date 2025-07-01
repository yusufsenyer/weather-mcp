from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/agent/weather", methods=["POST"])
def mcp_handler():
    data = request.get_json(force=True)
    method = data.get("method")
    id_ = data.get("id")

    if method == "tools/list":
        return jsonify({"jsonrpc": "2.0", "result": [{"name": "weather_tool", "description": "Get weather data"}], "id": id_})
    elif method == "resources/list":
        return jsonify({"jsonrpc": "2.0", "result": [], "id": id_})
    elif method == "prompts/list":
        return jsonify({"jsonrpc": "2.0", "result": [], "id": id_})
    elif method == "get_weather":
        # Burada dış API çağrısı yok, sabit veri dönüyoruz
        dummy_response = {
            "city": "TestCity",
            "temperature": 22,
            "feels_like": 21,
            "description": "Clear sky"
        }
        return jsonify({"jsonrpc": "2.0", "result": dummy_response, "id": id_})
    else:
        return jsonify({"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": id_})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
