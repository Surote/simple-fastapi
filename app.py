from fastapi import FastAPI
from datetime import datetime
import pytz
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Instrument the app with Prometheus metrics
Instrumentator().instrument(app).expose(app)

@app.get("/")
async def read_root():
    countries = {code.upper(): name for code, name in pytz.country_names.items()}
    return {
        "message": "Welcome to FastAPI with async!",
        "instructions": "Use the /localtime/{country} endpoint to get the local time.",
        "available_countries": countries
    }


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/localtime/{country}")
async def get_local_time(country: str):
    try:
        # Get the full name of the country
        country_name = pytz.country_names[country.upper()]
        # Get the timezone(s) for the country
        timezone = pytz.country_timezones[country.lower()]
        # Get the current local time in the first timezone
        local_time = datetime.now(pytz.timezone(timezone[0]))
        return {
            "country": country_name,
            "local_time": local_time.strftime("%Y-%m-%d %H:%M:%S")
        }
    except KeyError:
        return {"error": "Invalid country code or timezone not found"}