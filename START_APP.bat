@echo off
echo ================================================
echo   NFL DFS Player Block Finder
echo ================================================
echo.
echo Starting web application...
echo.
echo Once started, your browser will open to:
echo http://localhost:8501
echo.
echo To stop the app, press Ctrl+C in this window
echo.
echo ================================================
echo.

REM Check if running for first time
if not exist "draftkings_salaries_sample.csv" (
    echo First time setup detected...
    echo Generating sample data...
    python fetch_data.py --sample
    echo.
)

REM Start the Streamlit app
streamlit run app.py

pause
