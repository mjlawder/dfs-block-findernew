# 🎯 START HERE - Your DFS Block Finder is Ready!

## ✅ What You Got

A complete web application that finds correlated NFL DFS player blocks (like Trevor Lawrence + Parker Washington) that match expensive studs' pricing with elite tournament upside.

**Supports both DraftKings AND FanDuel!** 🎮

---

## 🚀 3 Steps to Get Running

### Step 1: Install Python Packages
Open terminal/command prompt in this folder and run:
```bash
pip install -r requirements.txt
```

### Step 2: Generate Test Data  
```bash
python fetch_data.py --sample --platform both
```

This creates sample data for both DraftKings and FanDuel!

### Step 3: Start the App
```bash
streamlit run app.py
```

**That's it!** Your browser will open to http://localhost:8501

---

## 📖 Which File to Read?

**New to this?** → Read `QUICKSTART.md`

**Want full details?** → Read `README.md`  

**Want to understand the files?** → Read `FILE_GUIDE.md`

**Windows user?** → Double-click `START_APP.bat`

---

## 🎮 What You Can Do

✅ Find QB+WR combos that match CMC's price  
✅ Analyze 6 weeks of game logs  
✅ See correlation between players  
✅ Compare ceiling/floor to studs  
✅ Visualize week-by-week performance  
✅ Export blocks to CSV  

---

## 💡 Quick Tips

**Best Blocks Have:**
- 0.75+ correlation
- 40+ point ceiling  
- Same team (QB + WR)
- High Vegas game total
- Recent injury to WR1 (more targets!)

**Avoid:**
- Blocks from different teams
- Low correlation (<0.60)
- Players with <4 weeks data
- Blocks way off target price

---

## 🔥 Real Example from JM

**Week 9 Discovery:**
```
Trevor Lawrence ($6,500) + Parker Washington ($3,700) = $10,200
vs
Christian McCaffrey ($10,200)

Game Logs (combined):
Week 4: 46.9 pts
Week 5: 38.5 pts
Week 6: 28.0 pts
Week 7: 38.2 pts
Week 8: 35.3 pts
Week 9: 38.4 pts

Correlation: 0.82
Ceiling: 46.9 (better than CMC!)
Result: 5th place, $1,000 prize
```

**This tool finds these opportunities automatically!**

---

## 📊 Sample Data Included

The sample data includes realistic Week 5-10 fantasy scores for:
- Top QBs (Mahomes, Allen, Lawrence, etc.)
- Elite WRs (Hill, Chase, Lamb, etc.) 
- Star RBs (CMC)
- Emerging combos (Lawrence+Washington, Fields+Moore)

Perfect for learning the tool before using real data!

---

## 🎯 Your Next Steps

1. ✅ Install packages (`pip install -r requirements.txt`)
2. ✅ Generate data (`python fetch_data.py --sample --platform both`)
3. ✅ Run app (`streamlit run app.py`)
4. ✅ In app: **Select DraftKings or FanDuel** in sidebar
5. ✅ Choose "Use Sample Data"
6. ✅ Click "Find Player Blocks"  
7. ✅ Explore the results!
8. ⭐ When ready, upload live CSVs from your platform

---

## 🆘 Having Issues?

**Error: "streamlit: command not found"**
```bash
pip install streamlit
```

**Error: "ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

**Port already in use?**
```bash
streamlit run app.py --server.port 8502
```

**Need more help?**
Check the **troubleshooting section** in README.md

---

## 🌟 Features You'll Love

**Find Blocks Tab:**
- Scan thousands of combinations instantly
- Filter by team, position, price
- Sort by ceiling, correlation, value

**Block Analysis Tab:**  
- Ceiling/floor distributions
- Correlation heatmaps
- Value per $1K metrics

**Game Logs Tab:**
- Week-by-week performance charts
- Compare blocks to studs
- Identify trends

**Guide Tab:**
- Complete strategy guide
- Tips from JM's approach
- Advanced stacking techniques

---

## 💰 Why This Works

**The Math:**
- Stud RB: $10,200 → ~27 points avg, 42 ceiling
- QB+WR Block: $10,200 → ~35 points avg, 47 ceiling  
- Same price, MORE upside!

**The Edge:**
- Correlation: When QB scores, WR scores too
- Leverage: Less ownership than studs
- Opportunity: Injuries create value
- Differentiation: Win tournaments by being different

---

## 🚀 Ready? Here's Your Command

```bash
# Run these 3 commands:
pip install -r requirements.txt
python fetch_data.py --sample
streamlit run app.py
```

**Then check your browser at http://localhost:8501**

---

## 📞 Questions?

All documentation is included:
- QUICKSTART.md - Fast setup
- README.md - Complete guide  
- FILE_GUIDE.md - File explanations
- In-app Guide tab - Strategy tips

---

**Let's find those tournament-winning blocks! 🏆**

*Built based on JM's successful strategy that won $1,000 in Week 9*
