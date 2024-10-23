import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

DB_PATH = 'db/weather_data.db'

# Fetch data from the database
def fetch_latest_weather_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT city, temp, condition, timestamp FROM weather
        ORDER BY timestamp DESC LIMIT 6
    ''')
    
    data = cursor.fetchall()
    conn.close()
    return data

def display_weather_data():
    # Fetch weather data from database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT city, temp, condition, timestamp FROM weather ORDER BY timestamp DESC LIMIT 1')
    weather_data = cursor.fetchone()
    
    if weather_data:
        city, temp, condition, timestamp = weather_data
        
        # Remove fractional seconds (if any) from the timestamp
        timestamp = timestamp.split('.')[0]
        
        # Convert timestamp string to datetime object
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        
        # Display weather data
        weather_info = f"City: {city}, Temp: {temp}°C, Condition: {condition}, Time: {timestamp}"
        print(weather_info)
    
    conn.close()
    
def show_alerts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT city, temp FROM weather
        WHERE temp > 35
    ''')
    
    alerts = cursor.fetchall()
    conn.close()

    alert_text.delete(1.0, tk.END)  # Clear previous output
    if alerts:
        for city, temp in alerts:
            alert_text.insert(tk.END, f"ALERT: {city} has a temperature of {temp:.2f}°C\n")
    else:
        alert_text.insert(tk.END, "No alerts at this time.\n")

# Show daily summary in a chart
def show_summary_chart():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT city, AVG(temp) FROM weather
        GROUP BY city
    ''')
    
    data = cursor.fetchall()
    conn.close()

    cities = [row[0] for row in data]
    temps = [row[1] for row in data]
    
    plt.bar(cities, temps, color='skyblue')
    plt.title("Average Temperature per City")
    plt.xlabel("Cities")
    plt.ylabel("Temperature (°C)")
    plt.show()

# GUI Setup
root = tk.Tk()
root.title("Real-Time Weather Monitoring System")

# Weather Data Frame
weather_frame = tk.Frame(root)
weather_frame.pack(pady=10)
output_text = tk.Text(weather_frame, width=60, height=10)
output_text.pack()

# Buttons
refresh_button = tk.Button(root, text="Refresh Weather Data", command=display_weather_data)
refresh_button.pack(pady=5)

alerts_button = tk.Button(root, text="Check Alerts", command=show_alerts)
alerts_button.pack(pady=5)

chart_button = tk.Button(root, text="Show Daily Summary Chart", command=show_summary_chart)
chart_button.pack(pady=5)

# Alert Text Box
alert_frame = tk.Frame(root)
alert_frame.pack(pady=10)
alert_text = tk.Text(alert_frame, width=60, height=5)
alert_text.pack()

root.mainloop()
