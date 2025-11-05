"""
DFS Data Fetcher
Fetches DraftKings pricing and NFL weekly stats from free sources
"""

import pandas as pd
import json
import argparse
from datetime import datetime
import sys

def fetch_draftkings_data():
    """
    Fetch DraftKings salaries using the unofficial API
    Returns DataFrame with player info and salaries
    """
    print("📥 Fetching DraftKings data...")
    
    try:
        from draft_kings.client import Client
        
        client = Client()
        
        # Get NFL contests
        contests = client.contests(sport='NFL')
        
        if not contests.contests:
            print("❌ No active NFL contests found")
            return None
        
        # Get the first main slate
        draft_group_id = None
        for contest in contests.contests:
            if 'Main' in contest.name or 'Sunday' in contest.name:
                draft_group_id = contest.draft_group_id
                break
        
        if not draft_group_id:
            draft_group_id = contests.contests[0].draft_group_id
        
        print(f"🎯 Using Draft Group ID: {draft_group_id}")
        
        # Get players for this draft group
        draftables = client.draft_group_players(draft_group_id)
        
        players_data = []
        for player in draftables.players:
            players_data.append({
                'Name': player.display_name,
                'Position': player.position,
                'Salary': player.salary,
                'Team': player.team_abbreviation,
                'Opponent': player.opponent_abbreviation if hasattr(player, 'opponent_abbreviation') else '',
                'Game': player.game_info.name if hasattr(player, 'game_info') else '',
                'DK_ID': player.player_id
            })
        
        df = pd.DataFrame(players_data)
        
        # Save to CSV
        filename = f"draftkings_salaries_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(filename, index=False)
        print(f"✅ Saved DraftKings data to {filename}")
        print(f"   Found {len(df)} players")
        
        return df
        
    except ImportError:
        print("❌ draft-kings package not installed")
        print("   Run: pip install draft-kings")
        return None
    except Exception as e:
        print(f"❌ Error fetching DraftKings data: {e}")
        return None

def fetch_nfl_stats(years=[2024], weeks=None):
    """
    Fetch NFL weekly stats using nfl_data_py
    Returns DataFrame with fantasy points and player stats
    """
    print("📥 Fetching NFL stats...")
    
    try:
        import nfl_data_py as nfl
        
        # Get weekly data
        weekly_data = nfl.import_weekly_data(
            years=years,
            columns=['player_id', 'player_name', 'recent_team', 'position', 
                    'week', 'season', 'fantasy_points', 'fantasy_points_ppr',
                    'passing_yards', 'passing_tds', 'rushing_yards', 
                    'rushing_tds', 'receptions', 'receiving_yards', 
                    'receiving_tds', 'targets']
        )
        
        # Filter to specified weeks if provided
        if weeks:
            weekly_data = weekly_data[weekly_data['week'].isin(weeks)]
        
        # Save to CSV
        filename = f"nfl_weekly_stats_{datetime.now().strftime('%Y%m%d')}.csv"
        weekly_data.to_csv(filename, index=False)
        print(f"✅ Saved NFL stats to {filename}")
        print(f"   Found {len(weekly_data)} player-week records")
        
        return weekly_data
        
    except ImportError:
        print("❌ nfl-data-py package not installed")
        print("   Run: pip install nfl-data-py")
        return None
    except Exception as e:
        print(f"❌ Error fetching NFL stats: {e}")
        return None

def generate_sample_data(platform='both'):
    """
    Generate sample data for testing
    """
    print("📝 Generating sample data...")
    
    # Generate for DraftKings
    if platform in ['draftkings', 'both']:
        dk_data = pd.DataFrame({
            'Name': [
                'Patrick Mahomes', 'Josh Allen', 'Christian McCaffrey', 'Tyreek Hill',
                'Travis Kelce', 'CeeDee Lamb', 'Trevor Lawrence', 'Parker Washington',
                'Justin Fields', 'DJ Moore', 'Caleb Williams', 'Rome Odunze',
                'Joe Burrow', 'Ja\'Marr Chase', 'Sam Howell', 'Terry McLaurin'
            ],
            'Position': [
                'QB', 'QB', 'RB', 'WR', 'TE', 'WR', 'QB', 'WR', 
                'QB', 'WR', 'QB', 'WR', 'QB', 'WR', 'QB', 'WR'
            ],
            'Salary': [
                8500, 8300, 10200, 8900, 7200, 8700, 6500, 3700,
                6300, 4200, 6800, 3400, 7900, 8500, 5800, 4100
            ],
            'Team': [
                'KC', 'BUF', 'SF', 'MIA', 'KC', 'DAL', 'JAX', 'JAX',
                'CHI', 'CHI', 'CHI', 'CHI', 'CIN', 'CIN', 'WAS', 'WAS'
            ],
            'Opponent': [
                'DEN', 'NYJ', 'TB', 'LV', 'DEN', 'PHI', 'MIN', 'MIN',
                'GB', 'GB', 'GB', 'GB', 'BAL', 'BAL', 'PHI', 'PHI'
            ]
        })
        
        dk_file = f"draftkings_salaries_sample.csv"
        dk_data.to_csv(dk_file, index=False)
        print(f"✅ Created {dk_file}")
    
    # Generate for FanDuel
    if platform in ['fanduel', 'both']:
        fd_data = pd.DataFrame({
            'Nickname': [  # FanDuel uses 'Nickname' instead of 'Name'
                'Patrick Mahomes', 'Josh Allen', 'Christian McCaffrey', 'Tyreek Hill',
                'Travis Kelce', 'CeeDee Lamb', 'Trevor Lawrence', 'Parker Washington',
                'Justin Fields', 'DJ Moore', 'Caleb Williams', 'Rome Odunze',
                'Joe Burrow', 'Ja\'Marr Chase', 'Sam Howell', 'Terry McLaurin'
            ],
            'Position': [
                'QB', 'QB', 'RB', 'WR', 'TE', 'WR', 'QB', 'WR',
                'QB', 'WR', 'QB', 'WR', 'QB', 'WR', 'QB', 'WR'
            ],
            'Salary': [  # FanDuel prices are typically higher
                9000, 8800, 10000, 8500, 7500, 8300, 7200, 4500,
                7000, 5000, 7300, 4200, 8400, 8100, 6500, 5200
            ],
            'Team': [
                'KC', 'BUF', 'SF', 'MIA', 'KC', 'DAL', 'JAX', 'JAX',
                'CHI', 'CHI', 'CHI', 'CHI', 'CIN', 'CIN', 'WAS', 'WAS'
            ],
            'Opponent': [
                'DEN', 'NYJ', 'TB', 'LV', 'DEN', 'PHI', 'MIN', 'MIN',
                'GB', 'GB', 'GB', 'GB', 'BAL', 'BAL', 'PHI', 'PHI'
            ],
            'FPPG': [  # FanDuel includes average fantasy points
                23.5, 24.1, 22.8, 19.3, 14.2, 18.7, 19.8, 8.5,
                18.3, 13.2, 17.9, 9.1, 21.2, 20.4, 16.8, 14.1
            ]
        })
        
        fd_file = f"fanduel_salaries_sample.csv"
        fd_data.to_csv(fd_file, index=False)
        print(f"✅ Created {fd_file}")
    
    # Sample weekly stats (last 6 weeks) - same for both platforms
    # Use whichever dataset we generated
    if platform in ['draftkings', 'both']:
        player_source = dk_data
    else:
        player_source = fd_data
        # Convert Nickname to Name for consistency
        player_source = player_source.rename(columns={'Nickname': 'Name'})
    
    stats_data = []
    for player in player_source['Name']:
        team = player_source[player_source['Name'] == player]['Team'].values[0]
        pos = player_source[player_source['Name'] == player]['Position'].values[0]
        
        # Generate realistic fantasy points
        if pos == 'QB':
            base_pts = 22
            variance = 8
        elif pos == 'RB':
            base_pts = 18
            variance = 10
        elif pos == 'WR':
            base_pts = 15
            variance = 7
        else:  # TE
            base_pts = 12
            variance = 6
        
        for week in range(5, 11):
            pts = base_pts + (variance * (hash(player + str(week)) % 100 - 50) / 50)
            pts = max(5, pts)  # Floor of 5 points
            
            stats_data.append({
                'player_name': player,
                'recent_team': team,
                'position': pos,
                'week': week,
                'season': 2024,
                'fantasy_points_ppr': round(pts, 1)
            })
    
    stats_df = pd.DataFrame(stats_data)
    
    # Save stats file
    stats_file = f"nfl_weekly_stats_sample.csv"
    stats_df.to_csv(stats_file, index=False)
    print(f"✅ Created {stats_file}")
    
    # Return the data
    if platform == 'draftkings':
        return dk_data, stats_df
    elif platform == 'fanduel':
        return fd_data, stats_df
    else:  # both
        return (dk_data, fd_data), stats_df

def main():
    parser = argparse.ArgumentParser(description='Fetch DFS data from free sources')
    parser.add_argument('--platform', type=str, default='draftkings',
                       choices=['draftkings', 'fanduel', 'both'],
                       help='Which platform to fetch data for')
    parser.add_argument('--week', type=str, default='current', 
                       help='Week to fetch (current or specific week number)')
    parser.add_argument('--sample', action='store_true',
                       help='Generate sample data instead of fetching live')
    parser.add_argument('--dk-only', action='store_true',
                       help='Only fetch DraftKings data')
    parser.add_argument('--stats-only', action='store_true',
                       help='Only fetch NFL stats')
    
    args = parser.parse_args()
    
    print("\n" + "="*50)
    print("🏈 DFS DATA FETCHER")
    print("="*50 + "\n")
    
    if args.sample:
        generate_sample_data(args.platform if not args.dk_only else 'draftkings')
        print("\n✅ Sample data generated!")
        print("\n📁 Files created:")
        if args.platform in ['draftkings', 'both'] or args.dk_only:
            print("   - draftkings_salaries_sample.csv")
        if args.platform in ['fanduel', 'both'] and not args.dk_only:
            print("   - fanduel_salaries_sample.csv")
        print("   - nfl_weekly_stats_sample.csv")
        return
    
    # Fetch live data
    if not args.stats_only:
        dk_df = fetch_draftkings_data()
        if dk_df is None:
            print("\n⚠️  Using sample data instead...")
            generate_sample_data()
            return
    
    if not args.dk_only:
        stats_df = fetch_nfl_stats(years=[2024])
        if stats_df is None:
            print("\n⚠️  Using sample data instead...")
            generate_sample_data()
            return
    
    print("\n" + "="*50)
    print("✅ DATA FETCH COMPLETE")
    print("="*50)
    print("\n📁 Files ready to upload to Streamlit app")
    print("\n🚀 Next steps:")
    print("   1. Run: streamlit run app.py")
    print("   2. Upload the generated CSV files")
    print("   3. Find player blocks!")

if __name__ == "__main__":
    main()
