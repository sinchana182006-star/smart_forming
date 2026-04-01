from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "8bec7150cc52ab5eafc832ddbfd6a5da"

@app.route("/", methods=["GET", "POST"])
def index():
    data = None

    if request.method == "POST":
        crop = request.form.get("crop")
        city = request.form.get("city")

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()

        if response.get("cod") != 200:
            data = {"error": "City not found or API issue. Try Bangalore"}
        else:
            temp = response["main"]["temp"]
            humidity = response["main"]["humidity"]

            # Improved logic
            if temp > 30 and humidity < 50:
                irrigation = "High water needed 💧 (Hot & Dry)"
            elif humidity > 70:
                irrigation = "Low water needed 🌧️ (High humidity)"
            else:
                irrigation = "Moderate water needed 🌱"

            data = {
                "crop": crop,
                "temp": temp,
                "humidity": humidity,
                "irrigation": irrigation
            }

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)