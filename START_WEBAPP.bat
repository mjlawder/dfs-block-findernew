@echo off
echo ========================================
echo  NFL DFS BLOCK FINDER
echo ========================================
echo.
echo Installing required packages...
pip install streamlit pandas requests
echo.
echo ========================================
echo Starting webapp...
echo ========================================
echo.
echo The app will open in your browser automatically.
echo If it doesn't, go to: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.
streamlit run dfs_block_finder.py
pause
