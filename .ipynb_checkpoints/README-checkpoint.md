# SQLAlchemy Challenge: Hawaii Climate Analysis

**NOTE**  
This project was developed using starter code provided by the course. Folder names and structure largely follow the provided template.
Project files can be found in the SurfsUp folder. 

## Description
This repository contains a two-part climate analysis and Flask API design project focused on historical weather data in Hawaii. In the first part, we use Python, SQLAlchemy, and various data analysis libraries to explore climate patterns. In the second part, we build a Flask API to expose the analyzed data through different endpoints.

## Summary

### Part 1: Analyze and Explore the Climate Data
Using a Jupyter Notebook (`climate_starter.ipynb`), we perform the following tasks:

1. **Database Connection**  
   - Connect to the provided SQLite database, `hawaii.sqlite`, using `SQLAlchemy create_engine`.
   - Reflect existing tables into SQLAlchemy ORM classes (`Measurement` and `Station`).
   - Create a session to interact with the database.

2. **Precipitation Analysis**  
   - Identify the most recent date in the dataset (August 23, 2017).
   - Query the previous 12 months of precipitation data.
   - Load the query results into a Pandas DataFrame, sort by date, and plot the precipitation values.
   - Print summary statistics for the precipitation data.

3. **Station Analysis**  
   - Query the total number of stations in the dataset.
   - List stations and observation counts, find the most active station (`USC00519281`).
   - Query the minimum, maximum, and average temperature for the most active station.
   - Retrieve the previous 12 months of temperature data for this station and plot the results as a histogram.

4. **Close the Session**  
   - Ensure that the session is properly closed at the end of the notebook.

### Part 2: Design Your Climate App
Using Flask, we create an API (`app.py`) that returns JSON responses for various endpoints:

1. **Landing Page (/)**  
   - Lists all available routes.

2. **Precipitation Route (/api/v1.0/precipitation)**  
   - Returns a dictionary (in JSON) of dates and precipitation amounts for the last year.

3. **Stations Route (/api/v1.0/stations)**  
   - Returns a JSON list of station IDs.

4. **TOBS Route (/api/v1.0/tobs)**  
   - Returns a JSON list of temperature observations (TOBS) for the most active station from the past year.

5. **Start Route (/api/v1.0/<start>)**  
   - Returns minimum, average, and maximum temperature for all dates greater than or equal to the provided start date (YYYY-MM-DD).

6. **Start/End Route (/api/v1.0/<start>/<end>)**  
   - Returns minimum, average, and maximum temperature for dates between the provided start and end dates (inclusive).

## Requirements

### Tools and Libraries
- **SQLite / SQLAlchemy** for database connections and ORM
- **Flask** for building the web API
- **Pandas** and **NumPy** for data manipulation
- **Matplotlib** for plotting (in Jupyter Notebook)
- **Python** standard libraries: `datetime`, `os`, etc.

## Contact Information
If you have any questions or need more information, feel free to reach out via email:

**Email:** [ilir.hajdari111@gmail.com](mailto:ilir.hajdari111@gmail.com)