import tempfile
import unittest
from pathlib import Path
from models import WeatherRecord, CurrentWeatherRecord, HistoricalWeatherRecord
from database import WeatherDatabase
from utils import make_temperature_filter, apply_operation

class ProjectTests(unittest.TestCase):
    def test_model(self):
        r = WeatherRecord("Bengaluru", 28, 60, 2.0, 1013, "Clouds")
        self.assertIn("Bengaluru", str(r))
        self.assertTrue(WeatherRecord.valid_temperature(28))
        self.assertFalse(WeatherRecord.valid_temperature(500))

    def test_polymorphism(self):
        a = CurrentWeatherRecord("A", 20, 50, 1, 1010, "Clear")
        b = HistoricalWeatherRecord("B", 18, 55, 2, 1009, "Rain")
        self.assertIn("Current weather", a.get_summary())
        self.assertIn("Historical observation", b.get_summary())

    def test_crud(self):
        with tempfile.TemporaryDirectory() as folder:
            db = WeatherDatabase(Path(folder) / "test.db")
            db.initialize()
            r = WeatherRecord("Test City", 25, 60, 2.0, 1012, "Clear")
            rid = db.create(r)
            self.assertEqual(db.read_one(rid)["city"], "Test City")
            self.assertTrue(db.update(rid, {"temperature": 26.0}))
            self.assertEqual(db.read_one(rid)["temperature"], 26.0)
            self.assertTrue(db.delete(rid))
            self.assertIsNone(db.read_one(rid))

    def test_closure_and_higher_order(self):
        check = make_temperature_filter(25)
        self.assertTrue(check({"temperature": 30}))
        self.assertEqual(apply_operation([1, 2], lambda n: n * 2), [2, 4])

if __name__ == "__main__":
    unittest.main()
