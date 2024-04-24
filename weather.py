from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

def get_weather_forecast(location):
    api_key = "e60177137615288e49eaf8dec8a6d28a"
    if not api_key:
        return {"error": "OpenWeatherMap API key is missing."}

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric" 
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if response.status_code == 200:
            weather_forecast = {
                "location": data["name"],
                "description": data["weather"][0]["description"],
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
            }
            return weather_forecast
        else:
            return {"error": f"Failed to retrieve weather data: {data.get('message', 'Unknown error')}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

@app.route('/weather_forecast', methods=['GET'])
def weather_forecast():
    location = request.args.get('location')

    if not location:
        return jsonify({"error": "Location is required."}), 400

    weather_forecast = get_weather_forecast(location)
    if "error" in weather_forecast:
        return jsonify({"error": weather_forecast["error"]}), 500
    else:
        return jsonify(weather_forecast)

if __name__ == '__main__':
    app.run(debug=True)
