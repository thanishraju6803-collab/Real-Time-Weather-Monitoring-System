# Real-Time Weather Monitoring and Analytics System
Advanced Python Programming Micro Project — Academic Year 2026–2027

## Setup (Windows / VS Code)
1. Open this folder in VS Code.
2. In the terminal run `py -m venv .venv`
3. Activate using `.venv\Scripts\Activate.ps1`. If PowerShell blocks activation, use `.venv\Scripts\python.exe` in the commands below.
4. Install packages: `python -m pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your OpenWeather API key.
6. Run `python main.py`.

Get a key at https://openweathermap.org/api. Do not share or upload `.env`.

## Features
- Tkinter desktop GUI and live current-weather API integration
- SQLite weather history and Create/Read/Update/Delete operations
- Pandas/NumPy analytics and two Matplotlib charts
- CSV/JSON export
- OOP, functional programming, generators/iterators, decorator, closure and higher-order function
- Threading, AsyncIO, multiprocessing, timing, logging, exception handling and validation

## Files
- `main.py`: GUI and application flow
- `models.py`: OOP classes
- `api_service.py`: REST API and AsyncIO calls
- `database.py`: SQLite schema and CRUD
- `analytics.py`: data processing, charts and multiprocessing demonstration
- `file_handler.py`: CSV/JSON export
- `utils.py`: decorator, closure, higher-order function and logging
- `REPORT.md`: report chapters based on the project manual
- `tests/test_project.py`: basic tests

## Important scope note
The current-weather endpoint returns current conditions, not a historical archive. Trend charts use observations saved by this application over time. Sample charts/data should not be described as live results.
