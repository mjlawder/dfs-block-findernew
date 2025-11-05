# 🏈 NFL DFS Player Block Finder (DraftKings & FanDuel)

Find correlated player combinations that match expensive studs' pricing with elite tournament upside on both DraftKings and FanDuel.

## What Is This?

This tool helps you discover **player blocks** - groups of 2-3 correlated players whose combined DFS salary equals an expensive stud, but with similar or better ceiling potential.

**Works with both DraftKings and FanDuel!**

### The Original Strategy

Inspired by JM's discovery:
- **Trevor Lawrence ($6,500) + Parker Washington ($3,700) = $10,200**
- Same price as Christian McCaffrey ($10,200)
- Similar ceiling scores (40-50 points)
- High correlation (QB+WR score together)
- Travis Hunter out → More targets for Washington

Result: This combo helped win 5th place ($1,000) in a 2000-player tournament!

## Features

✅ **Automatic Block Detection** - Scans thousands of player combinations  
✅ **Correlation Analysis** - Identifies which players score together  
✅ **Game Log Visualization** - See week-by-week performance  
✅ **Ceiling/Floor Metrics** - Evaluate tournament upside  
✅ **Free Data Sources** - No paid APIs required  
✅ **Interactive Web App** - Easy-to-use Streamlit interface  

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download this repository**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Generate sample data** (for testing)
```bash
python fetch_data.py --sample
```

4. **Run the app**
```bash
streamlit run app.py
```

5. **Open your browser** to http://localhost:8501

## Usage

### Quick Start

1. **Upload Data**
   - Run `python fetch_data.py --sample` to create test files
   - Or upload your own DraftKings CSV and stats CSV

2. **Configure Settings**
   - Target Price: Price of stud you want to match ($10,200)
   - Price Tolerance: How much flexibility ($200-300)
   - Weeks to Analyze: Recent weeks to include (4-6)

3. **Find Blocks**
   - Click "Find Player Blocks"
   - Review results sorted by ceiling

4. **Analyze**
   - View game logs for each block
   - Check correlation scores
   - Compare to stud alternatives

### Getting Live Data

#### Option 1: Manual Upload
1. Export CSV from DraftKings or FanDuel lobby
   - **DraftKings**: Contest lobby → Export Players
   - **FanDuel**: Any contest → Download Players
2. Run `python fetch_data.py` to get NFL stats
3. Upload both files to the app

#### Option 2: Automatic Fetch
```bash
# Generate sample data for both platforms
python fetch_data.py --sample --platform both

# DraftKings only (uses API)
python fetch_data.py --platform draftkings

# FanDuel only (manual CSV required)
python fetch_data.py --platform fanduel --stats-only

# Current week's stats only
python fetch_data.py --stats-only
```

## Data Sources (All Free!)

### 1. DraftKings Pricing
- **Source**: Unofficial public API
- **What**: Player salaries, positions, teams
- **Update**: Weekly when slates release
- **Package**: `draft-kings` (Python)

### 2. FanDuel Pricing
- **Source**: CSV export from FanDuel lobby
- **What**: Player salaries, positions, teams
- **Update**: Weekly when slates release
- **How**: Download from any FanDuel contest page

### 3. NFL Fantasy Stats
- **Source**: nflfastR via nfl_data_py
- **What**: Weekly fantasy points, player stats
- **History**: Back to 1999
- **Package**: `nfl-data-py` (Python)

### 4. Game Info
- **Source**: ESPN/NFL public APIs
- **What**: Schedules, rosters, matchups
- **Update**: Real-time during season

## Understanding the Metrics

### Correlation (0.0 - 1.0)
How often players score together:
- **0.8+** = Excellent (QB + WR1)
- **0.7-0.8** = Good (QB + WR2)
- **0.6-0.7** = Acceptable (QB + TE)
- **<0.6** = Weak

### Ceiling
Best performance in recent weeks. Target 40+ for GPPs.

### Floor
Worst performance. Lower floors OK if ceiling is elite.

### 30+ Rate
Percentage of games with 30+ points. Target 50%+.

### Value per 1K
Points per $1,000 spent. Average is ~2.5-3.0.

## Strategy Tips

### ✅ DO
- Target teams with high Vegas totals (45+ points)
- Look for WR injuries (more targets for backup)
- Stack QB+WR from same team
- Use blocks in 10-20% of lineups (diversify!)
- Check matchup context

### ❌ DON'T
- Ignore game environment
- Use low-correlation blocks
- Put all lineups on one block
- Forget about ownership leverage

## Advanced Techniques

### Bring-Back Stacks
Pair your block with opposing receiver:
```
Lawrence + Washington (JAX)
    +
Justin Jefferson (MIN)
```
Captures shootout potential.

### Game Stacks
Multiple blocks from same game:
```
Lawrence + Washington (JAX)
    +
Cousins + Hockenson (MIN)
```

### Leverage News
React to:
- Injury reports
- Weather updates  
- Beat writer intel
- Vegas line moves

## Project Structure

```
dfs_app/
├── app.py              # Main Streamlit application
├── fetch_data.py       # Data fetching script
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── block_finder.py    # Core analysis logic (coming soon)
```

## Roadmap

- [x] Basic block finder
- [x] Correlation analysis
- [x] Game log visualization
- [ ] 3-player blocks (QB+WR1+WR2)
- [ ] Historical win rate tracking
- [ ] Ownership projection integration
- [ ] Lineup optimizer
- [ ] CSV export for lineups
- [ ] Mobile-responsive design

## FAQ

**Q: Is this legal?**  
A: Yes! Using public data for analysis is legal.

**Q: Does this guarantee wins?**  
A: No. DFS has variance. This increases your edge but doesn't eliminate risk.

**Q: How often should I use blocks?**  
A: Mix them in 10-30% of GPP lineups. Diversify!

**Q: What about cash games?**  
A: Blocks work better for GPPs. For cash, use consistent studs.

**Q: Can I deploy this online?**  
A: Yes! Deploy to Streamlit Cloud, Heroku, or Render.com.

## Deployment

### Streamlit Cloud (Free)
1. Push code to GitHub
2. Go to streamlit.io/cloud
3. Connect your repo
4. Deploy!

### Local Network
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Docker
```bash
docker build -t dfs-block-finder .
docker run -p 8501:8501 dfs-block-finder
```

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "No DraftKings data"
- Run `python fetch_data.py --sample` for test data
- Or check if slates are active on DraftKings

### "Connection refused"
- Make sure Streamlit is running
- Check firewall settings
- Try http://localhost:8501

## Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use and modify!

## Credits

- **JM** - Original strategy discovery
- **nflfastR team** - Free NFL data
- **DraftKings** - Public API access
- **You** - For using this tool!

## Support

Found a bug? Have ideas? Open an issue!

---

**Good luck and may your blocks hit their ceiling! 🚀**
