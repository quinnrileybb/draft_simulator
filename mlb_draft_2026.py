import streamlit as st
import pandas as pd
import os
import random

# Page config
st.set_page_config(
    page_title="MLB Draft Simulator 2026",
    page_icon="⚾",
    layout="wide"
)

@st.cache_data
def load_prospects():
    """Load prospects from CSV file"""
    try:
        df = pd.read_csv('prospects_2026.csv')
        prospects = []
        for _, row in df.iterrows():
            rank = int(row['Rank'])
            
            if rank <= 10: grade = "A+"
            elif rank <= 30: grade = "A"
            elif rank <= 60: grade = "A-"
            elif rank <= 100: grade = "B+"
            elif rank <= 150: grade = "B"
            elif rank <= 250: grade = "B-"
            elif rank <= 400: grade = "C+"
            else: grade = "C"
            
            # Parse slot value from CSV (remove $ and commas)
            slot_value_str = str(row.get('Slot Value', '$0')).replace('$', '').replace(',', '')
            try:
                slot_value = int(slot_value_str)
            except:
                slot_value = 0
            
            # Parse adjusted slot bonus
            adjusted_str = str(row.get('Adjusted Slot Bonus', '$0')).replace('$', '').replace(',', '')
            try:
                adjusted_slot = int(adjusted_str)
            except:
                adjusted_slot = slot_value
            
            prospects.append({
                "rank": rank,
                "name": row['Player'],
                "position": row['Position'],
                "school": row['School'],
                "class": row.get('Class', 'C'),
                "grade": grade,
                "slot_value": slot_value,  # Standard slot for this pick
                "adjusted_slot": adjusted_slot,  # What they typically sign for
                "drafted": False,
                "team": None,
                "pick": None
            })
        
        return prospects
    except Exception as e:
        st.error(f"Error loading prospects: {e}")
        return []

# Import complete 2026 draft order
import sys
sys.path.append('/home/claude')
from draft_order_2026 import get_full_draft_order

# Get complete draft order (rounds 1-10, ~324 picks with all comp rounds)
COMPLETE_DRAFT_ORDER = get_full_draft_order()

# Teams for selection (alphabetical)
ALL_TEAMS = sorted([
    "Angels", "Astros", "Athletics", "Blue Jays", "Braves",
    "Brewers", "Cardinals", "Cubs", "Diamondbacks", "Dodgers",
    "Giants", "Guardians", "Marlins", "Mets", "Nationals",
    "Orioles", "Padres", "Phillies", "Pirates", "Rangers",
    "Rays", "Red Sox", "Reds", "Rockies", "Royals",
    "Mariners", "Tigers", "Twins", "White Sox", "Yankees"
])

# Bonus pools
TEAM_POOLS = {
    "White Sox": 17090000, "Rays": 19590500, "Twins": 16410400, "Giants": 15011200,
    "Pirates": 18592800, "Royals": 15505000, "Orioles": 17893200, "Athletics": 11527200,
    "Braves": 16800000, "Rockies": 16560000, "Nationals": 15245600, "Angels": 15650800,
    "Cardinals": 15452800, "Marlins": 15100000, "Diamondbacks": 11876400, "Rangers": 12180800,
    "Astros": 14200000, "Reds": 13100000, "Guardians": 12500000, "Red Sox": 13500000,
    "Padres": 11200000, "Tigers": 12150000, "Cubs": 11350000, "Mariners": 11100000,
    "Brewers": 14500000, "Mets": 6500000, "Yankees": 6200000, "Phillies": 9800000,
    "Blue Jays": 11200000, "Dodgers": 6800000
}

# Slot values
SLOT_VALUES = {}
r1_vals = [11629645, 10765335, 9979620, 9253200, 8584125, 7960500, 7378425, 6833625, 
           6321975, 5840475, 5386725, 4957875, 4551375, 4164825, 3795900, 3442425, 
           3103125, 2776950, 2462775, 2159625, 1866150, 1581300, 1304175, 1033875, 
           769875, 3613200, 3613200, 3043125, 3043125, 3043125]

for i, val in enumerate(r1_vals, 1):
    SLOT_VALUES[i] = val

current_val = 2300000
for pick in range(31, 301):
    SLOT_VALUES[pick] = max(150000, int(current_val))
    current_val *= 0.985

def get_team_at_pick(pick_num, round_num):
    """Get which team picks at this position using complete draft order"""
    # Find the pick in COMPLETE_DRAFT_ORDER
    for rnd, team, overall_pick in COMPLETE_DRAFT_ORDER:
        if overall_pick == pick_num:
            return team
    return None

def get_round_from_pick(pick_num):
    """Get round number from overall pick number"""
    for rnd, team, overall_pick in COMPLETE_DRAFT_ORDER:
        if overall_pick == pick_num:
            return rnd if rnd != "CB-B" else 2  # Treat CB-B as part of round 2
    return None

def get_team_picks_in_round(team, round_num):
    """Get all pick numbers for a team in a specific round"""
    picks = []
    for rnd, tm, overall_pick in COMPLETE_DRAFT_ORDER:
        # Match round (handle CB-B as special case)
        if rnd == round_num or (round_num == 2 and rnd == "CB-B"):
            if tm == team:
                picks.append(overall_pick)
    return picks

# Team Draft Tendencies (Applied contextually based on round and situation)
TEAM_TENDENCIES = {
    "Padres": {
        "round_1_hs_boost": 0.50,  # ONLY Round 1: extreme HS preference
        "desc": "First Round HS Focus"
    },
    "Tigers": {
        "round_1_ss_boost": 0.20,  # Round 1-3: love shortstops
        "round_1_hs_boost": 0.15,
        "desc": "HS Middle Infielders Early"
    },
    "Braves": {
        "pitcher_boost": 0.20,  # All rounds: pitching org
        "desc": "Pitching Development"
    },
    "Royals": {
        "round_1_hs_pitcher_boost": 0.25,  # Round 1-2: prep arms
        "pitcher_boost": 0.10,  # All rounds: slight pitcher lean
        "desc": "Prep Arms Early"
    },
    "Astros": {
        "college_boost": 0.25,  # All rounds: college heavy
        "pitcher_boost": 0.15,  # Especially college pitchers
        "desc": "College Arms"
    },
    "Angels": {
        "college_boost": 0.20,  # Round 1-5: college preference
        "hitter_boost": 0.15,
        "desc": "College Bats"
    },
    "Rays": {
        "pitcher_boost": 0.20,  # All rounds
        "college_boost": 0.10,  # Slight college lean
        "desc": "Pitching Development"
    },
    "Pirates": {
        "round_1_hs_boost": 0.15,  # Round 1-3: upside plays
        "pitcher_boost": 0.15,
        "desc": "HS Arms Early"
    },
    "Reds": {
        "balanced": True,
        "desc": "Balanced Approach"
    },
    "Guardians": {
        "underslot": 0.15,  # Later rounds: save money
        "college_boost": 0.10,  # Polished guys
        "desc": "Underslot Strategy"
    },
    "Orioles": {
        "hitter_boost": 0.15,  # All rounds
        "college_boost": 0.10,
        "desc": "College Position Players"
    },
    "Mariners": {
        "pitcher_boost": 0.20,  # All rounds
        "desc": "Pitching Development"
    },
    "Marlins": {
        "pitcher_boost": 0.20,  # Heavy pitching
        "round_1_hs_boost": 0.10,
        "desc": "Arms Heavy"
    },
    "Cubs": {
        "college_boost": 0.20,  # Round 1-5
        "hitter_boost": 0.15,
        "desc": "College Hitters"
    },
    "Dodgers": {
        "round_1_hs_boost": 0.15,  # Round 1-3: development depth
        "balanced": True,
        "desc": "Development Depth"
    },
    "Brewers": {
        "toolsy_boost": 0.20,  # All rounds: raw tools
        "desc": "Tools Over Polish"
    },
    "Blue Jays": {
        "college_boost": 0.15,  # Round 1-5
        "pitcher_boost": 0.15,
        "desc": "College Arms"
    },
    "Rangers": {
        "medical_risk_tolerance": 0.25,  # Guys who fell due to injury concerns
        "desc": "Medical Risk Takers"
    },
    "Phillies": {
        "hitter_boost": 0.15,
        "college_boost": 0.10,
        "desc": "Position Players"
    },
    "Yankees": {
        "hitter_boost": 0.15,
        "college_boost": 0.10,
        "desc": "College Bats"
    },
    "Red Sox": {
        "hitter_boost": 0.15,
        "college_boost": 0.10,
        "desc": "Position Players"
    },
    "Diamondbacks": {
        "athlete_boost": 0.10,
        "desc": "Athletic Profiles"
    },
    "Rockies": {
        "chaos": 0.20,  # Random variance
        "desc": "Unpredictable"
    },
    "White Sox": {
        "balanced": True,
        "desc": "Best Available"
    },
    "Twins": {
        "balanced": True,
        "desc": "Balanced Approach"
    },
    "Giants": {
        "college_boost": 0.10,
        "desc": "Safe Picks"
    },
    "Cardinals": {
        "college_boost": 0.15,
        "desc": "College Heavy"
    },
    "Mets": {
        "balanced": True,
        "desc": "Balanced"
    },
    "Athletics": {
        "balanced": True,
        "desc": "Best Available"
    },
}

def apply_team_tendency(team, prospect, base_score, pick_num):
    """Apply team-specific draft tendencies based on round and context"""
    if team not in TEAM_TENDENCIES:
        return base_score
    
    tendencies = TEAM_TENDENCIES[team]
    multiplier = 1.0
    
    is_hs = (prospect['class'] == 'H')
    is_pitcher = (prospect['position'] in ['LHP', 'RHP'])
    is_hitter = not is_pitcher
    rank = prospect['rank']
    
    # Determine round from pick number
    if pick_num <= 40:
        round_num = 1
    elif pick_num <= 108:
        round_num = 2
    elif pick_num <= 143:
        round_num = 3
    elif pick_num <= 171:
        round_num = 4
    elif pick_num <= 201:
        round_num = 5
    else:
        round_num = 6 + (pick_num - 202) // 30
    
    # ROUND 1 SPECIFIC TENDENCIES (picks 1-40)
    if round_num == 1:
        # Padres: ONLY applies to Round 1
        if 'round_1_hs_boost' in tendencies and is_hs:
            multiplier += tendencies['round_1_hs_boost']
        
        # Tigers: Round 1 SS boost
        if 'round_1_ss_boost' in tendencies and prospect['position'] == 'SS':
            multiplier += tendencies['round_1_ss_boost']
        if 'round_1_hs_boost' in tendencies and is_hs:
            multiplier += tendencies['round_1_hs_boost']
        
        # Royals: Round 1 HS pitcher combo
        if 'round_1_hs_pitcher_boost' in tendencies and is_hs and is_pitcher:
            multiplier += tendencies['round_1_hs_pitcher_boost']
    
    # EARLY ROUNDS (1-3) - Some tendencies apply
    if round_num <= 3:
        # Pirates: HS boost rounds 1-3
        if team == "Pirates" and 'round_1_hs_boost' in tendencies and is_hs:
            multiplier += tendencies['round_1_hs_boost'] * 0.7  # Weaker in R2-3
        
        # Tigers: SS boost rounds 1-3
        if team == "Tigers" and 'round_1_ss_boost' in tendencies and prospect['position'] == 'SS':
            multiplier += tendencies['round_1_ss_boost'] * 0.7
        
        # Dodgers: HS boost rounds 1-3
        if team == "Dodgers" and 'round_1_hs_boost' in tendencies and is_hs:
            multiplier += tendencies['round_1_hs_boost'] * 0.6
    
    # MID ROUNDS (1-5) - College preference still matters
    if round_num <= 5:
        if 'college_boost' in tendencies and not is_hs:
            multiplier += tendencies['college_boost']
    
    # ALL ROUNDS - Organizational philosophy
    # Pitcher boosts (apply to all rounds)
    if 'pitcher_boost' in tendencies and is_pitcher:
        multiplier += tendencies['pitcher_boost']
    
    # Hitter boosts (apply to all rounds)
    if 'hitter_boost' in tendencies and is_hitter:
        multiplier += tendencies['hitter_boost']
    
    # College boost for orgs that don't limit to early rounds
    if round_num > 5 and team in ["Astros", "Braves", "Rays"]:
        if 'college_boost' in tendencies and not is_hs:
            multiplier += tendencies['college_boost'] * 0.5  # Half strength late
    
    # Toolsy Boost (Brewers) - guys that fell despite high rank
    if 'toolsy_boost' in tendencies:
        # If ranked top 150 but available after pick 200 = fell for polish concerns
        if rank <= 150 and pick_num > 200:
            multiplier += tendencies['toolsy_boost']
    
    # Medical Risk Tolerance (Rangers) - guys who fell dramatically
    if 'medical_risk_tolerance' in tendencies:
        # If ranked top 100 but available after pick 150 = possible injury concern
        if rank <= 100 and pick_num > 150:
            multiplier += tendencies['medical_risk_tolerance']
        # If ranked top 200 but available after pick 300+ = definite injury concern
        if rank <= 200 and pick_num > 300:
            multiplier += tendencies['medical_risk_tolerance'] * 1.5
    
    # Underslot Strategy (Guardians) - later rounds, grab fallers
    if 'underslot' in tendencies and round_num >= 3:
        # Guys ranked much higher than current pick = savings opportunity
        if rank < pick_num * 0.6:
            multiplier += tendencies['underslot']
    
    # Chaos Factor (Rockies) - random
    if 'chaos' in tendencies:
        multiplier += random.uniform(-tendencies['chaos'], tendencies['chaos'])
    
    return base_score * multiplier
    """
    Calculate how likely a prospect is to be picked at this position
    Based on rank, position, H/C status
    """
    rank = prospect['rank']
    position = prospect['position']
    is_hs = (prospect['class'] == 'H')
    
    # Base expected pick = rank with adjustments
    expected_pick = rank
    
    # POSITION ADJUSTMENTS
    if position in ['C', 'SS']:
        if rank <= 50:
            expected_pick -= random.randint(5, 12)
        elif rank <= 150:
            expected_pick -= random.randint(8, 20)
        else:
            expected_pick -= random.randint(10, 25)
    elif position == 'CF':
        if rank <= 50:
            expected_pick -= random.randint(3, 8)
        elif rank <= 150:
            expected_pick -= random.randint(5, 15)
        else:
            expected_pick -= random.randint(8, 20)
    elif position == '1B':
        if rank <= 50:
            expected_pick += random.randint(5, 15)
        elif rank <= 100:
            expected_pick += random.randint(10, 25)
        elif rank <= 250:
            expected_pick += random.randint(20, 50)
        else:
            expected_pick += random.randint(40, 80)
    elif position in ['LHP', 'RHP']:
        if rank > 50:
            expected_pick += random.randint(5, 20)
    
    # H/C ADJUSTMENTS
    if is_hs:
        if rank <= 30:
            expected_pick += random.randint(2, 8)
        elif rank <= 50:
            expected_pick += random.randint(5, 15)
            if random.random() < 0.30:  # 30% major fall
                expected_pick += random.randint(30, 60)
        elif rank <= 100:
            expected_pick += random.randint(15, 40)
            if random.random() < 0.40:  # 40% disaster
                expected_pick += random.randint(50, 100)
        elif rank <= 250:
            expected_pick += random.randint(30, 80)
            if random.random() < 0.50:  # 50% massive fall
                expected_pick += random.randint(80, 150)
        else:
            # Deep HS prospects often go undrafted
            if random.random() < 0.60:
                expected_pick = 999  # Basically undrafted in 10 rounds
            else:
                expected_pick += random.randint(100, 200)
    else:  # College
        if rank <= 50:
            expected_pick -= random.randint(2, 8)
        elif rank <= 150:
            # College seniors rise
            if random.random() < 0.40:  # Assume 40% seniors
                expected_pick -= random.randint(15, 35)
            else:
                expected_pick -= random.randint(5, 15)
        elif rank <= 400:
            if random.random() < 0.40:  # Seniors
                expected_pick -= random.randint(20, 50)
            else:
                expected_pick -= random.randint(10, 25)
    
    # Calculate distance from expected pick
    distance = abs(pick_num - expected_pick)
    
    # Convert to probability score (closer = higher score)
    if distance == 0:
        score = 100
    elif distance < 10:
        score = 90
    elif distance < 25:
        score = 70
    elif distance < 50:
        score = 40
    elif distance < 100:
        score = 20
    else:
        score = 5
    
    return max(1, score)

def calculate_variance_score(prospect, pick_num):
    """Apply team-specific draft tendencies"""
    if team not in TEAM_TENDENCIES:
        return base_score
    
    tendencies = TEAM_TENDENCIES[team]
    multiplier = 1.0
    
    is_hs = (prospect['class'] == 'H')
    is_pitcher = (prospect['position'] in ['LHP', 'RHP'])
    is_hitter = not is_pitcher
    
    # HS Boost
    if 'hs_boost' in tendencies and is_hs:
        multiplier += tendencies['hs_boost']
    
    # College Boost
    if 'college_boost' in tendencies and not is_hs:
        multiplier += tendencies['college_boost']
    
    # Pitcher Boost
    if 'pitcher_boost' in tendencies and is_pitcher:
        multiplier += tendencies['pitcher_boost']
    
    # Hitter Boost
    if 'hitter_boost' in tendencies and is_hitter:
        multiplier += tendencies['hitter_boost']
    
    # SS Boost
    if 'ss_boost' in tendencies and prospect['position'] == 'SS':
        multiplier += tendencies['ss_boost']
    
    # HS Pitcher Combo
    if 'hs_pitcher_boost' in tendencies and is_hs and is_pitcher:
        multiplier += tendencies['hs_pitcher_boost']
    
    # Upside Boost (high rank that fell = tools)
    if 'upside_boost' in tendencies:
        if prospect['rank'] <= 150 and prospect['grade'] in ['A+', 'A', 'A-']:
            multiplier += tendencies['upside_boost']
    
    # Chaos Factor (Rockies)
    if 'chaos' in tendencies:
        multiplier += random.uniform(-0.3, 0.3)
    
    return base_score * multiplier

def cpu_draft_pick(available_prospects, team, pick_num):
    """CPU logic with variance and team tendencies"""
    if not available_prospects:
        return None
    
    # Calculate scores for each prospect
    prospect_scores = []
    for prospect in available_prospects:
        # Base score from variance model
        variance_score = calculate_variance_score(prospect, pick_num)
        
        # Apply team tendencies
        final_score = apply_team_tendency(team, prospect, variance_score, pick_num)
        
        prospect_scores.append((prospect, final_score))
    
    # Weight heavily toward higher scores but allow some randomness
    prospects = [p[0] for p in prospect_scores]
    weights = [p[1] for p in prospect_scores]
    
    # Add small random element so it's not always the same
    weights = [w + random.uniform(0, 10) for w in weights]
    
    selected = random.choices(prospects, weights=weights, k=1)[0]
    return selected

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.user_team = None
    st.session_state.num_rounds = 10
    st.session_state.draft_started = False
    st.session_state.current_pick = 1
    st.session_state.current_round = 1
    st.session_state.available_prospects = []
    st.session_state.draft_results = []
    st.session_state.team_spending = {team: 0 for team in ALL_TEAMS}

# Load prospects
ALL_PROSPECTS = load_prospects()
if len(ALL_PROSPECTS) > 0:
    st.sidebar.success(f"Loaded {len(ALL_PROSPECTS)} prospects")

# UI
st.title("2026 MLB Draft Simulator")

# Sidebar - Setup
with st.sidebar:
    st.header("Draft Setup")
    
    if not st.session_state.draft_started:
        # Team selection
        selected_team = st.selectbox(
            "Select Your Team",
            ALL_TEAMS,
            index=0
        )
        
        # Number of rounds
        num_rounds = st.slider(
            "Number of Rounds",
            min_value=1,
            max_value=10,
            value=10
        )
        
        st.markdown("---")
        
        if st.button("Start Draft", type="primary", use_container_width=True):
            st.session_state.user_team = selected_team
            st.session_state.num_rounds = num_rounds
            st.session_state.draft_started = True
            st.session_state.available_prospects = ALL_PROSPECTS.copy()
            st.session_state.current_pick = 1
            st.session_state.current_round = 1
            st.session_state.draft_results = []
            st.session_state.team_spending = {team: 0 for team in ALL_TEAMS}
            st.rerun()
    
    else:
        st.markdown(f"**Your Team:** {st.session_state.user_team}")
        st.markdown(f"**Rounds:** {st.session_state.num_rounds}")
        st.markdown("---")
        
        # Show your pool
        pool = TEAM_POOLS[st.session_state.user_team]
        spent = st.session_state.team_spending[st.session_state.user_team]
        remaining = pool - spent
        
        st.subheader("Your Bonus Pool")
        st.metric("Total Pool", f"${pool:,.0f}")
        st.metric("Spent", f"${spent:,.0f}")
        st.metric("Remaining", f"${remaining:,.0f}", 
                 delta=f"{(remaining/pool)*100:.1f}%",
                 delta_color="normal" if remaining >= 0 else "inverse")
        
        if remaining < 0:
            st.error("Over pool!")
        
        st.markdown("---")
        
        # Your upcoming picks
        st.subheader("Your Picks")
        
        # Show picks for all remaining rounds
        for round_num in range(st.session_state.current_round, st.session_state.num_rounds + 1):
            user_picks = get_team_picks_in_round(st.session_state.user_team, round_num)
            if user_picks:
                pick_word = "Pick" if len(user_picks) == 1 else "Picks"
                st.markdown(f"**Round {round_num}:** {pick_word} {', '.join(map(str, user_picks))}")
        
        st.markdown("---")
        
        if st.button("Reset Draft", use_container_width=True):
            st.session_state.draft_started = False
            st.rerun()

# Main content
if not st.session_state.draft_started:
    st.info("Select your team and number of rounds to begin!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Round 1 Order")
        # Get first 30 picks from complete draft order
        round_1_teams = [team for rnd, team, pick in COMPLETE_DRAFT_ORDER if pick <= 30]
        st.dataframe(
            pd.DataFrame({"Pick": range(1, len(round_1_teams) + 1), "Team": round_1_teams}),
            use_container_width=True, hide_index=True, height=400
        )
    
    with col2:
        st.subheader("Team Bonus Pools")
        pools_list = sorted(TEAM_POOLS.items(), key=lambda x: x[1], reverse=True)
        st.dataframe(
            pd.DataFrame([{"Team": t, "Pool": f"${p:,.0f}"} for t, p in pools_list]),
            use_container_width=True, hide_index=True, height=400
        )

else:
    # Draft in progress
    # Get actual total picks from complete draft order for selected rounds
    total_picks = max([pick for rnd, team, pick in COMPLETE_DRAFT_ORDER if (isinstance(rnd, int) and rnd <= st.session_state.num_rounds) or (rnd == "CB-B" and 2 <= st.session_state.num_rounds)])
    
    if st.session_state.current_pick > total_picks:
        # DRAFT COMPLETE
        st.success("Draft Complete!")
        
        # Show results
        df = pd.DataFrame(st.session_state.draft_results)
        
        tab1, tab2, tab3 = st.tabs(["Full Results", "Your Team", "All Teams"])
        
        with tab1:
            st.dataframe(
                df[['pick', 'round', 'team', 'rank', 'player', 'position', 'school', 'class', 'grade']],
                use_container_width=True, hide_index=True, height=600
            )
        
        with tab2:
            your_picks = df[df['team'] == st.session_state.user_team]
            st.subheader(f"{st.session_state.user_team} Draft Results")
            st.dataframe(
                your_picks[['pick', 'round', 'rank', 'player', 'position', 'school', 'class', 'grade']],
                use_container_width=True, hide_index=True
            )
        
        with tab3:
            spending_data = []
            for team in sorted(ALL_TEAMS):
                pool = TEAM_POOLS[team]
                spent = st.session_state.team_spending[team]
                picks = len(df[df['team'] == team])
                spending_data.append({
                    'Team': team,
                    'Picks': picks,
                    'Pool': f"${pool:,.0f}",
                    'Spent': f"${spent:,.0f}",
                    'Remaining': f"${pool - spent:,.0f}"
                })
            st.dataframe(pd.DataFrame(spending_data), use_container_width=True, hide_index=True)
        
    else:
        # Draft ongoing
        current_team = get_team_at_pick(st.session_state.current_pick, st.session_state.current_round)
        is_user_pick = (current_team == st.session_state.user_team)
        
        # Header
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.subheader(f"Round {st.session_state.current_round} - Pick #{st.session_state.current_pick}")
        with col2:
            st.subheader(f"**{current_team}** is on the clock")
        with col3:
            slot = SLOT_VALUES.get(st.session_state.current_pick, 150000)
            st.metric("Slot Value", f"${slot:,.0f}")
        
        st.markdown("---")
        
        if is_user_pick:
            # USER'S PICK
            st.info("YOUR PICK! Select a player below")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                position_filter = st.multiselect("Position", sorted(set(p['position'] for p in st.session_state.available_prospects)))
            with col2:
                grade_filter = st.multiselect("Grade", ["A+", "A", "A-", "B+", "B", "B-", "C+", "C"])
            with col3:
                hs_college = st.multiselect("H/C", ["H", "C"])
            
            # Filter prospects
            filtered = st.session_state.available_prospects.copy()
            if position_filter:
                filtered = [p for p in filtered if p['position'] in position_filter]
            if grade_filter:
                filtered = [p for p in filtered if p['grade'] in grade_filter]
            if hs_college:
                filtered = [p for p in filtered if p['class'] in hs_college]
            
            # Show available prospects
            st.markdown(f"### Available Prospects ({len(filtered)} showing)")
            
            for prospect in filtered[:50]:  # Show top 50
                col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 3, 2, 3, 1, 1, 2])
                with col1:
                    st.write(f"#{prospect['rank']}")
                with col2:
                    st.write(prospect['name'])
                with col3:
                    st.write(prospect['position'])
                with col4:
                    school_short = prospect['school'][:25] + "..." if len(prospect['school']) > 25 else prospect['school']
                    st.write(school_short)
                with col5:
                    st.write(prospect['class'])
                with col6:
                    st.write(prospect['grade'])
                with col7:
                    if st.button(f"Draft", key=f"draft_{prospect['rank']}"):
                        # Make the pick
                        prospect['drafted'] = True
                        prospect['team'] = current_team
                        prospect['pick'] = st.session_state.current_pick
                        
                        # Use the prospect's adjusted slot bonus (what they actually sign for)
                        actual_bonus = prospect.get('adjusted_slot', slot)
                        
                        st.session_state.draft_results.append({
                            'pick': st.session_state.current_pick,
                            'round': st.session_state.current_round,
                            'team': current_team,
                            'player': prospect['name'],
                            'rank': prospect['rank'],
                            'position': prospect['position'],
                            'school': prospect['school'],
                            'class': prospect['class'],
                            'grade': prospect['grade'],
                            'slot_value': slot,  # Pick's slot value
                            'actual_bonus': actual_bonus  # What they actually sign for
                        })
                        
                        st.session_state.team_spending[current_team] += actual_bonus
                        st.session_state.available_prospects.remove(prospect)
                        
                        # Advance pick
                        st.session_state.current_pick += 1
                        # Update round based on actual pick
                        new_round = get_round_from_pick(st.session_state.current_pick)
                        if new_round:
                            st.session_state.current_round = new_round
                        
                        st.rerun()
        
        else:
            # CPU PICK
            st.warning(f"{current_team} is picking...")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Simulate Pick", type="primary", use_container_width=True):
                    # CPU makes pick
                    selected = cpu_draft_pick(st.session_state.available_prospects, current_team, st.session_state.current_pick)
                
                if selected:
                    selected['drafted'] = True
                    selected['team'] = current_team
                    selected['pick'] = st.session_state.current_pick
                    
                    # Use the prospect's adjusted slot bonus
                    actual_bonus = selected.get('adjusted_slot', slot)
                    
                    st.session_state.draft_results.append({
                        'pick': st.session_state.current_pick,
                        'round': st.session_state.current_round,
                        'team': current_team,
                        'player': selected['name'],
                        'rank': selected['rank'],
                        'position': selected['position'],
                        'school': selected['school'],
                        'class': selected['class'],
                        'grade': selected['grade'],
                        'slot_value': slot,  # Pick's slot value
                        'actual_bonus': actual_bonus  # What they sign for
                    })
                    
                    st.session_state.team_spending[current_team] += actual_bonus
                    st.session_state.available_prospects.remove(selected)
                    
                    # Advance pick
                    st.session_state.current_pick += 1
                    # Update round based on actual pick
                    new_round = get_round_from_pick(st.session_state.current_pick)
                    if new_round:
                        st.session_state.current_round = new_round
                    
                    st.rerun()
            
            with col2:
                if st.button("Simulate Until My Pick", use_container_width=True):
                    # Find next user pick
                    next_user_pick = None
                    for rnd, team, pick in COMPLETE_DRAFT_ORDER:
                        if pick > st.session_state.current_pick and team == st.session_state.user_team:
                            next_user_pick = pick
                            break
                    
                    if next_user_pick is None:
                        st.warning("No more picks remaining for your team")
                    else:
                        # Simulate all picks until user's turn
                        while st.session_state.current_pick < next_user_pick:
                            current_team_sim = get_team_at_pick(st.session_state.current_pick, st.session_state.current_round)
                            if current_team_sim != st.session_state.user_team:
                                selected = cpu_draft_pick(st.session_state.available_prospects, current_team_sim, st.session_state.current_pick)
                                
                                if selected:
                                    slot_sim = SLOT_VALUES.get(st.session_state.current_pick, 150000)
                                    actual_bonus = selected.get('adjusted_slot', slot_sim)
                                    
                                    selected['drafted'] = True
                                    selected['team'] = current_team_sim
                                    selected['pick'] = st.session_state.current_pick
                                    
                                    st.session_state.draft_results.append({
                                        'pick': st.session_state.current_pick,
                                        'round': st.session_state.current_round,
                                        'team': current_team_sim,
                                        'player': selected['name'],
                                        'rank': selected['rank'],
                                        'position': selected['position'],
                                        'school': selected['school'],
                                        'class': selected['class'],
                                        'grade': selected['grade'],
                                        'slot_value': slot_sim,
                                        'actual_bonus': actual_bonus
                                    })
                                    
                                    st.session_state.team_spending[current_team_sim] += actual_bonus
                                    st.session_state.available_prospects.remove(selected)
                            
                            # Advance
                            st.session_state.current_pick += 1
                            new_round = get_round_from_pick(st.session_state.current_pick)
                            if new_round:
                                st.session_state.current_round = new_round
                        
                        st.rerun()
        
        # Show picks with tabs
        if st.session_state.draft_results:
            st.markdown("---")
            
            tab1, tab2, tab3 = st.tabs(["Recent Picks", "Your Picks", "All Picks"])
            
            with tab1:
                st.subheader("Last 20 Picks")
                recent = pd.DataFrame(st.session_state.draft_results[-20:])
                st.dataframe(
                    recent[['pick', 'team', 'rank', 'player', 'position', 'school', 'class']],
                    use_container_width=True, hide_index=True, height=500
                )
            
            with tab2:
                st.subheader(f"{st.session_state.user_team} Picks")
                all_picks = pd.DataFrame(st.session_state.draft_results)
                your_picks = all_picks[all_picks['team'] == st.session_state.user_team]
                if len(your_picks) > 0:
                    st.dataframe(
                        your_picks[['pick', 'round', 'rank', 'player', 'position', 'school', 'class', 'grade']],
                        use_container_width=True, hide_index=True, height=500
                    )
                else:
                    st.info("You haven't picked yet")
            
            with tab3:
                st.subheader("Complete Draft Board")
                all_picks = pd.DataFrame(st.session_state.draft_results)
                st.dataframe(
                    all_picks[['pick', 'round', 'team', 'rank', 'player', 'position', 'school', 'class', 'grade']],
                    use_container_width=True, hide_index=True, height=500
                )

