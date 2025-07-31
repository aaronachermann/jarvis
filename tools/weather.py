import requests
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get current weather information for a city using the Open-Meteo API."""
    try:
        # Query coordinates via geocoding api
        geo_resp = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "it", "format": "json"},
            timeout=5,
        )
        geo_resp.raise_for_status()
        data = geo_resp.json()
        results = data.get("results")
        if not results:
            return f"Non trovo la citta' {city}."
        lat = results[0]["latitude"]
        lon = results[0]["longitude"]
        weather_resp = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon, "current_weather": True, "timezone": "auto"},
            timeout=5,
        )
        weather_resp.raise_for_status()
        weather = weather_resp.json().get("current_weather", {})
        temperature = weather.get("temperature")
        windspeed = weather.get("windspeed")
        if temperature is None:
            return "Non riesco a ottenere le informazioni meteo."
        return f"A {city.title()} ci sono {temperature}°C con vento a {windspeed} km/h." \
               if windspeed is not None else f"A {city.title()} ci sono {temperature}°C." 
    except Exception as e:
        return f"Errore nel recupero del meteo: {e}"
