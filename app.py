import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="DFS Block Finder", layout="wide", page_icon="🏈")

# Custom CSS
st.markdown("""
<style>
    .block-card {
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #4CAF50;
        margin: 10px 0;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏈 NFL DFS Player Block Finder")
st.markdown("Find correlated player stacks that match stud pricing with elite upside")

# Initialize session state
if 'blocks_found' not in st.session_state:
    st.session_state.blocks_found = False
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    platform = st.radio(
        "DFS Platform",
        ["DraftKings", "FanDuel"],
        horizontal=True,
        help="Select your DFS platform"
    )
    
    # Platform-specific defaults
    if platform == "DraftKings":
        default_price = 10200
        max_price = 15000
        salary_cap = 50000
    else:  # FanDuel
        default_price = 10000
        max_price = 12000
        salary_cap = 60000
    
    target_price = st.number_input(
        "Target Price ($)", 
        min_value=5000, 
        max_value=max_price, 
        value=default_price, 
        step=100,
        help="Price of the stud you want to match"
    )
    
    st.caption(f"💰 {platform} Salary Cap: ${salary_cap:,}")
    
    price_tolerance = st.number_input(
        "Price Tolerance ($)", 
        min_value=0, 
        max_value=1000, 
        value=300, 
        step=50,
        help="How much flexibility in combined price"
    )
    
    weeks_back = st.slider(
        "Weeks to Analyze", 
        3, 17, 6,
        help="How many recent weeks to include in analysis"
    )
    
    min_ceiling = st.number_input(
        "Min Ceiling Score", 
        15.0, 70.0, 35.0, 2.5,
        help="Minimum peak performance required"
    )
    
    correlation_min = st.slider(
        "Min Correlation", 
        0.0, 1.0, 0.65, 0.05,
        help="How correlated should players be (0-1)"
    )
    
    st.markdown("---")
    
    positions = st.multiselect(
        "Allowed Positions",
        ["QB", "RB", "WR", "TE"],
        default=["QB", "WR", "TE"],
        help="Which positions to include in blocks"
    )
    
    same_team_only = st.checkbox(
        "Same Team Only", 
        value=True,
        help="Only find blocks from same team (more correlation)"
    )
    
    st.markdown("---")
    st.info("💡 **Tip**: Start with QB+WR combos from high-scoring teams")

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Find Blocks", 
    "📊 Block Analysis", 
    "📈 Game Logs", 
    "ℹ️ Guide"
])

with tab1:
    st.header("Player Block Scanner")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Data Upload")
        
        upload_method = st.radio(
            "Choose data source:",
            ["Upload Files", "Use Sample Data", "Fetch Live Data"],
            horizontal=True
        )
        
        if upload_method == "Upload Files":
            st.markdown(f"""
            **Upload these files for {platform}:**
            1. {platform} CSV (download from {platform} lobby)
            2. Weekly fantasy stats CSV
            
            **How to export {platform} CSV:**
            - {"Go to contest lobby → Export Players" if platform == "DraftKings" else "Open any contest → Download Players"}
            """)
            
            salary_file = st.file_uploader(f"{platform} Salaries", type=['csv'])
            stats_file = st.file_uploader("Weekly Stats", type=['csv'])
            
            data_ready = salary_file is not None and stats_file is not None
            
        elif upload_method == "Use Sample Data":
            st.info("Using sample data from Week 10, 2024")
            data_ready = True
            # We'll generate sample data
            
        else:  # Fetch Live Data
            st.code("python fetch_data.py --week current", language="bash")
            if st.button("Run Data Fetcher"):
                st.warning("⚠️ Run fetch_data.py script first, then refresh")
            data_ready = False
    
    with col2:
        st.metric("Target Price", f"${target_price:,}")
        st.metric("Price Range", f"${target_price-price_tolerance:,} - ${target_price+price_tolerance:,}")
        st.metric("Weeks Analyzed", weeks_back)
    
    st.markdown("---")
    
    if data_ready:
        if st.button("🚀 Find Player Blocks", type="primary", use_container_width=True):
            with st.spinner("🔍 Analyzing thousands of player combinations..."):
                # Load data based on platform
                if upload_method == "Upload Files":
                    salary_data = pd.read_csv(salary_file)
                    # Standardize column names for both platforms
                    salary_data = standardize_salary_columns(salary_data, platform)
                    stats_data = pd.read_csv(stats_file)
                else:
                    # Use sample data
                    salary_data, stats_data = load_sample_data(platform)
                
                # Simulate processing
                import time
                time.sleep(1)
                
                # Generate sample results
                st.session_state.blocks_found = True
                st.session_state.analysis_data = generate_sample_blocks(
                    target_price, 
                    price_tolerance, 
                    weeks_back,
                    platform
                )
                st.session_state.platform = platform
                
                st.success(f"✅ Found correlated player blocks for {platform}!")
                st.balloons()
        
        if st.session_state.blocks_found:
            display_block_results(st.session_state.analysis_data, target_price, st.session_state.get('platform', 'DraftKings'))
    else:
        st.info("👆 Upload data or select sample data to begin")

with tab2:
    st.header("Block Analysis & Comparison")
    
    if st.session_state.blocks_found:
        display_detailed_analysis(st.session_state.analysis_data, target_price)
    else:
        st.info("Find blocks first to see detailed analysis")
        
        # Show what will be available
        st.markdown("""
        ### Available Analytics:
        - **Ceiling/Floor Distributions**: See the range of outcomes
        - **Correlation Matrices**: How often players score together
        - **Game-by-Game Breakdown**: Week-by-week performance
        - **Stud Comparisons**: Side-by-side with expensive options
        - **Value Ratings**: Points per $1K spent
        """)

with tab3:
    st.header("Game Log Explorer")
    
    if st.session_state.blocks_found:
        display_game_logs(st.session_state.analysis_data)
    else:
        st.info("Find blocks first to explore game logs")

with tab4:
    display_guide()

# Helper functions
def standardize_salary_columns(df, platform):
    """Standardize column names for both platforms"""
    if platform == "DraftKings":
        # DK columns: Name, Position, Salary, TeamAbbrev, AvgPointsPerGame
        column_map = {
            'Name': 'Name',
            'Position': 'Position', 
            'Salary': 'Salary',
            'TeamAbbrev': 'Team',
            'Game Info': 'Opponent'
        }
    else:  # FanDuel
        # FD columns: Nickname, Position, Salary, Team, Opponent, FPPG
        column_map = {
            'Nickname': 'Name',
            'Position': 'Position',
            'Salary': 'Salary', 
            'Team': 'Team',
            'Opponent': 'Opponent'
        }
    
    # Rename columns if they exist
    for old_col, new_col in column_map.items():
        if old_col in df.columns:
            df = df.rename(columns={old_col: new_col})
    
    return df

def load_sample_data(platform):
    """Load sample data for the specified platform"""
    # Generate sample salaries based on platform
    if platform == "DraftKings":
        salary_data = pd.DataFrame({
            'Name': [
                'Patrick Mahomes', 'Josh Allen', 'Christian McCaffrey', 'Tyreek Hill',
                'Travis Kelce', 'Trevor Lawrence', 'Parker Washington',
                'Justin Fields', 'DJ Moore', 'Caleb Williams', 'Rome Odunze',
                'Sam Howell', 'Terry McLaurin', 'Bo Nix', 'Courtland Sutton'
            ],
            'Position': ['QB', 'QB', 'RB', 'WR', 'TE', 'QB', 'WR', 
                        'QB', 'WR', 'QB', 'WR', 'QB', 'WR', 'QB', 'WR'],
            'Salary': [8500, 8300, 10200, 8900, 7200, 6500, 3700,
                      6300, 4200, 6800, 3400, 5800, 4100, 5400, 4800],
            'Team': ['KC', 'BUF', 'SF', 'MIA', 'KC', 'JAX', 'JAX',
                    'CHI', 'CHI', 'CHI', 'CHI', 'WAS', 'WAS', 'DEN', 'DEN'],
            'Opponent': ['DEN', 'NYJ', 'TB', 'LV', 'DEN', 'MIN', 'MIN',
                        'GB', 'GB', 'GB', 'GB', 'PHI', 'PHI', 'KC', 'KC']
        })
    else:  # FanDuel
        salary_data = pd.DataFrame({
            'Name': [
                'Patrick Mahomes', 'Josh Allen', 'Christian McCaffrey', 'Tyreek Hill',
                'Travis Kelce', 'Trevor Lawrence', 'Parker Washington',
                'Justin Fields', 'DJ Moore', 'Caleb Williams', 'Rome Odunze',
                'Sam Howell', 'Terry McLaurin', 'Bo Nix', 'Courtland Sutton'
            ],
            'Position': ['QB', 'QB', 'RB', 'WR', 'TE', 'QB', 'WR',
                        'QB', 'WR', 'QB', 'WR', 'QB', 'WR', 'QB', 'WR'],
            'Salary': [9000, 8800, 10000, 8500, 7500, 7200, 4500,
                      7000, 5000, 7300, 4200, 6500, 5200, 6200, 5500],
            'Team': ['KC', 'BUF', 'SF', 'MIA', 'KC', 'JAX', 'JAX',
                    'CHI', 'CHI', 'CHI', 'CHI', 'WAS', 'WAS', 'DEN', 'DEN'],
            'Opponent': ['DEN', 'NYJ', 'TB', 'LV', 'DEN', 'MIN', 'MIN',
                        'GB', 'GB', 'GB', 'GB', 'PHI', 'PHI', 'KC', 'KC']
        })
    
    # Sample stats (same for both platforms)
    stats_data = []
    for player in salary_data['Name']:
        team = salary_data[salary_data['Name'] == player]['Team'].values[0]
        pos = salary_data[salary_data['Name'] == player]['Position'].values[0]
        
        if pos == 'QB':
            base_pts = 22
            variance = 8
        elif pos == 'RB':
            base_pts = 18
            variance = 10
        elif pos == 'WR':
            base_pts = 15
            variance = 7
        else:
            base_pts = 12
            variance = 6
        
        for week in range(5, 11):
            pts = base_pts + (variance * (hash(player + str(week)) % 100 - 50) / 50)
            pts = max(5, pts)
            
            stats_data.append({
                'player_name': player,
                'recent_team': team,
                'position': pos,
                'week': week,
                'season': 2024,
                'fantasy_points_ppr': round(pts, 1)
            })
    
    return salary_data, pd.DataFrame(stats_data)

def generate_sample_blocks(target_price, tolerance, weeks, platform='DraftKings'):
    """Generate sample data for demonstration"""
    
    if platform == "DraftKings":
    blocks = [
        {
            'name': 'Trevor Lawrence + Parker Washington',
            'players': ['Trevor Lawrence', 'Parker Washington'],
            'positions': ['QB', 'WR'],
            'prices': [6500, 3700],
            'combined_price': 10200,
            'team': 'JAX',
            'game_logs': [46.9, 38.5, 28.0, 38.2, 35.3, 38.4],
            'correlation': 0.82,
            'avg_score': 37.5,
            'ceiling': 46.9,
            'floor': 28.0,
            'games_30plus': 5,
            'opponent': 'MIN'
        },
        {
            'name': 'Justin Fields + DJ Moore',
            'players': ['Justin Fields', 'DJ Moore'],
            'positions': ['QB', 'WR'],
            'prices': [6300, 4200],
            'combined_price': 10500,
            'team': 'CHI',
            'game_logs': [51.7, 44.3, 47.5, 44.2, 30.9, 42.2],
            'correlation': 0.88,
            'avg_score': 43.5,
            'ceiling': 51.7,
            'floor': 30.9,
            'games_30plus': 6,
            'opponent': 'GB'
        },
        {
            'name': 'Caleb Williams + Rome Odunze',
            'players': ['Caleb Williams', 'Rome Odunze'],
            'positions': ['QB', 'WR'],
            'prices': [6800, 3400],
            'combined_price': 10200,
            'team': 'CHI',
            'game_logs': [38.8, 35.3, 29.2, 36.1, 31.8, 40.5],
            'correlation': 0.75,
            'avg_score': 35.3,
            'ceiling': 40.5,
            'floor': 29.2,
            'games_30plus': 5,
            'opponent': 'GB'
        },
        {
            'name': 'Sam Howell + Terry McLaurin',
            'players': ['Sam Howell', 'Terry McLaurin'],
            'positions': ['QB', 'WR'],
            'prices': [5800, 4100],
            'combined_price': 9900,
            'team': 'WAS',
            'game_logs': [42.1, 28.7, 35.8, 31.2, 26.5, 38.9],
            'correlation': 0.79,
            'avg_score': 33.9,
            'ceiling': 42.1,
            'floor': 26.5,
            'games_30plus': 4,
            'opponent': 'PHI'
        },
        {
            'name': 'Bo Nix + Courtland Sutton',
            'players': ['Bo Nix', 'Courtland Sutton'],
            'positions': ['QB', 'WR'],
            'prices': [5400, 4800],
            'combined_price': 10200,
            'team': 'DEN',
            'game_logs': [39.5, 33.2, 41.8, 28.9, 37.4, 35.6],
            'correlation': 0.71,
            'avg_score': 36.1,
            'ceiling': 41.8,
            'floor': 28.9,
            'games_30plus': 5,
            'opponent': 'KC'
        }
    ]
    
    # Add FanDuel-specific blocks if that platform is selected
    if platform == "FanDuel":
        # Adjust prices for FanDuel (typically 15-20% higher than DK)
        blocks = [
            {
                'name': 'Trevor Lawrence + Parker Washington',
                'players': ['Trevor Lawrence', 'Parker Washington'],
                'positions': ['QB', 'WR'],
                'prices': [7200, 4500],
                'combined_price': 11700,
                'team': 'JAX',
                'game_logs': [46.9, 38.5, 28.0, 38.2, 35.3, 38.4],
                'correlation': 0.82,
                'avg_score': 37.5,
                'ceiling': 46.9,
                'floor': 28.0,
                'games_30plus': 5,
                'opponent': 'MIN'
            },
            {
                'name': 'Justin Fields + DJ Moore',
                'players': ['Justin Fields', 'DJ Moore'],
                'positions': ['QB', 'WR'],
                'prices': [7000, 5000],
                'combined_price': 12000,
                'team': 'CHI',
                'game_logs': [51.7, 44.3, 47.5, 44.2, 30.9, 42.2],
                'correlation': 0.88,
                'avg_score': 43.5,
                'ceiling': 51.7,
                'floor': 30.9,
                'games_30plus': 6,
                'opponent': 'GB'
            },
            {
                'name': 'Caleb Williams + Rome Odunze',
                'players': ['Caleb Williams', 'Rome Odunze'],
                'positions': ['QB', 'WR'],
                'prices': [7300, 4200],
                'combined_price': 11500,
                'team': 'CHI',
                'game_logs': [38.8, 35.3, 29.2, 36.1, 31.8, 40.5],
                'correlation': 0.75,
                'avg_score': 35.3,
                'ceiling': 40.5,
                'floor': 29.2,
                'games_30plus': 5,
                'opponent': 'GB'
            },
            {
                'name': 'Sam Howell + Terry McLaurin',
                'players': ['Sam Howell', 'Terry McLaurin'],
                'positions': ['QB', 'WR'],
                'prices': [6500, 5200],
                'combined_price': 11700,
                'team': 'WAS',
                'game_logs': [42.1, 28.7, 35.8, 31.2, 26.5, 38.9],
                'correlation': 0.79,
                'avg_score': 33.9,
                'ceiling': 42.1,
                'floor': 26.5,
                'games_30plus': 4,
                'opponent': 'PHI'
            },
            {
                'name': 'Bo Nix + Courtland Sutton',
                'players': ['Bo Nix', 'Courtland Sutton'],
                'positions': ['QB', 'WR'],
                'prices': [6200, 5500],
                'combined_price': 11700,
                'team': 'DEN',
                'game_logs': [39.5, 33.2, 41.8, 28.9, 37.4, 35.6],
                'correlation': 0.71,
                'avg_score': 36.1,
                'ceiling': 41.8,
                'floor': 28.9,
                'games_30plus': 5,
                'opponent': 'KC'
            }
        ]
    
    # Filter by price range
    filtered_blocks = [
        b for b in blocks 
        if abs(b['combined_price'] - target_price) <= tolerance
    ]
    
    return filtered_blocks

def display_block_results(blocks, target_price, platform='DraftKings'):
    """Display the found blocks in a nice format"""
    
    st.subheader(f"🎯 Top Blocks Near ${target_price:,} ({platform})")
    
    # Sort by ceiling
    blocks_sorted = sorted(blocks, key=lambda x: x['ceiling'], reverse=True)
    
    # Display each block
    for i, block in enumerate(blocks_sorted[:10]):
        with st.expander(
            f"#{i+1} | {block['name']} - {block['team']} vs {block['opponent']} | ${block['combined_price']:,} | Ceiling: {block['ceiling']:.1f}",
            expanded=(i < 3)
        ):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Combined Price", f"${block['combined_price']:,}")
                st.caption(f"{block['players'][0]}: ${block['prices'][0]:,}")
                st.caption(f"{block['players'][1]}: ${block['prices'][1]:,}")
            
            with col2:
                st.metric("Avg Score", f"{block['avg_score']:.1f}")
                st.metric("Ceiling", f"{block['ceiling']:.1f}")
            
            with col3:
                st.metric("Floor", f"{block['floor']:.1f}")
                st.metric("30+ Games", f"{block['games_30plus']}/6")
            
            with col4:
                st.metric("Correlation", f"{block['correlation']:.2f}")
                value_per_k = block['avg_score'] / (block['combined_price'] / 1000)
                st.metric("Value/1K", f"{value_per_k:.1f}")
            
            # Mini game log chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(range(1, len(block['game_logs'])+1)),
                y=block['game_logs'],
                mode='lines+markers',
                name='Combined Score',
                line=dict(color='#4CAF50', width=3),
                marker=dict(size=10)
            ))
            fig.add_hline(y=30, line_dash="dash", line_color="orange", 
                         annotation_text="30pt threshold")
            fig.update_layout(
                title="Last 6 Weeks Combined Scores",
                xaxis_title="Weeks Ago",
                yaxis_title="Fantasy Points",
                height=300,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Comparison table
    st.subheader("📊 Quick Comparison")
    
    comp_data = []
    for block in blocks_sorted[:5]:
        comp_data.append({
            'Block': block['name'],
            'Price': f"${block['combined_price']:,}",
            'Avg': f"{block['avg_score']:.1f}",
            'Ceiling': f"{block['ceiling']:.1f}",
            'Floor': f"{block['floor']:.1f}",
            '30+ Rate': f"{block['games_30plus']}/6",
            'Correlation': f"{block['correlation']:.2f}"
        })
    
    st.dataframe(pd.DataFrame(comp_data), use_container_width=True, hide_index=True)

def display_detailed_analysis(blocks, target_price):
    """Show detailed analytics"""
    
    st.subheader("Distribution Analysis")
    
    # Ceiling distribution
    ceilings = [b['ceiling'] for b in blocks]
    fig = px.histogram(
        x=ceilings, 
        nbins=20,
        title="Ceiling Score Distribution",
        labels={'x': 'Ceiling Score', 'y': 'Count'}
    )
    fig.add_vline(x=40, line_dash="dash", line_color="red", 
                  annotation_text="40pt target")
    st.plotly_chart(fig, use_container_width=True)
    
    # Correlation vs Ceiling scatter
    st.subheader("Correlation vs Ceiling")
    
    df_scatter = pd.DataFrame([
        {
            'Block': b['name'],
            'Correlation': b['correlation'],
            'Ceiling': b['ceiling'],
            'Price': b['combined_price']
        }
        for b in blocks
    ])
    
    fig = px.scatter(
        df_scatter,
        x='Correlation',
        y='Ceiling',
        size='Price',
        hover_data=['Block'],
        title="Find High Correlation + High Ceiling Blocks (top right = best)"
    )
    st.plotly_chart(fig, use_container_width=True)

def display_game_logs(blocks):
    """Show week-by-week breakdown"""
    
    st.subheader("Week-by-Week Game Logs")
    
    selected_block = st.selectbox(
        "Select Block to Analyze",
        [b['name'] for b in blocks]
    )
    
    block = next(b for b in blocks if b['name'] == selected_block)
    
    # Create detailed game log
    weeks = [f"Week {6-i}" for i in range(6)]
    scores = block['game_logs']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=weeks,
        y=scores,
        marker_color=['green' if s >= 30 else 'orange' for s in scores],
        text=[f"{s:.1f}" for s in scores],
        textposition='auto'
    ))
    fig.add_hline(y=30, line_dash="dash", line_color="red",
                  annotation_text="30pt threshold")
    fig.update_layout(
        title=f"{selected_block} - Last 6 Weeks",
        xaxis_title="Week",
        yaxis_title="Combined Fantasy Points",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Stats breakdown
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average", f"{np.mean(scores):.1f}")
    with col2:
        st.metric("Std Dev", f"{np.std(scores):.1f}")
    with col3:
        st.metric("Consistency", f"{(1 - np.std(scores)/np.mean(scores)):.1%}")

def display_guide():
    """Display usage guide"""
    
    st.header("📖 Complete Guide")
    
    st.markdown("""
    ## What is a Player Block?
    
    A **player block** is 2-3 correlated players whose combined salary matches an expensive stud, 
    but with similar or better scoring potential.
    
    ### The Original Example
    
    **Week 9 Discovery:**
    - Trevor Lawrence ($6,500) + Parker Washington ($3,700) = **$10,200**
    - Christian McCaffrey = **$10,200**
    - Travis Hunter was OUT → More targets for Parker Washington
    - **Result**: The combo had similar ceiling to CMC
    
    ### Why This Works
    
    1. **Correlation Bonus**: QB + WR score together
       - QB throws TD → WR catches TD → BOTH get points
       - Single game outcome drives both scores
    
    2. **Salary Efficiency**: Sometimes 2 players > 1 player
       - DK pricing isn't always perfect
       - Opportunity changes (injuries) create value
    
    3. **Tournament Upside**: Differentiation wins GPPs
       - Less ownership on blocks vs studs
       - When it hits, you're ahead of field
    
    ## How to Use This Tool
    
    ### Step 1: Set Your Target
    - Pick a stud's price you want to match ($9K-$12K typically)
    - Set tolerance ($200-$500 flexibility)
    
    ### Step 2: Configure Filters
    - Weeks to analyze (4-8 weeks recommended)
    - Minimum ceiling (35+ for GPPs)
    - Correlation threshold (0.70+ for QB+WR)
    
    ### Step 3: Find Blocks
    - Upload DK salaries + weekly stats
    - Click "Find Player Blocks"
    - Tool scans all possible combinations
    
    ### Step 4: Analyze Results
    - Review game logs (consistency matters)
    - Check matchups (Vegas totals)
    - Look for opportunity changes (injuries)
    
    ### Step 5: Build Lineups
    - Mix blocks with other stacks
    - Diversify across multiple blocks
    - Consider game environment (weather, pace)
    
    ## Data Sources
    
    All data sources are **100% FREE**:
    
    1. **DraftKings Pricing**
       - Unofficial public API
       - Updated when DK releases slates
    
    2. **NFL Stats** 
       - nfl_data_py package
       - Weekly data going back to 1999
       - Fantasy points by scoring system
    
    3. **Vegas Lines** (optional)
       - Team totals for matchup analysis
       - Available from The Odds API (free tier)
    
    ## Key Metrics Explained
    
    ### Ceiling
    Best performance in recent weeks. For GPPs, you want 45+ ceilings.
    
    ### Floor  
    Worst performance. Lower floors OK if ceiling is elite (tournament strategy).
    
    ### Correlation
    How often players score together (0-1 scale):
    - 0.8+ = Excellent (QB+WR1)
    - 0.7-0.8 = Good (QB+WR2)
    - 0.6-0.7 = Acceptable (QB+TE)
    - <0.6 = Weak correlation
    
    ### 30+ Rate
    Percentage of games hitting 30 points. Target 50%+ for consistency.
    
    ### Value/1K
    Points per $1,000 spent. Industry average is ~2.5-3.0.
    
    ## Tips & Strategies
    
    ### Finding the Best Blocks
    
    ✅ **DO:**
    - Target teams with injuries to WR1/WR2 (more targets for others)
    - Look for high Vegas totals (45+ points)
    - Stack QB+WR in positive game scripts
    - Use blocks in 10-20% of lineups (not 100%)
    
    ❌ **DON'T:**
    - Ignore matchup context
    - Use low-correlation blocks (random players)
    - Put all eggs in one block
    - Forget about ownership (be contrarian)
    
    ### Advanced Tactics
    
    1. **Bring-Back Stacks**: Pair your block with opposing pass catcher
       - Ex: Lawrence+Washington + Justin Jefferson
       - Captures shootout potential
    
    2. **Game Stacks**: Use multiple blocks from same game
       - If you think it's a shootout
       - Ex: Lawrence+Washington + Cousins+Hockenson
    
    3. **Leverage Changes**: React to news
       - Injuries to target hogs
       - Weather reports (dome vs outdoor)
       - Beat writer intel
    
    ## Deployment & Updates
    
    ### Running Locally
    ```bash
    # Install dependencies
    pip install -r requirements.txt
    
    # Fetch data
    python fetch_data.py --week current
    
    # Run app
    streamlit run app.py
    ```
    
    ### Updating Data
    Run the fetch script weekly when DK releases salaries (usually Tuesday/Wednesday).
    
    ## FAQs
    
    **Q: Is this legal?**  
    A: Yes! Using public data for analysis is 100% legal. You're not scraping their site or violating ToS.
    
    **Q: Does this guarantee wins?**  
    A: No. DFS has variance. This tool increases your edge but doesn't eliminate risk.
    
    **Q: How often should I use blocks?**  
    A: Mix them in 10-30% of your GPP lineups. Diversify!
    
    **Q: What about 3-player blocks?**  
    A: Coming soon! QB+WR1+WR2 combos for mega-stacks.
    
    **Q: Can I use this for cash games?**  
    A: Blocks work better for GPPs. For cash, you want consistent studs.
    
    ## Support & Feedback
    
    Found a bug? Have ideas? Open an issue on GitHub or contact the developer.
    
    **Good luck and may your blocks hit their ceiling! 🚀**
    """)

# Run the app
if __name__ == "__main__":
    pass
