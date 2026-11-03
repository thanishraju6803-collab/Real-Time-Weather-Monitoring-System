from dataclasses import dataclass
from datetime import datetime

@dataclass
class WeatherRecord:
    city: str
    temperature: float
    humidity: int
    wind_speed: float
    pressure: float
    weather_condition: str
    recorded_at: str = ""

    def __post_init__(self):
        self.city = self.city.strip()
        if not self.city:
            raise ValueError("City cannot be empty.")
        if not 0 <= int(self.humidity) <= 100:
            raise ValueError("Humidity must be between 0 and 100.")
        if not self.recorded_at:
            self.recorded_at = datetime.now().astimezone().isoformat(timespec="seconds")

    @classmethod
    def from_api_response(cls, city, payload):
        main = payload.get("main", {})
        weather = payload.get("weather", [{}])[0]
        wind = payload.get("wind", {})
        return cls(city, float(main["temp"]), int(main["humidity"]),
                   float(wind.get("speed", 0)), float(main.get("pressure", 0)),
                   str(weather.get("description", "Unknown")).title())

    @staticmethod
    def valid_temperature(value):
        try:
            return -100 <= float(value) <= 70
        except (TypeError, ValueError):
            return False

    def __str__(self):
        return f"{self.city}: {self.temperature:.1f}°C, {self.weather_condition}"

    def __lt__(self, other):
        if not isinstance(other, WeatherRecord):
            return NotImplemented
        return self.temperature < other.temperature

class CurrentWeatherRecord(WeatherRecord):
    def get_summary(self):
        return f"Current weather in {self.city}: {self.weather_condition}, {self.temperature:.1f}°C"

class HistoricalWeatherRecord(WeatherRecord):
    def get_summary(self):
        return f"Historical observation for {self.city}: {self.temperature:.1f}°C"
