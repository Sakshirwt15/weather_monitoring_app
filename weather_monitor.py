import requests
import sqlite3
import time
from datetime import datetime, timedelta
import schedule

API_KEY = '8d830cbac892f8198e1a4b6ccc8e0f5e'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
DB_PATH = 'db/weather_data.db'
THRESHOLD_TEMP = 35  # User-defined temperature threshold for alerts (Celsius)
CONSECUTIVE_ALERTS = 2  # Trigger alert if temp exceeds threshold for 2 consecutive updates

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

# Create a connection to the database and table
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        DROP TABLE IF EXISTS weather  -- Drop the table if it exists, so we can recreate it
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temp REAL,
            condition TEXT,  -- Make sure this column is added
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()


def store_weather_data(city, temp, condition):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Convert datetime to string before storing
    weather_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        INSERT INTO weather (city, temp, condition, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (city, temp, condition, weather_time))
    
    conn.commit()
    conn.close()
    print(f"Weather data stored successfully for {city}.")

# Fetch weather data from OpenWeatherMap API
def fetch_weather_data():
    for city in CITIES:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
        response = requests.get(url).json()
        
        city_name = response['name']
        temp_kelvin = response['main']['temp']
        temp_celsius = kelvin_to_celsius(temp_kelvin)
        weather_condition = response['weather'][0]['main']
        
        print(f"City: {city_name}, Temp: {temp_celsius}°C, Condition: {weather_condition}, Time: {datetime.now()}")

        store_weather_data(city_name, temp_celsius, weather_condition)

# Aggregates and Rollups for Daily Summary
def daily_weather_summary():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT city, AVG(temp), MAX(temp), MIN(temp), COUNT(*) as frequency, condition
        FROM weather
        WHERE timestamp >= date('now', '-1 day') 
        GROUP BY city, condition
        ORDER BY frequency DESC
    ''')
    
    result = cursor.fetchall()
    for row in result:
        print(f"Daily Summary for {row[0]}: Avg Temp: {row[1]}°C, Max Temp: {row[2]}°C, Min Temp: {row[3]}°C, Dominant Condition: {row[5]}")
    
    conn.close()

# Alerts for Threshold Breaches
def check_temperature_alerts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for city in CITIES:
        cursor.execute('''
            SELECT temp, timestamp FROM weather
            WHERE city = ? ORDER BY timestamp DESC LIMIT ?
        ''', (city, CONSECUTIVE_ALERTS))
        
        temps = cursor.fetchall()
        if len(temps) == CONSECUTIVE_ALERTS and all(temp[0] > THRESHOLD_TEMP for temp in temps):
            print(f"ALERT: {city} has exceeded {THRESHOLD_TEMP}°C for the last {CONSECUTIVE_ALERTS} updates!")
    
    conn.close()

# Schedule the weather fetch and summary functions
def start_weather_monitoring():
    schedule.every(15).seconds.do(fetch_weather_data)
    schedule.every().day.at("23:59").do(daily_weather_summary)
    schedule.every(5).minutes.do(check_temperature_alerts)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    init_db()
    print("Weather monitoring started...")
    start_weather_monitoring()
