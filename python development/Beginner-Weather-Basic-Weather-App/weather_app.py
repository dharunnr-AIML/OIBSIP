import tkinter as tk
from tkinter import messagebox
import requests


def get_weather():
    city = city_entry.get().strip()

    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    try:
        # Find city coordinates
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=10
        )
        geo_data = geo_response.json()

        if "results" not in geo_data:
            messagebox.showerror(
                "Error",
                "City not found. Please check the city name."
            )
            return

        location = geo_data["results"][0]
        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location["name"]
        country = location.get("country", "")

        # Get current weather
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "apparent_temperature,"
                "wind_speed_10m"
            ),
            "temperature_unit": "celsius",
            "wind_speed_unit": "kmh"
        }

        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        )
        weather_data = weather_response.json()

        current = weather_data["current"]

        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        feels_like = current["apparent_temperature"]
        wind_speed = current["wind_speed_10m"]

        result_label.config(
            text=(
                f"📍 {city_name}, {country}\n\n"
                f"🌡 Temperature: {temperature} °C\n"
                f"🤗 Feels Like: {feels_like} °C\n"
                f"💧 Humidity: {humidity}%\n"
                f"💨 Wind Speed: {wind_speed} km/h"
            ),
            fg="black"
        )

    except requests.exceptions.RequestException:
        messagebox.showerror(
            "Error",
            "Network error. Please check your internet connection."
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Something went wrong:\n{e}"
        )


root = tk.Tk()
root.title("Basic Weather App")
root.geometry("500x450")
root.resizable(False, False)

title_label = tk.Label(
    root,
    text="Basic Weather App",
    font=("Arial", 22, "bold")
)
title_label.pack(pady=25)

city_label = tk.Label(
    root,
    text="Enter City Name",
    font=("Arial", 12)
)
city_label.pack()

city_entry = tk.Entry(
    root,
    width=30,
    font=("Arial", 12)
)
city_entry.pack(pady=10)

weather_button = tk.Button(
    root,
    text="Get Weather",
    command=get_weather,
    font=("Arial", 12, "bold")
)
weather_button.pack(pady=15)

result_label = tk.Label(
    root,
    text="",
    font=("Arial", 13),
    justify="left"
)
result_label.pack(pady=20)

root.mainloop()