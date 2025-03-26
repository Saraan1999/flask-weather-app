from flask import Flask, request, render_template_string
import requests

# ✅ Initialize Flask App
app = Flask(__name__)

# 🔴 Replace with your actual OpenWeather API key
API_KEY = "951b9e9a8a263e163d6bcfa90c094545"  
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error_message = ""

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            params = {"q": city, "appid": API_KEY, "units": "metric"}
            headers = {"User-Agent": "MyFlaskApp"}  # ✅ Prevents blocking
            response = requests.get(BASE_URL, params=params, headers=headers)

            if response.status_code == 200:
                weather_data = response.json()
            else:
                error_message = "City not found or API issue"

    # ✅ Simple HTML template (renders directly)
    html_template = """
    <html>
    <head>
        <title>Weather App</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 50px;
                background-color: #f0f8ff;
            }
            h1 {
                color: #333;
            }
            input, button {
                padding: 10px;
                margin: 5px;
                font-size: 16px;
            }
            .weather-container {
                margin-top: 20px;
                padding: 15px;
                border-radius: 10px;
                background: #fff;
                display: inline-block;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
        </style>
    </head>
    <body>
        <h1>Weather App</h1>
        <form method="POST">
            <input type="text" name="city" placeholder="Enter city name" required>
            <button type="submit">Get Weather</button>
        </form>

        {% if weather_data %}
        <div class="weather-container">
            <h2>Weather in {{ weather_data.name }}</h2>
            <p><strong>Temperature:</strong> {{ weather_data.main.temp }}°C</p>
            <p><strong>Humidity:</strong> {{ weather_data.main.humidity }}%</p>
            <p><strong>Condition:</strong> {{ weather_data.weather[0].description }}</p>
        </div>
        {% endif %}

        {% if error_message %}
        <p style="color:red;">{{ error_message }}</p>
        {% endif %}
    </body>
    </html>
    """

    return render_template_string(html_template, weather_data=weather_data, error_message=error_message)

# ✅ Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # 🔴 Use port 10000 for Render
