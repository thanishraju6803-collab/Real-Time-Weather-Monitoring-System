import asyncio
import logging
import threading
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime

from api_service import WeatherAPI
from database import WeatherDatabase
from models import WeatherRecord
from analytics import WeatherAnalytics, multiprocessing_demo
from file_handler import export_csv, export_json, import_csv, import_json
from utils import setup_logging

class WeatherDashboard(tk.Tk):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.api = WeatherAPI()
        self.title("Real-Time Weather Monitoring and Analytics System")
        self.geometry("1120x720")
        self.minsize(900, 600)
        self.build_ui()
        self.refresh_history()

    def build_ui(self):
        header = ttk.Frame(self, padding=12)
        header.pack(fill="x")
        ttk.Label(header, text="Weather Monitor", font=("Segoe UI", 20, "bold")).pack(side="left")
        ttk.Label(header, text="Live weather • SQLite history • Analytics", padding=10).pack(side="left")

        search = ttk.LabelFrame(self, text="Current weather", padding=10)
        search.pack(fill="x", padx=12, pady=5)
        self.city = tk.StringVar(value="Bengaluru")
        ttk.Label(search, text="City:").pack(side="left")
        ttk.Entry(search, textvariable=self.city, width=24).pack(side="left", padx=8)
        ttk.Button(search, text="Fetch & Save", command=self.fetch_weather).pack(side="left", padx=3)
        ttk.Button(search, text="Fetch Multiple Cities (AsyncIO)", command=self.fetch_multiple).pack(side="left", padx=3)
        ttk.Button(search, text="CPU Demo (multiprocessing)", command=self.run_cpu_demo).pack(side="left", padx=3)

        self.current = tk.StringVar(value="Enter a city and click Fetch & Save.")
        ttk.Label(self, textvariable=self.current, padding=14, relief="groove", anchor="w").pack(fill="x", padx=12, pady=5)

        actions = ttk.Frame(self, padding=8)
        actions.pack(fill="x")
        buttons = [
            ("Refresh History", self.refresh_history), ("Update Selected", self.update_selected),
            ("Delete Selected", self.delete_selected), ("Analytics & Charts", self.show_analytics),
            ("Export CSV", self.export_csv), ("Export JSON", self.export_json),
            ("Import CSV/JSON", self.import_records)
        ]
        for label, command in buttons:
            ttk.Button(actions, text=label, command=command).pack(side="left", padx=3)

        frame = ttk.Frame(self, padding=12)
        frame.pack(fill="both", expand=True)
        self.columns = ("id", "city", "temperature", "humidity", "wind_speed", "pressure", "condition", "recorded_at")
        self.table = ttk.Treeview(frame, columns=self.columns, show="headings")
        names = {"id":"ID", "city":"City", "temperature":"Temp °C", "humidity":"Humidity %",
                 "wind_speed":"Wind m/s", "pressure":"Pressure hPa", "condition":"Condition", "recorded_at":"Recorded At"}
        widths = {"id":45, "city":120, "temperature":80, "humidity":90, "wind_speed":90,
                  "pressure":95, "condition":130, "recorded_at":230}
        for col in self.columns:
            self.table.heading(col, text=names[col])
            self.table.column(col, width=widths[col], anchor="center")
        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scroll.set)
        self.table.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.status = tk.StringVar(value="Ready")
        ttk.Label(self, textvariable=self.status, relief="sunken", padding=5, anchor="w").pack(fill="x", side="bottom")

    def fetch_weather(self):
        city = self.city.get().strip()
        self.status.set(f"Fetching {city}...")
        threading.Thread(target=self._fetch_worker, args=(city,), daemon=True).start()

    def _fetch_worker(self, city):
        try:
            record = self.api.fetch(city)
            record_id = self.db.create(record)
            self.after(0, lambda: self._fetch_success(record, record_id))
        except Exception as exc:
            logging.exception("Weather fetch failed")
            self.after(0, lambda message=str(exc): self._show_error(message))

    def _fetch_success(self, record, record_id):
        self.current.set(
            f"{record.city} | {record.temperature:.1f} °C | {record.weather_condition} | "
            f"Humidity {record.humidity}% | Wind {record.wind_speed:.1f} m/s | "
            f"Pressure {record.pressure:.0f} hPa | Saved ID {record_id}"
        )
        self.status.set("Weather fetched and saved.")
        self.refresh_history()

    def _show_error(self, message):
        self.status.set("Request failed.")
        messagebox.showerror("Weather/API error", message)

    def fetch_multiple(self):
        raw = simpledialog.askstring("Multiple cities", "Enter city names separated by commas:")
        if not raw:
            return
        cities = [c.strip() for c in raw.split(",") if c.strip()]
        if not cities:
            return
        self.status.set("Fetching cities concurrently with AsyncIO...")
        threading.Thread(target=self._async_worker, args=(cities,), daemon=True).start()

    def _async_worker(self, cities):
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        try:
            results = asyncio.run(self.api.fetch_many(cities))
            saved, errors = [], []
            for city, result in zip(cities, results):
                if isinstance(result, Exception):
                    errors.append(f"{city}: {result}")
                else:
                    saved.append(self.db.create(result))
            message = f"Saved {len(saved)} record(s)."
            if errors:
                message += "\\n\\nFailures:\\n" + "\\n".join(errors)
            self.after(0, lambda: self._async_done(message))
        except Exception as exc:
            logging.exception("AsyncIO operation failed")
            self.after(0, lambda message=str(exc): self._show_error(message))

    def _async_done(self, message):
        self.refresh_history()
        self.status.set(message.replace("\\n", " "))
        messagebox.showinfo("AsyncIO results", message)

    def refresh_history(self):
        for item in self.table.get_children():
            self.table.delete(item)
        try:
            for r in self.db.read_all(limit=500):
                self.table.insert("", "end", values=(
                    r["id"], r["city"], f'{r["temperature"]:.1f}', r["humidity"],
                    f'{r["wind_speed"]:.1f}', f'{r["pressure"]:.0f}',
                    r["weather_condition"], r["recorded_at"]
                ))
            self.status.set("History refreshed.")
        except Exception as exc:
            logging.exception("History read failed")
            messagebox.showerror("Database error", str(exc))

    def selected_id(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Select record", "Please select a record first.")
            return None
        return int(self.table.item(selected[0], "values")[0])

    def update_selected(self):
        rid = self.selected_id()
        if rid is None:
            return
        old = self.db.read_one(rid)
        city = simpledialog.askstring("Update record", "City:", initialvalue=old["city"])
        if city is None:
            return
        temp = simpledialog.askfloat("Update record", "Temperature °C:", initialvalue=old["temperature"])
        if temp is None:
            return
        humidity = simpledialog.askinteger("Update record", "Humidity (0–100):",
                                           initialvalue=old["humidity"], minvalue=0, maxvalue=100)
        if humidity is None:
            return
        if not WeatherRecord.valid_temperature(temp) or not city.strip():
            messagebox.showerror("Invalid input", "Enter a city and temperature between -100 and 70°C.")
            return
        self.db.update(rid, {"city": city.strip(), "temperature": temp, "humidity": humidity,
                             "recorded_at": datetime.now().astimezone().isoformat(timespec="seconds")})
        self.refresh_history()
        messagebox.showinfo("Updated", "Record updated.")

    def delete_selected(self):
        rid = self.selected_id()
        if rid is None:
            return
        if messagebox.askyesno("Confirm delete", f"Delete record ID {rid}?"):
            if self.db.delete(rid):
                self.refresh_history()
                messagebox.showinfo("Deleted", "Record deleted.")

    def show_analytics(self):
        records = self.db.read_all(limit=5000)
        if not records:
            messagebox.showinfo("Analytics", "No records yet. Fetch weather first.")
            return
        analytics = WeatherAnalytics(records)
        stats = analytics.summary()
        examples = analytics.functional_examples()
        window = tk.Toplevel(self)
        window.title("Weather Analytics")
        window.geometry("650x410")
        text = (
            f"Observations: {stats.get('count', 0)}\\n"
            f"Average temperature: {stats.get('average_temperature', 0):.2f} °C\\n"
            f"Minimum temperature: {stats.get('minimum_temperature', 0):.2f} °C\\n"
            f"Maximum temperature: {stats.get('maximum_temperature', 0):.2f} °C\\n"
            f"Temperature standard deviation: {stats.get('temperature_std', 0):.2f}\\n"
            f"Average humidity: {stats.get('average_humidity', 0):.2f}%\\n"
            f"Average wind speed: {stats.get('average_wind_speed', 0):.2f} m/s\\n\\n"
            f"Unique cities: {', '.join(sorted(examples['cities']))}\\n"
            f"Observations at or above 30°C: {len(examples['hot'])}"
        )
        ttk.Label(window, text=text, font=("Consolas", 11), justify="left", padding=15).pack(fill="x")
        ttk.Button(window, text="Show both charts", command=lambda: self.show_charts(analytics)).pack(pady=8)

    def show_charts(self, analytics):
        try:
            for fig in analytics.charts():
                fig.show()
        except Exception as exc:
            logging.exception("Chart generation failed")
            messagebox.showerror("Chart error", str(exc))

    def export_csv(self):
        try:
            path = export_csv(self.db.read_all(limit=10000))
            messagebox.showinfo("Export complete", f"CSV saved to:\\n{path}")
        except Exception as exc:
            logging.exception("CSV export failed")
            messagebox.showerror("Export error", str(exc))

    def export_json(self):
        try:
            path = export_json(self.db.read_all(limit=10000))
            messagebox.showinfo("Export complete", f"JSON saved to:\\n{path}")
        except Exception as exc:
            logging.exception("JSON export failed")
            messagebox.showerror("Export error", str(exc))

    def import_records(self):
        filename = filedialog.askopenfilename(
            title="Import weather records",
            filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json")]
        )
        if not filename:
            return
        try:
            if filename.lower().endswith(".csv"):
                rows = import_csv(filename)
            elif filename.lower().endswith(".json"):
                rows = import_json(filename)
            else:
                raise ValueError("Choose a CSV or JSON file.")
            imported = 0
            for row in rows:
                city = str(row.get("city", "")).strip()
                if not city:
                    continue
                record = WeatherRecord(
                    city=city,
                    temperature=float(row["temperature"]),
                    humidity=int(float(row["humidity"])),
                    wind_speed=float(row.get("wind_speed", 0)),
                    pressure=float(row.get("pressure", 0)),
                    weather_condition=str(row.get("weather_condition", "Imported")),
                    recorded_at=str(row.get("recorded_at") or datetime.now().astimezone().isoformat(timespec="seconds"))
                )
                self.db.create(record)
                imported += 1
            self.refresh_history()
            messagebox.showinfo("Import complete", f"Imported {imported} record(s).")
        except Exception as exc:
            logging.exception("Import failed")
            messagebox.showerror("Import error", str(exc))

    def run_cpu_demo(self):
        self.status.set("Running multiprocessing CPU demo...")
        def worker():
            try:
                result, elapsed = multiprocessing_demo()
                message = f"CPU results: {result}\\nElapsed time: {elapsed:.3f} seconds"
                self.after(0, lambda: messagebox.showinfo("Multiprocessing", message))
                self.after(0, lambda: self.status.set("Multiprocessing demo completed."))
            except Exception as exc:
                logging.exception("Multiprocessing demo failed")
                self.after(0, lambda message=str(exc): self._show_error(message))
        threading.Thread(target=worker, daemon=True).start()

def main():
    setup_logging()
    db = WeatherDatabase()
    db.initialize()
    WeatherDashboard(db).mainloop()

if __name__ == "__main__":
    main()
