import sqlite3
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path(__file__).resolve().parent / "data" / "weather.db"

class WeatherDatabase:
    def __init__(self, path=None):
        self.path = Path(path) if path else DB_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def connection(self):
        conn = sqlite3.connect(self.path, timeout=10)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def initialize(self):
        with self.connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS weather_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT NOT NULL,
                    temperature REAL NOT NULL,
                    humidity INTEGER NOT NULL CHECK(humidity BETWEEN 0 AND 100),
                    wind_speed REAL NOT NULL,
                    pressure REAL NOT NULL,
                    weather_condition TEXT NOT NULL,
                    recorded_at TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS saved_cities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT NOT NULL UNIQUE,
                    country_code TEXT DEFAULT ''
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_weather_city_time ON weather_records(city, recorded_at)")

    def create(self, record):
        with self.connection() as conn:
            cursor = conn.execute("""
                INSERT INTO weather_records
                (city, temperature, humidity, wind_speed, pressure, weather_condition, recorded_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (record.city, record.temperature, record.humidity, record.wind_speed,
                  record.pressure, record.weather_condition, record.recorded_at))
            conn.execute("INSERT OR IGNORE INTO saved_cities(city) VALUES (?)", (record.city,))
            return cursor.lastrowid

    def read_all(self, city=None, limit=2000):
        with self.connection() as conn:
            if city:
                rows = conn.execute("SELECT * FROM weather_records WHERE city LIKE ? ORDER BY recorded_at DESC LIMIT ?",
                                    (f"%{city}%", limit)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM weather_records ORDER BY recorded_at DESC LIMIT ?", (limit,)).fetchall()
            return [dict(row) for row in rows]

    def read_one(self, record_id):
        with self.connection() as conn:
            row = conn.execute("SELECT * FROM weather_records WHERE id=?", (record_id,)).fetchone()
            return dict(row) if row else None

    def update(self, record_id, values):
        allowed = {"city", "temperature", "humidity", "wind_speed", "pressure", "weather_condition", "recorded_at"}
        fields = [key for key in values if key in allowed]
        if not fields:
            return False
        sql = ", ".join(f"{field}=?" for field in fields)
        params = [values[field] for field in fields] + [record_id]
        with self.connection() as conn:
            cursor = conn.execute(f"UPDATE weather_records SET {sql} WHERE id=?", params)
            return cursor.rowcount > 0

    def delete(self, record_id):
        with self.connection() as conn:
            cursor = conn.execute("DELETE FROM weather_records WHERE id=?", (record_id,))
            return cursor.rowcount > 0
