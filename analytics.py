import time
from functools import reduce
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import timed, make_temperature_filter, apply_operation

class WeatherAnalytics:
    def __init__(self, records):
        self.records = list(records)
        self.df = pd.DataFrame(self.records)

    @timed
    def summary(self):
        if self.df.empty:
            return {"count": 0}
        temps = pd.to_numeric(self.df["temperature"], errors="coerce").dropna().to_numpy(dtype=float)
        humidity = pd.to_numeric(self.df["humidity"], errors="coerce").dropna()
        wind = pd.to_numeric(self.df["wind_speed"], errors="coerce").dropna()
        if len(temps) == 0:
            return {"count": 0}
        return {
            "count": len(self.df),
            "average_temperature": float(np.mean(temps)),
            "minimum_temperature": float(np.min(temps)),
            "maximum_temperature": float(np.max(temps)),
            "temperature_std": float(np.std(temps)),
            "average_humidity": float(humidity.mean()) if len(humidity) else 0,
            "average_wind_speed": float(wind.mean()) if len(wind) else 0,
        }

    def functional_examples(self):
        temps = [float(row["temperature"]) for row in self.records]
        # lambda, map, filter, reduce and comprehensions
        sorted_temps = sorted(temps, key=lambda x: x)
        fahrenheit = list(map(lambda c: c * 9 / 5 + 32, temps))
        hot = list(filter(make_temperature_filter(30), self.records))
        total = reduce(lambda a, b: a + b, temps, 0.0)
        unique_cities = {row["city"] for row in self.records}
        by_city = {city: [r for r in self.records if r["city"] == city] for city in unique_cities}
        # Use the higher-order function in the running analytics flow.
        rounded_temps = apply_operation(temps, lambda value: round(value, 1))
        # Consume both the generator and iterator rather than only defining them.
        generated_count = sum(1 for _ in self.record_generator())
        iterated_temperatures = list(self.temperature_iterator())
        return {"sorted": sorted_temps, "fahrenheit": fahrenheit, "hot": hot,
                "total": total, "cities": unique_cities, "by_city": by_city,
                "rounded": rounded_temps, "generated_count": generated_count,
                "iterated_temperatures": iterated_temperatures}

    def record_generator(self):
        for record in self.records:
            yield record

    def temperature_iterator(self):
        return iter(float(record["temperature"]) for record in self.records)

    def charts(self):
        if self.df.empty:
            raise ValueError("No saved records yet. Fetch weather first.")
        df = self.df.copy()
        df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
        df["recorded_at"] = pd.to_datetime(df["recorded_at"], errors="coerce")
        df = df.dropna(subset=["temperature", "recorded_at"])
        if df.empty:
            raise ValueError("No valid date/temperature observations.")
        city = df["city"].mode().iloc[0]
        one_city = df[df["city"] == city].sort_values("recorded_at")
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        ax1.plot(one_city["recorded_at"], one_city["temperature"], marker="o")
        ax1.set_title(f"Temperature Trend — {city}")
        ax1.set_xlabel("Recorded time")
        ax1.set_ylabel("Temperature (°C)")
        ax1.tick_params(axis="x", rotation=30)
        fig1.tight_layout()

        means = df.groupby("city")["temperature"].mean().sort_values()
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        means.plot(kind="bar", ax=ax2)
        ax2.set_title("Average Recorded Temperature by City")
        ax2.set_xlabel("City")
        ax2.set_ylabel("Temperature (°C)")
        fig2.tight_layout()
        return fig1, fig2

def _cpu_task(number):
    total = 0
    for n in range(1, number):
        total += (n * n) % 97
    return total

def multiprocessing_demo():
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=2) as pool:
        result = list(pool.map(_cpu_task, [160000, 170000, 180000, 190000]))
    return result, time.perf_counter() - start
