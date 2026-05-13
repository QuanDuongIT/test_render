from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

# cache đơn giản
weather_cache = {
    "data": None,
    "time": 0
}

CACHE_TIME = 300  # 5 phút


def get_weather():
    """Lấy thời tiết Hà Nội từ Open-Meteo"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 21.0285,   # Hà Nội
        "longitude": 105.8542,
        "current_weather": True
    }

    res = requests.get(url, params=params)
    data = res.json()

    return {
        "temperature": data["current_weather"]["temperature"],
        "windspeed": data["current_weather"]["windspeed"],
        "time": data["current_weather"]["time"]
    }


def get_cached_weather():
    """chỉ gọi API 1 lần trong 5 phút"""
    now = time.time()

    if weather_cache["data"] is None or now - weather_cache["time"] > CACHE_TIME:
        weather_cache["data"] = get_weather()
        weather_cache["time"] = now

    return weather_cache["data"]


# =========================
# WEB UI
# =========================
@app.route("/")
def home():
    weather = get_cached_weather()

    return f"""
    <h1>🌤 Weather App (Hà Nội)</h1>

    <p>🌡 Nhiệt độ: {weather['temperature']} °C</p>
    <p>💨 Gió: {weather['windspeed']} km/h</p>
    <p>⏰ Thời gian đo: {weather['time']}</p>

    <hr>
    <a href="/api/weather">API Weather JSON</a>
    """


# =========================
# API JSON
# =========================
@app.route("/api/weather")
def api_weather():
    weather = get_cached_weather()
    return jsonify(weather)


if __name__ == "__main__":
    app.run(debug=True)