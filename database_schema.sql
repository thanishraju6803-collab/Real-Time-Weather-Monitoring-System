CREATE TABLE IF NOT EXISTS weather_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL,
    temperature REAL NOT NULL,
    humidity INTEGER NOT NULL CHECK(humidity BETWEEN 0 AND 100),
    wind_speed REAL NOT NULL,
    pressure REAL NOT NULL,
    weather_condition TEXT NOT NULL,
    recorded_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS saved_cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL UNIQUE,
    country_code TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_weather_city_time ON weather_records(city, recorded_at);
