# 🎮 DraftKings vs FanDuel - Platform Guide

Both platforms are now fully supported! Here's what you need to know:

## Key Differences

### Salary Structure
| Feature | DraftKings | FanDuel |
|---------|-----------|---------|
| **Salary Cap** | $50,000 | $60,000 |
| **Typical Stud Price** | $9K-$11K | $9.5K-$11K |
| **Price Range** | $3K-$11K | $4K-$11K |
| **Flexibility** | More value plays | Higher baseline prices |

### Scoring System
| Stat | DraftKings | FanDuel |
|------|-----------|---------|
| **Pass TD** | 4 pts | 4 pts |
| **Pass Yard** | 0.04 pts (25 yds = 1 pt) | 0.04 pts (25 yds = 1 pt) |
| **Rush/Rec TD** | 6 pts | 6 pts |
| **Rush/Rec Yard** | 0.1 pts | 0.1 pts |
| **Reception** | 1 pt (PPR) | 0.5 pt (Half PPR) |
| **300-yd Bonus** | 3 pts | 3 pts |
| **100-yd Bonus** | None | None |

**Key Difference**: DraftKings is full PPR, FanDuel is half PPR. This makes pass-catching RBs and target-heavy WRs slightly less valuable on FanDuel.

## Which Platform is Better for Blocks?

### DraftKings Advantages ✅
- **More pricing discrepancies**: Wider price ranges = more arbitrage opportunities
- **Full PPR scoring**: Makes WR blocks more viable
- **Easier data access**: Unofficial API available
- **More value plays**: $3K players can provide value

### FanDuel Advantages ✅
- **Higher salary cap**: More room for multiple blocks
- **Consistent pricing**: Less week-to-week volatility
- **Half PPR**: Rewards TD-dependent players (good for QB stacks)
- **Simpler scoring**: Fewer obscure bonuses

## Strategy Adjustments

### For DraftKings
- **Target**: $9,000-$11,000 blocks
- **Focus**: High-reception WRs (full PPR!)
- **Tolerance**: $200-$300 (tight pricing)
- **Stack with**: Pass-catching RBs

### For FanDuel
- **Target**: $10,000-$12,000 blocks
- **Focus**: TD-upside WRs (half PPR means TDs matter more)
- **Tolerance**: $300-$500 (more flexibility)
- **Stack with**: High-yardage players

## Example Blocks Comparison

### Same Block, Different Platforms

**Trevor Lawrence + Parker Washington**

| Platform | Lawrence Price | Washington Price | Combined | Value |
|----------|---------------|------------------|----------|-------|
| DraftKings | $6,500 | $3,700 | $10,200 | Great! |
| FanDuel | $7,200 | $4,500 | $11,700 | Good |

**Key Insight**: The block works on both platforms, but DK pricing is tighter while FD has more salary cap room.

## How to Use the App

1. **Select Your Platform**
   - Top of sidebar: Choose DraftKings or FanDuel
   - Defaults adjust automatically (price ranges, salary cap)

2. **Upload Platform-Specific Data**
   - DraftKings CSV: Column names = Name, Salary, Position
   - FanDuel CSV: Column names = Nickname, Salary, Position
   - NFL Stats: Same file works for both!

3. **Configure Your Search**
   - DK users: Target around $10K with $200 tolerance
   - FD users: Target around $11K with $400 tolerance

4. **Analyze Results**
   - All analysis features work identically
   - Correlation scores apply to both platforms
   - Game logs are platform-agnostic

## Getting Data for Each Platform

### DraftKings
```bash
# Automatic (uses unofficial API)
python fetch_data.py --platform draftkings

# Or manual
# 1. Go to DK contest lobby
# 2. Click "Export Players"
# 3. Upload CSV to app
```

### FanDuel
```bash
# Generate sample data
python fetch_data.py --sample --platform fanduel

# For live data (manual)
# 1. Open any FD contest
# 2. Click "Download" button
# 3. Upload CSV to app
```

### Both at Once
```bash
python fetch_data.py --sample --platform both
```

This creates:
- `draftkings_salaries_sample.csv`
- `fanduel_salaries_sample.csv`
- `nfl_weekly_stats_sample.csv`

## Pro Tips

### Multi-Platform Strategy
1. **Run blocks on both sites**
   - Same blocks often work on DK and FD
   - Diversify your exposure

2. **Leverage pricing differences**
   - If a player is cheaper on one platform, use them there
   - Build platform-specific lineups

3. **Ownership arbitrage**
   - DK players may not play FD and vice versa
   - Be contrarian across platforms

### Platform-Specific Blocks

**Better for DraftKings:**
- RB+WR combos (RB catches passes = full PPR value)
- Target hog WRs (high reception totals)
- 3-player blocks (more salary flexibility)

**Better for FanDuel:**
- QB+WR combos (TDs matter more in half PPR)
- Big-play WRs (home run TDs)
- 2-player blocks (pricing is tighter)

## Sample Data Included

The app includes sample data for both platforms:
- Realistic pricing based on typical platform differences
- Same player game logs (scoring is similar enough)
- All features work identically

## FAQs

**Q: Can I use the same blocks on both platforms?**
A: Yes! The game logs and correlations are identical. Just adjust for different pricing.

**Q: Which platform is better for tournaments?**
A: Both are great. DK has more entries, FD has bigger prizes. Use both!

**Q: Do I need separate accounts?**
A: This tool works independently of your accounts. Just upload the CSV files.

**Q: Will pricing always be ~15-20% higher on FD?**
A: Generally yes, but it varies by player. Always check actual prices.

**Q: Can I switch platforms mid-season?**
A: Absolutely! Your block-finding strategy works on both.

---

**Bottom Line**: This tool works seamlessly on both DraftKings and FanDuel. The core strategy of finding correlated blocks is platform-agnostic. Pick whichever platform you prefer, or use both for maximum edge! 🚀
