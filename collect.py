import requests
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# ---------------------------
# LOAD ENV
# ---------------------------
load_dotenv()
MONGO_URI = os.getenv("mongodb+srv://sidrakiran1117_db_user:Test1234@cluster0.gxbcmuj.mongodb.net/aqi_db?retryWrites=true&w=majority")

client = MongoClient("mongodb+srv://sidrakiran1117_db_user:Test1234@cluster0.gxbcmuj.mongodb.net/aqi_db?retryWrites=true&w=majority")
db = client["aqi_db"]
collection = db["aqi_data"]

# ---------------------------
# CONFIG
# ---------------------------
API_KEY = "ff8f5c3fc65958ddd9b50e7149bfc1ad"

CITIES = {
    "Islamabad": (33.6844, 73.0479),
    "Rawalpindi": (33.5651, 73.0169)
}

# ---------------------------
# FETCH FUNCTION
# ---------------------------
def fetch_data(city, lat, lon):
    try:
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
        aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"

        weather = requests.get(weather_url).json()
        aqi = requests.get(aqi_url).json()

        record = {
            "timestamp": datetime.utcnow(),
            "city": city,
            "temp": weather["main"]["temp"],
            "humidity": weather["main"]["humidity"],
            "wind_speed": weather["wind"]["speed"],
            "aqi": aqi["list"][0]["main"]["aqi"],
            "pm2_5": aqi["list"][0]["components"]["pm2_5"]
        }

        return record

    except Exception as e:
        print(f"Error fetching {city}:", e)
        return None


# ---------------------------
# STORE IN MONGODB
# ---------------------------
def collect_data():
    print("Collecting data...")

    for city, (lat, lon) in CITIES.items():
        data = fetch_data(city, lat, lon)

        if data:
            collection.insert_one(data)
            print(f"✅ Stored {city} data")
        else:
            print(f"❌ Failed {city}")


# ---------------------------
# RUN
# ---------------------------
if __name__ == "__main__":
    collect_data()