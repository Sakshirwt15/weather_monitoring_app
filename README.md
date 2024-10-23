## Description
The Weather Monitoring App provides real-time weather updates for specified cities. It fetches weather data from an API, stores it in a local SQLite database, and offers a user-friendly interface to display current and historical weather conditions.

## Features
- Fetches real-time weather data using an external API.
- Stores weather data in a SQLite database.
- Displays current weather conditions through a graphical user interface (GUI).
- Provides daily weather summaries and alerts for specific conditions.
  
## Requirements
- Python 3.x
- Tkinter (included with Python)
- SQLite (included with Python)
- `requests` library for API calls
- `schedule` library for periodic tasks
- `matplotlib` for visualizations

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Sakshirwt15/weather_monitoring_app.git
cd weather_monitoring_app

pip install -r requirements.txt
## Usage
To start the weather monitoring application, run:
```bash
python weather_monitor.py

##Configuration
- Ensure you have access to the weather API and replace the API key in the code if necessary.
- Set user-configurable thresholds for alerts in the application settings.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them.
4. Push to your fork and submit a pull request.

## Acknowledgments
- Thanks to the OpenWeatherMap API for providing weather data.
- Inspired by other weather monitoring applications and tutorials.

