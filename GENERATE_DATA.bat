@echo off
echo ================================================
echo   Generating Sample Data for Both Platforms
echo ================================================
echo.
echo This will create:
echo   - draftkings_salaries_sample.csv
echo   - fanduel_salaries_sample.csv  
echo   - nfl_weekly_stats_sample.csv
echo.
echo ================================================
echo.

python fetch_data.py --sample --platform both

echo.
echo ================================================
echo   Sample data generated!
echo ================================================
echo.
echo You can now run the app with:
echo   streamlit run app.py
echo.
pause
