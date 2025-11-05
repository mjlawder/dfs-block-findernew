# 🏈 DFS Block Finder - Quick Start

Get up and running in 5 minutes with DraftKings or FanDuel!

## 1. Install Python
Download Python 3.8+ from python.org if you don't have it installed

## 2. Open Terminal/Command Prompt
- **Windows**: Search for "cmd" or "PowerShell"
- **Mac**: Search for "Terminal"  
- **Linux**: You know what to do 😉

## 3. Navigate to This Folder
```bash
cd path/to/dfs_app
```

## 4. Install Dependencies
```bash
pip install -r requirements.txt
```

*If that doesn't work, try:*
```bash
pip3 install -r requirements.txt
```

*If you're on Linux/Mac and get permission errors:*
```bash
pip install -r requirements.txt --user
```

## 5. Generate Sample Data
This creates test files so you can try the app immediately:
```bash
python fetch_data.py --sample
```

You should see:
```
✅ Created draftkings_salaries_sample.csv
✅ Created nfl_weekly_stats_sample.csv
```

## 6. Run the App
```bash
streamlit run app.py
```

You'll see:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

## 7. Open Your Browser
The app should open automatically. If not, go to:
**http://localhost:8501**

## 8. Use the App

1. **Select your platform** (DraftKings or FanDuel) in the sidebar
2. **Select "Use Sample Data"** in the first tab
3. **Click "Find Player Blocks"**  
4. **Explore the results!**

**Pro tip**: Try both platforms to see pricing differences!

---

## Next Steps

### Get Live Data

Once you're comfortable with the sample data:

```bash
python fetch_data.py
```

This will fetch:
- Current DraftKings salaries (if slates are active)
- Latest NFL weekly stats

Then upload these files in the app.

### Troubleshooting

**"streamlit: command not found"**
```bash
pip install streamlit
# or
python -m pip install streamlit
```

**"ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

**Port already in use**
```bash
streamlit run app.py --server.port 8502
```

### Windows Users

If you prefer, double-click `START_WEBAPP.bat` instead of using command line!

---

## What You'll See

1. **Find Blocks Tab**: Upload data and discover player blocks
2. **Block Analysis Tab**: Deep dive into correlations and distributions
3. **Game Logs Tab**: Week-by-week performance charts  
4. **Guide Tab**: Complete strategy guide

## Tips for First Use

- Start with target price around $10,000-$10,500
- Set tolerance to $300
- Analyze 6 weeks of data
- Look for blocks with 0.75+ correlation
- Target 40+ ceiling scores

---

**Ready? Let's find some blocks! 🚀**
