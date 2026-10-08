"""Live weather lookup for ClosetIQ.

Uses Open-Meteo (open-meteo.com) — free, no API key required — via Tina4's
``Api`` client, and maps the current conditions onto the outfit engine's
weather buckets (hot / mild / cold / rainy).
"""
from tina4_python.api import Api

_API_BASE = "https://api.open-meteo.com"

# WMO weather interpretation codes → short human labels.
WMO_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    56: "Freezing drizzle", 57: "Dense freezing drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    66: "Freezing rain", 67: "Heavy freezing rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow", 77: "Snow grains",
    80: "Slight showers", 81: "Moderate showers", 82: "Violent showers",
    85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Severe thunderstorm with hail",
}

_RAINY_CODES = {51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82, 95, 96, 99}
_SNOW_CODES = {71, 73, 75, 77, 85, 86}


def map_to_bucket(temperature, code, precipitation=0.0):
    """Map live conditions onto an outfit-engine weather bucket.

    Precipitation and snow take precedence over temperature, since they drive
    the jacket decision; otherwise temperature bands choose hot/mild/cold.
    """
    code = int(code) if code is not None else -1
    temp = float(temperature) if temperature is not None else 18.0
    precip = float(precipitation) if precipitation is not None else 0.0

    if code in _RAINY_CODES or precip > 0.2:
        return "rainy"
    if code in _SNOW_CODES or temp < 12:
        return "cold"
    if temp >= 24:
        return "hot"
    return "mild"


def fetch_current_weather(lat, lon):
    """Fetch current weather for a coordinate.

    Returns a dict ``{temperature, precipitation, code, description, bucket}``
    on success, or ``{"error": "..."}`` on failure.
    """
    try:
        lat_f, lon_f = float(lat), float(lon)
    except (TypeError, ValueError):
        return {"error": "Invalid coordinates."}
    if not (-90 <= lat_f <= 90 and -180 <= lon_f <= 180):
        return {"error": "Coordinates out of range."}

    api = Api(_API_BASE)
    result = api.get("/v1/forecast", params={
        "latitude": round(lat_f, 4),
        "longitude": round(lon_f, 4),
        "current": "temperature_2m,weather_code,precipitation",
        "timezone": "auto",
    })

    if result.get("error"):
        return {"error": "Weather service unavailable."}

    current = (result.get("body") or {}).get("current")
    if not current or "temperature_2m" not in current:
        return {"error": "Weather data unavailable."}

    temperature = current.get("temperature_2m")
    code = current.get("weather_code")
    precipitation = current.get("precipitation", 0.0)

    return {
        "temperature": round(float(temperature)) if temperature is not None else None,
        "precipitation": precipitation,
        "code": code,
        "description": WMO_DESCRIPTIONS.get(int(code) if code is not None else -1, "Unknown"),
        "bucket": map_to_bucket(temperature, code, precipitation),
    }
