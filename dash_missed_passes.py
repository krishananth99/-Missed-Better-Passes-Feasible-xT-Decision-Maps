import streamlit as st
import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt

# Import the core analysis functions from your existing file
from feasible_pass_analysis import analyze_pass_scenario

# --- STREAMLIT UI LAYOUT ---
st.set_page_config(
    page_title="Pass Decision Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚽️ Pass Decision Analysis App")
st.markdown("Use this app to analyze a pass scenario and compare the actual pass against the best feasible alternatives. Adjust the player positions in the sidebar to create a new scenario.")

# --- SIDEBAR FOR USER INPUT ---
with st.sidebar:
    st.header("Player Positions")
    st.info("Enter the positions for the attacking and defending players. Use the x and y coordinates (0-120 and 0-80).")

    # Define attacker positions
    st.subheader("Attacking Players")
    passer_x = st.slider("Passer X", 0, 120, 60)
    passer_y = st.slider("Passer Y", 0, 80, 40)
    passer_id = 1

    attacker_2_x = st.slider("Attacker 2 X", 0, 120, 70)
    attacker_2_y = st.slider("Attacker 2 Y", 0, 80, 20)

    attacker_3_x = st.slider("Attacker 3 X", 0, 120, 75)
    attacker_3_y = st.slider("Attacker 3 Y", 0, 80, 55)
    actual_receiver_id = 3

    attacker_4_x = st.slider("Attacker 4 X", 0, 120, 80)
    attacker_4_y = st.slider("Attacker 4 Y", 0, 80, 70)

    attacker_5_x = st.slider("Attacker 5 X", 0, 120, 50)
    attacker_5_y = st.slider("Attacker 5 Y", 0, 80, 60)

    # Define defender positions
    st.subheader("Defending Players")
    defender_1_x = st.slider("Defender 1 X", 0, 120, 65)
    defender_1_y = st.slider("Defender 1 Y", 0, 80, 30)

    defender_2_x = st.slider("Defender 2 X", 0, 120, 70)
    defender_2_y = st.slider("Defender 2 Y", 0, 80, 50)

    defender_3_x = st.slider("Defender 3 X", 0, 120, 85)
    defender_3_y = st.slider("Defender 3 Y", 0, 80, 45)

    defender_4_x = st.slider("Defender 4 X", 0, 120, 60)
    defender_4_y = st.slider("Defender 4 Y", 0, 80, 60)

# --- SCENARIO DATA PREPARATION ---
scenario_data = {
    'passer_id': passer_id,
    'actual_pass': {
        'receiver_id': actual_receiver_id,
        'start_x': passer_x,
        'start_y': passer_y,
        'end_x': attacker_3_x,
        'end_y': attacker_3_y
    },
    'players': {
        1: {'team': 'Attackers', 'position': (passer_x, passer_y)},
        2: {'team': 'Attackers', 'position': (attacker_2_x, attacker_2_y)},
        3: {'team': 'Attackers', 'position': (attacker_3_x, attacker_3_y)},
        4: {'team': 'Attackers', 'position': (attacker_4_x, attacker_4_y)},
        5: {'team': 'Attackers', 'position': (attacker_5_x, attacker_5_y)},
        6: {'team': 'Defenders', 'position': (defender_1_x, defender_1_y)},
        7: {'team': 'Defenders', 'position': (defender_2_x, defender_2_y)},
        8: {'team': 'Defenders', 'position': (defender_3_x, defender_3_y)},
        9: {'team': 'Defenders', 'position': (defender_4_x, defender_4_y)},
    }
}

# --- RUN ANALYSIS AND DISPLAY RESULTS ---
analysis_df = analyze_pass_scenario(scenario_data)

st.subheader("Analysis Results")
st.dataframe(analysis_df)

# --- VISUALIZATION ---
st.subheader("Pitch Visualization")
fig, ax = plt.subplots(figsize=(10, 7))
pitch = Pitch(pitch_color='grass', line_color='white', line_zorder=2)
pitch.draw(ax=ax)

# Plot players
for p_id, data in scenario_data['players'].items():
    color = 'blue' if data['team'] == 'Attackers' else 'red'
    ax.scatter(data['position'][0], data['position'][1], color=color, s=200, label=f'Player {p_id}')

# Plot the actual pass
actual_pass = analysis_df[analysis_df['is_actual']]
if not actual_pass.empty:
    passer_x = actual_pass.iloc[0]['start_x']
    passer_y = actual_pass.iloc[0]['start_y']
    receiver_x = actual_pass.iloc[0]['end_x']
    receiver_y = actual_pass.iloc[0]['end_y']
    ax.arrow(passer_x, passer_y, receiver_x - passer_x, receiver_y - passer_y,
             color='gold', head_width=1, length_includes_head=True, zorder=3, label='Actual Pass')

# Plot top 3 alternative passes
alternative_passes = analysis_df[~analysis_df['is_actual']].head(3)
for _, row in alternative_passes.iterrows():
    passer_x = row['start_x']
    passer_y = row['start_y']
    receiver_x = row['end_x']
    receiver_y = row['end_y']
    ax.arrow(passer_x, passer_y, receiver_x - passer_x, receiver_y - passer_y,
             color='darkgreen', head_width=1, length_includes_head=True, alpha=0.7, zorder=1, label='Feasible Alternative')

ax.set_title('Pass Analysis: Feasible vs. Actual Options', fontsize=16)
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())

st.pyplot(fig)
