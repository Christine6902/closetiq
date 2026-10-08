"""Weather route — live conditions + outfit bucket for a coordinate."""
from tina4_python.core.router import get
from tina4_python.swagger import description, tags
from src.app.weather import fetch_current_weather


@description("Return live weather for a coordinate plus the matched outfit weather bucket (hot/mild/cold/rainy).")
@tags(["weather"])
@get("/api/weather")
async def current_weather(request, response):
    """Look up live weather for ?lat=&lon= and return it with the mapped bucket as JSON."""
    lat = request.query.get("lat")
    lon = request.query.get("lon")
    if lat is None or lon is None:
        return response({"error": "lat and lon query parameters are required."}, 400)

    result = fetch_current_weather(lat, lon)
    if "error" in result:
        status = 400 if "Invalid" in result["error"] or "range" in result["error"] else 502
        return response(result, status)
    return response(result)
