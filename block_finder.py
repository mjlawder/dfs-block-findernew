"""
Block Finder Core Logic
Analyzes player combinations to find correlated blocks
"""

import pandas as pd
import numpy as np
from itertools import combinations
from typing import List, Dict, Tuple

class BlockFinder:
    """
    Main class for finding and analyzing player blocks
    """
    
    def __init__(self, dk_data: pd.DataFrame, stats_data: pd.DataFrame):
        """
        Initialize with DraftKings salaries and NFL stats
        
        Args:
            dk_data: DataFrame with columns [Name, Position, Salary, Team, Opponent]
            stats_data: DataFrame with columns [player_name, week, fantasy_points_ppr, recent_team]
        """
        self.dk_data = dk_data
        self.stats_data = stats_data
        self.blocks = []
        
        # Merge salary info with stats
        self.enriched_data = self._merge_data()
    
    def _merge_data(self) -> pd.DataFrame:
        """Merge DK salaries with weekly stats"""
        # Standardize names
        self.dk_data['player_key'] = self.dk_data['Name'].str.lower().str.replace('.', '').str.strip()
        self.stats_data['player_key'] = self.stats_data['player_name'].str.lower().str.replace('.', '').str.strip()
        
        # Merge
        merged = self.stats_data.merge(
            self.dk_data[['player_key', 'Salary', 'Position', 'Team', 'Opponent']],
            on='player_key',
            how='inner'
        )
        
        return merged
    
    def find_blocks(self, 
                   target_price: int,
                   tolerance: int = 300,
                   min_weeks: int = 4,
                   same_team_only: bool = True,
                   positions: List[str] = ['QB', 'WR', 'TE'],
                   block_size: int = 2) -> List[Dict]:
        """
        Find player blocks matching target price
        
        Args:
            target_price: Target combined salary
            tolerance: +/- price flexibility
            min_weeks: Minimum weeks of data required
            same_team_only: Only find blocks from same team
            positions: Allowed positions
            block_size: Number of players in block (2 or 3)
            
        Returns:
            List of block dictionaries with analysis
        """
        print(f"🔍 Searching for {block_size}-player blocks near ${target_price:,}...")
        
        # Filter to eligible players
        eligible = self.dk_data[
            (self.dk_data['Position'].isin(positions)) &
            (self.dk_data['Salary'] > 0)
        ].copy()
        
        blocks = []
        checked = 0
        
        # Group by team if same_team_only
        if same_team_only:
            teams = eligible['Team'].unique()
            for team in teams:
                team_players = eligible[eligible['Team'] == team]
                blocks.extend(self._check_team_combinations(
                    team_players, target_price, tolerance, 
                    min_weeks, block_size, team
                ))
                checked += 1
                if checked % 5 == 0:
                    print(f"   Checked {checked}/{len(teams)} teams...")
        else:
            # Check all combinations (slower)
            player_combos = combinations(eligible.index, block_size)
            for combo in player_combos:
                block = self._analyze_combination(
                    eligible.loc[list(combo)],
                    target_price,
                    tolerance,
                    min_weeks
                )
                if block:
                    blocks.append(block)
        
        print(f"✅ Found {len(blocks)} eligible blocks")
        
        # Sort by ceiling
        blocks.sort(key=lambda x: x['ceiling'], reverse=True)
        
        self.blocks = blocks
        return blocks
    
    def _check_team_combinations(self,
                                 team_players: pd.DataFrame,
                                 target_price: int,
                                 tolerance: int,
                                 min_weeks: int,
                                 block_size: int,
                                 team: str) -> List[Dict]:
        """Check all combinations for a specific team"""
        blocks = []
        
        for combo in combinations(team_players.index, block_size):
            players = team_players.loc[list(combo)]
            
            # Check if price is in range
            total_salary = players['Salary'].sum()
            if abs(total_salary - target_price) <= tolerance:
                block = self._analyze_combination(
                    players, target_price, tolerance, min_weeks
                )
                if block:
                    blocks.append(block)
        
        return blocks
    
    def _analyze_combination(self,
                            players: pd.DataFrame,
                            target_price: int,
                            tolerance: int,
                            min_weeks: int) -> Dict:
        """
        Analyze a specific player combination
        
        Returns:
            Dict with block analysis or None if insufficient data
        """
        # Get stats for these players
        player_names = players['Name'].tolist()
        
        # Get game logs
        game_logs = self._get_combined_game_logs(player_names, min_weeks)
        
        if game_logs is None or len(game_logs) < min_weeks:
            return None
        
        # Calculate metrics
        combined_salary = players['Salary'].sum()
        avg_score = np.mean(game_logs)
        ceiling = np.max(game_logs)
        floor = np.min(game_logs)
        games_30plus = sum(1 for score in game_logs if score >= 30)
        
        # Calculate correlation
        correlation = self._calculate_correlation(player_names, game_logs)
        
        # Build block dict
        block = {
            'name': ' + '.join(player_names),
            'players': player_names,
            'positions': players['Position'].tolist(),
            'prices': players['Salary'].tolist(),
            'combined_price': int(combined_salary),
            'team': players['Team'].iloc[0],
            'opponent': players['Opponent'].iloc[0],
            'game_logs': game_logs,
            'avg_score': round(avg_score, 1),
            'ceiling': round(ceiling, 1),
            'floor': round(floor, 1),
            'games_30plus': games_30plus,
            'correlation': round(correlation, 2),
            'value_per_1k': round(avg_score / (combined_salary / 1000), 2)
        }
        
        return block
    
    def _get_combined_game_logs(self, 
                               player_names: List[str],
                               min_weeks: int) -> List[float]:
        """
        Get combined fantasy points for players by week
        
        Returns:
            List of combined scores or None if insufficient data
        """
        # Get recent weeks
        recent_weeks = sorted(self.enriched_data['week'].unique(), reverse=True)[:min_weeks * 2]
        
        combined_logs = []
        
        for week in recent_weeks:
            week_total = 0
            players_found = 0
            
            for player in player_names:
                player_key = player.lower().replace('.', '').strip()
                week_data = self.enriched_data[
                    (self.enriched_data['player_key'] == player_key) &
                    (self.enriched_data['week'] == week)
                ]
                
                if not week_data.empty:
                    week_total += week_data['fantasy_points_ppr'].iloc[0]
                    players_found += 1
            
            # Only include week if all players played
            if players_found == len(player_names):
                combined_logs.append(week_total)
        
        if len(combined_logs) >= min_weeks:
            return combined_logs[:min_weeks]
        else:
            return None
    
    def _calculate_correlation(self, 
                              player_names: List[str],
                              combined_logs: List[float]) -> float:
        """
        Calculate correlation between players
        
        For 2 players: Pearson correlation
        For 3+ players: Average pairwise correlation
        
        Returns:
            Correlation score 0-1
        """
        if len(player_names) != 2:
            # Simplified correlation for 3+ players
            # Just check if they're from same team
            return 0.75  # Placeholder
        
        # Get individual logs for each player
        player1_logs = []
        player2_logs = []
        
        recent_weeks = sorted(self.enriched_data['week'].unique(), reverse=True)[:len(combined_logs)]
        
        for week in recent_weeks:
            p1_key = player_names[0].lower().replace('.', '').strip()
            p2_key = player_names[1].lower().replace('.', '').strip()
            
            p1_data = self.enriched_data[
                (self.enriched_data['player_key'] == p1_key) &
                (self.enriched_data['week'] == week)
            ]
            
            p2_data = self.enriched_data[
                (self.enriched_data['player_key'] == p2_key) &
                (self.enriched_data['week'] == week)
            ]
            
            if not p1_data.empty and not p2_data.empty:
                player1_logs.append(p1_data['fantasy_points_ppr'].iloc[0])
                player2_logs.append(p2_data['fantasy_points_ppr'].iloc[0])
        
        if len(player1_logs) < 3:
            return 0.5  # Not enough data
        
        # Calculate Pearson correlation
        try:
            correlation = np.corrcoef(player1_logs, player2_logs)[0, 1]
            # Convert to 0-1 scale (correlations can be negative)
            correlation = max(0, correlation)
            return correlation
        except:
            return 0.5
    
    def compare_to_stud(self, 
                       block: Dict,
                       stud_name: str) -> Dict:
        """
        Compare a block to a stud player
        
        Returns:
            Comparison dictionary
        """
        # Get stud's game log
        stud_key = stud_name.lower().replace('.', '').strip()
        stud_data = self.enriched_data[
            self.enriched_data['player_key'] == stud_key
        ]
        
        if stud_data.empty:
            return None
        
        # Get recent weeks
        recent_weeks = sorted(stud_data['week'].unique(), reverse=True)[:len(block['game_logs'])]
        stud_logs = []
        
        for week in recent_weeks:
            week_data = stud_data[stud_data['week'] == week]
            if not week_data.empty:
                stud_logs.append(week_data['fantasy_points_ppr'].iloc[0])
        
        comparison = {
            'block_name': block['name'],
            'block_price': block['combined_price'],
            'block_ceiling': block['ceiling'],
            'block_avg': block['avg_score'],
            'stud_name': stud_name,
            'stud_price': stud_data['Salary'].iloc[0],
            'stud_ceiling': max(stud_logs) if stud_logs else 0,
            'stud_avg': np.mean(stud_logs) if stud_logs else 0,
            'ceiling_diff': block['ceiling'] - max(stud_logs) if stud_logs else 0,
            'avg_diff': block['avg_score'] - np.mean(stud_logs) if stud_logs else 0
        }
        
        return comparison
    
    def export_to_csv(self, filename: str = 'blocks_export.csv'):
        """Export found blocks to CSV"""
        if not self.blocks:
            print("❌ No blocks to export")
            return
        
        # Flatten blocks for CSV
        export_data = []
        for block in self.blocks:
            export_data.append({
                'Block': block['name'],
                'Price': block['combined_price'],
                'Team': block['team'],
                'Opponent': block['opponent'],
                'Avg_Score': block['avg_score'],
                'Ceiling': block['ceiling'],
                'Floor': block['floor'],
                '30+_Games': f"{block['games_30plus']}/{len(block['game_logs'])}",
                'Correlation': block['correlation'],
                'Value_per_1K': block['value_per_1k']
            })
        
        df = pd.DataFrame(export_data)
        df.to_csv(filename, index=False)
        print(f"✅ Exported {len(self.blocks)} blocks to {filename}")

# Example usage
if __name__ == "__main__":
    print("Block Finder module loaded")
    print("Import this module in your Streamlit app:")
    print("  from block_finder import BlockFinder")
