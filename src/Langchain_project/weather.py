import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_current_weather():
    city = input("Enter city name: ").strip()
    if not API_KEY:
        print("Missing API_KEY in .env")
        return
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    resp = requests.get(BASE_URL, params=params, timeout=10)
    data = resp.json()
    print(data)


if __name__ == "__main__":
    get_current_weather()
