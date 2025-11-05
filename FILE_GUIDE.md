# 📁 File Guide - What Each File Does

## Main Application Files

### app.py ⭐ **MAIN FILE**
The core Streamlit web application. This is what you run to start the app.
- Interactive web interface
- Data upload & visualization
- Block finding & analysis
- Game log charts

**To run:** `streamlit run app.py`

---

## Data Management Files

### fetch_data.py
Script to pull DraftKings pricing and NFL stats from free APIs.

**Commands:**
```bash
python fetch_data.py --sample    # Generate test data
python fetch_data.py            # Fetch live data
python fetch_data.py --dk-only  # DraftKings only
python fetch_data.py --stats-only # NFL stats only
```

### block_finder.py
Core analysis engine that finds and evaluates player blocks.
- Combination analysis
- Correlation calculations
- Game log aggregation
- Block scoring

---

## Configuration Files

### requirements.txt
Lists all Python packages needed to run the app.

**Packages included:**
- streamlit (web app framework)
- pandas (data manipulation)
- numpy (math operations)
- plotly (interactive charts)
- nfl-data-py (free NFL stats)
- draft-kings (DK API wrapper)

**Install with:** `pip install -r requirements.txt`

### README.md
Comprehensive documentation covering:
- Installation instructions
- Usage guide
- Strategy tips
- Data source details
- Troubleshooting
- Deployment options

---

## Quick Start Files

### QUICKSTART.md
5-minute getting started guide. Follow this first!

### START_APP.bat (Windows only)
Double-click this file to automatically:
1. Generate sample data (first time only)
2. Start the web app
3. Open browser

---

## Legacy Files (Can be ignored)

These were from earlier iterations and are kept for reference:
- dfs_block_finder.py
- dfs_block_finder_pro.py
- dfs_data_fetcher.py
- test_block_finder.py

**You don't need these!** Use the new `app.py` instead.

---

## Typical Workflow

1. **First Time Setup:**
   ```bash
   pip install -r requirements.txt
   python fetch_data.py --sample
   streamlit run app.py
   ```

2. **Weekly Usage:**
   ```bash
   python fetch_data.py  # Get latest data
   streamlit run app.py  # Start app
   ```

3. **In the App:**
   - Upload generated CSV files
   - Configure target price
   - Find blocks
   - Analyze results
   - Build lineups!

---

## File Sizes (Approximate)

```
app.py              ~19 KB   (main application)
fetch_data.py       ~8 KB    (data fetcher)
block_finder.py     ~13 KB   (analysis engine)
requirements.txt    <1 KB    (dependencies)
README.md           ~6 KB    (documentation)
QUICKSTART.md       ~2 KB    (quick guide)
```

---

## Need Help?

1. **Read QUICKSTART.md** - 5-minute setup guide
2. **Read README.md** - Full documentation
3. **Check app.py Guide tab** - In-app strategy guide
4. **Review fetch_data.py** - Data source info

---

## Want to Customize?

All files are yours to modify! Common customizations:

**app.py:**
- Change default target prices
- Modify correlation thresholds
- Add new metrics
- Customize charts

**block_finder.py:**
- Adjust scoring algorithms
- Add 3-player blocks
- Include different positions
- Change weighting

**fetch_data.py:**
- Add new data sources
- Include Vegas lines
- Pull injury reports
- Add ownership projections

---

**Ready to get started?** Open QUICKSTART.md and follow the steps! 🚀
