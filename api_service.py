import asyncio
import os
import re
import requests
import aiohttp
from dotenv import load_dotenv
from models import CurrentWeatherRecord

load_dotenv()

class WeatherAPIError(Exception):
    pass

class WeatherAPI:
    URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key=None, timeout=10):
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY", "").strip()
        self.timeout = timeout

    @staticmethod
    def valid_city(city):
        return bool(re.fullmatch(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ .'-]{0,79}", city.strip()))

    def fetch(self, city):
        if not self.valid_city(city):
            raise ValueError("Enter a valid city name.")
        if not self.api_key or self.api_key == "your_openweather_api_key_here":
            raise WeatherAPIError("API key missing. Copy .env.example to .env and add your OpenWeather API key.")
        try:
            response = requests.get(self.URL, params={"q": city, "appid": self.api_key, "units": "metric"}, timeout=self.timeout)
            if response.status_code == 404:
                raise WeatherAPIError(f"City '{city}' was not found.")
            if response.status_code == 401:
                raise WeatherAPIError("API key is invalid or not activated.")
            response.raise_for_status()
            payload = response.json()
            return CurrentWeatherRecord.from_api_response(payload.get("name", city), payload)
        except requests.Timeout as exc:
            raise WeatherAPIError("Request timed out. Try again.") from exc
        except requests.RequestException as exc:
            raise WeatherAPIError(f"Weather API request failed: {exc}") from exc
        except (KeyError, TypeError) as exc:
            raise WeatherAPIError("The API response did not contain expected weather fields.") from exc

    async def fetch_async_one(self, session, city):
        if not self.valid_city(city):
            raise ValueError(f"Invalid city: {city}")
        if not self.api_key or self.api_key == "your_openweather_api_key_here":
            raise WeatherAPIError("API key missing. Configure .env first.")
        try:
            async with session.get(self.URL, params={"q": city, "appid": self.api_key, "units": "metric"},
                                   timeout=aiohttp.ClientTimeout(total=self.timeout)) as response:
                if response.status == 404:
                    raise WeatherAPIError(f"City '{city}' was not found.")
                if response.status == 401:
                    raise WeatherAPIError("API key is invalid or not activated.")
                response.raise_for_status()
                payload = await response.json()
                return CurrentWeatherRecord.from_api_response(payload.get("name", city), payload)
        except asyncio.TimeoutError as exc:
            raise WeatherAPIError(f"Request timed out for {city}.") from exc
        except aiohttp.ClientError as exc:
            raise WeatherAPIError(f"Request failed for {city}: {exc}") from exc

    async def fetch_many(self, cities):
        async with aiohttp.ClientSession() as session:
            return await asyncio.gather(
                *(self.fetch_async_one(session, city) for city in cities),
                return_exceptions=True
            )
