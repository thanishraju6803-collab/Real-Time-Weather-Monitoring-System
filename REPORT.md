# MICRO PROJECT REPORT

## Cover Page
**Project Title:** Real-Time Weather Monitoring and Analytics System  
**Course:** Advanced Python Programming  
**Academic Year:** 2026–2027  
**Student Name:** __________________________  
**USN:** __________________________  
**Section:** __________________________  
**Institution:** __________________________  

# Chapter 1 — Introduction

## 1.1 Background
Weather information supports daily planning and environmental awareness. This project creates a Python desktop application that fetches current weather through a public REST API, saves observations locally and analyzes saved records.

## 1.2 Problem Statement
A basic weather lookup does not by itself maintain local observation history or provide database record management and analytics. The project integrates live weather retrieval, persistent storage, CRUD operations, statistical summaries and charts.

## 1.3 Objectives
- Retrieve current weather for a city through a REST API.
- Display temperature, humidity, wind speed, pressure and weather condition.
- Save observations and timestamps in SQLite.
- Implement Create, Read, Update and Delete.
- Analyze saved records using Pandas and NumPy.
- Create at least two Matplotlib visualizations.
- Demonstrate all five Advanced Python Programming modules.
- Export structured data in CSV and JSON formats.

## 1.4 Scope
The system focuses on current weather observations saved while the application is used. Historical analytics depend on the local records collected by the application. The current-weather endpoint is not treated as a historical archive.

# Chapter 2 — Requirements and Technology

## 2.1 Hardware Requirements
- Desktop or laptop capable of running Python and a GUI.
- Recommended 4 GB RAM or more.
- Internet connection for live API calls.

## 2.2 Software Requirements
- Python 3.10 or later.
- Visual Studio Code or another Python editor.
- Tkinter, OpenWeather API key and packages in `requirements.txt`.

## 2.3 Technologies
Python, Tkinter, Requests, aiohttp, SQLite, Pandas, NumPy, Matplotlib, CSV, JSON and logging.

## 2.4 Database Tables

### weather_records
| Column | Type | Purpose |
|---|---|---|
| id | INTEGER PRIMARY KEY | Unique observation ID |
| city | TEXT | City name |
| temperature | REAL | Celsius |
| humidity | INTEGER | Relative humidity, 0–100 |
| wind_speed | REAL | Metres per second |
| pressure | REAL | hPa |
| weather_condition | TEXT | Condition description |
| recorded_at | TEXT | Timestamp with timezone offset |

### saved_cities
| Column | Type | Purpose |
|---|---|---|
| id | INTEGER PRIMARY KEY | Unique city ID |
| city | TEXT UNIQUE | City name |
| country_code | TEXT | Optional country code |

An index on city and timestamp supports history queries. Tables are initialized automatically at startup.

## 2.5 API Integration
The application uses the OpenWeather Current Weather endpoint and metric units. The API key is read from `.env`, not hard-coded. The application handles invalid city names, missing keys, HTTP failures and timeouts.

# Chapter 3 — Implementation

## 3.1 Architecture
The Tkinter dashboard receives user input. The API service fetches current weather and maps the response to a weather model. The database service stores records in SQLite. The analytics service loads saved observations into Pandas, uses NumPy for calculations and Matplotlib for charts. The file handler exports records to CSV and JSON.

## 3.2 Module I — Object-Oriented Programming
`WeatherRecord` defines the data model and validation. `CurrentWeatherRecord` and `HistoricalWeatherRecord` inherit from it and override `get_summary()`. `__str__()` formats records, `__lt__()` compares temperatures, `from_api_response()` is a class method and `valid_temperature()` is a static method. Constructors and instance methods initialize and use object data.

## 3.3 Module II — Functional Programming and Iterators
The analytics module uses lambda expressions, `map()`, `filter()` and `reduce()`. Set and dictionary comprehensions organize cities and observations. `record_generator()` yields one record at a time; `temperature_iterator()` returns an iterator. The timing decorator measures function execution, a closure remembers a temperature threshold, and `apply_operation()` is a higher-order function.

## 3.4 Module III — Concurrency and Performance
A worker thread performs API calls without blocking the GUI. AsyncIO and aiohttp retrieve multiple cities concurrently. `ProcessPoolExecutor` demonstrates multiprocessing for a CPU-oriented calculation. `time.perf_counter()` measures elapsed time and the decorator logs timing. Multiprocessing overhead may exceed its benefit on small workloads.

## 3.5 Module IV — Libraries and Data Handling
Pandas handles records and summary calculations. NumPy computes mean, minimum, maximum and standard deviation. Matplotlib generates a temperature-trend line chart and a city-comparison bar chart. Regular expressions validate city input. CSV and JSON provide structured data export.

## 3.6 Module V — Application Development
Tkinter provides the GUI, OpenWeather supplies current weather through a REST API, and SQLite stores observations. The interface supports create, read, update and delete operations and integrates API access, analytics, charts and file export.

## 3.7 Logging and Error Handling
The application logs API, database, export, chart and multiprocessing errors to `logs/app.log`. It handles missing API keys, invalid input, network errors and unexpected responses with readable messages.

# Chapter 4 — Results

Add screenshots captured from the running application.

## 4.1 Main GUI
Insert a screenshot of the Weather Monitor dashboard and history table.

## 4.2 Live API Output
Insert a screenshot showing the city, temperature, humidity, wind speed, pressure and condition from the API.

## 4.3 Database and CRUD
Insert screenshots of stored records, an updated record and a deleted record.

## 4.4 Analytics
Insert a screenshot of the statistical summary.

## 4.5 Visualizations
Insert the temperature-trend line chart and average-temperature-by-city bar chart. These charts should use actual saved observations.

## 4.6 Structured Files and Concurrency
Insert CSV and JSON exports, AsyncIO multi-city output and multiprocessing output.

# Chapter 5 — Testing

Fill the actual-result column after running each test.

| ID | Test case | Expected result | Actual result |
|---|---|---|---|
| T01 | Fetch valid city | Weather shown and saved | To be filled |
| T02 | Invalid city | Friendly error message | To be filled |
| T03 | Missing API key | Setup message shown | To be filled |
| T04 | Network failure | Error handled; GUI stays responsive | To be filled |
| T05 | Create record | Record inserted in SQLite | To be filled |
| T06 | Read history | Saved rows displayed | To be filled |
| T07 | Update record | Selected values changed | To be filled |
| T08 | Delete record | Selected row removed | To be filled |
| T09 | Analytics | Summary calculated from saved records | To be filled |
| T10 | Charts | Two charts displayed | To be filled |
| T11 | CSV/JSON export | Files contain saved records | To be filled |
| T12 | AsyncIO | Multiple requests run concurrently | To be filled |
| T13 | Multiprocessing | CPU tasks return results and timing | To be filled |
| T14 | Restart application | History persists | To be filled |

## Conclusion
The project integrates a weather REST API, desktop GUI, SQLite CRUD, analytics and visualization in an end-to-end Python application. It demonstrates concepts from all five modules of Advanced Python Programming.

## References
1. Advanced Python Programming — Micro Project Manual, Academic Year 2026–2027.
2. OpenWeather API: https://openweathermap.org/api
3. Python documentation: https://docs.python.org/3/
4. SQLite documentation: https://www.sqlite.org/docs.html
5. Pandas documentation: https://pandas.pydata.org/docs/
6. NumPy documentation: https://numpy.org/doc/
7. Matplotlib documentation: https://matplotlib.org/stable/
