import streamlit as st
import random
import json
import requests
import time

import requests
url = "https://raw.githubusercontent.com/Bowserinator/Periodic-Table-JSON/master/PeriodicTableJSON.json"
response = requests.get(url)
full_data = response.json()

ELEMENTS = [
    {
        "symbol": el["symbol"],
        "name": el["name"],
        "atomic_number": el["number"],
        "group": el.get("xpos"),
        "period": el.get("ypos"),
        "category": el.get("category", "unknown")
    }
    for el in full_data["elements"]
    if el.get("xpos") is not None and el.get("ypos") is not None
]

# ----- Game Configurations -----
MAX_PLAYERS = 2
HAND_SIZE = 7

# ----- Utility Functions -----
def draw_cards(deck, n):
    return [deck.pop() for _ in range(min(n, len(deck)))]

def is_valid_group_meld(cards):
    return len(cards) >= 3 and all(c['group'] == cards[0]['group'] for c in cards)

def is_valid_period_meld(cards):
    sorted_cards = sorted(cards, key=lambda x: x['atomic_number'])
    return len(cards) >= 3 and all(c['period'] == cards[0]['period'] for c in cards) and \
           all(sorted_cards[i+1]['atomic_number'] == sorted_cards[i]['atomic_number'] + 1 for i in range(len(cards)-1))

def is_valid_property_meld(cards):
    return len(cards) >= 3 and all(c['category'] == cards[0]['category'] for c in cards)

def validate_meld(cards):
    return is_valid_group_meld(cards) or is_valid_period_meld(cards) or is_valid_property_meld(cards)

def animate_card_play(card):
    with st.spinner(f"Playing card {card['symbol']} ({card['name']})..."):
        time.sleep(0.6)

# ----- Streamlit App -----
st.set_page_config(page_title="Periodic Rummy", layout="wide")
st.title("🧪 Periodic Table Rummy Game")

# ----- Instructions Page -----
with st.expander("📘 How to Play"):
    st.markdown("""
    **Objective**: Make valid sets (called melds) from the periodic table cards based on:
    - **Group Meld**: Same column/group (e.g., Group 1: Li, Na, K)
    - **Period Meld**: Same row in order (e.g., Period 2: Li, Be, B)
    - **Property Meld**: Same category (e.g., Noble Gases: He, Ne, Ar)

    **Turn**:
    - Click checkboxes to select cards.
    - Click **Play Selected Cards** to try a meld.
    - Or **Draw Card** to pick a card from the deck.

    **Win Condition**:
    - Play all your cards before the computer.
    """)

# ----- Game Initialization -----
if "deck" not in st.session_state:
    st.session_state.deck = random.sample(ELEMENTS, len(ELEMENTS))
    st.session_state.hands = {
        "Player 1": draw_cards(st.session_state.deck, HAND_SIZE),
        "Computer": draw_cards(st.session_state.deck, HAND_SIZE)
    }
    st.session_state.discard_pile = []
    st.session_state.turn = "Player 1"
    st.session_state.melds = []

# ----- Player 1 Turn -----
if st.session_state.turn == "Player 1":
    st.subheader("🧑 Your Hand")
    hand = st.session_state.hands["Player 1"]
    cols = st.columns(len(hand))
    selected_cards = []
    for j, card in enumerate(hand):
        with cols[j]:
            st.markdown(f"**{card['symbol']}**\n{card['name']}")
            if st.checkbox("Select", key=f"p1_{j}"):
                selected_cards.append(card)

    if st.button("▶️ Play Selected Cards"):
        if validate_meld(selected_cards):
            for card in selected_cards:
                animate_card_play(card)
                hand.remove(card)
            st.session_state.melds.append(selected_cards)
            st.success("Valid meld!")
            st.session_state.turn = "Computer"
        else:
            st.error("Invalid meld. Try same group, period, or property.")

    if st.button("🎴 Draw Card"):
        if st.session_state.deck:
            new_card = draw_cards(st.session_state.deck, 1)[0]
            hand.append(new_card)
            animate_card_play(new_card)
            st.success(f"You drew {new_card['symbol']} ({new_card['name']})")
            st.session_state.turn = "Computer"
        else:
            st.warning("Deck is empty!")

# ----- Computer Turn -----
eligible_melds = []
if st.session_state.turn == "Computer":
    comp_hand = st.session_state.hands["Computer"]
    st.subheader("🤖 Computer is playing...")
    time.sleep(1)

    # Try to play a valid meld
    for i in range(len(comp_hand)):
        for j in range(i+1, len(comp_hand)):
            for k in range(j+1, len(comp_hand)):
                trial = [comp_hand[i], comp_hand[j], comp_hand[k]]
                if validate_meld(trial):
                    eligible_melds.append(trial)

    if eligible_melds:
        best = eligible_melds[0]
        for card in best:
            animate_card_play(card)
            comp_hand.remove(card)
        st.session_state.melds.append(best)
        st.success("Computer played a meld!")
    else:
        if st.session_state.deck:
            new_card = draw_cards(st.session_state.deck, 1)[0]
            comp_hand.append(new_card)
            animate_card_play(new_card)
            st.info(f"Computer drew a card.")
        else:
            st.warning("Deck is empty. Computer skips.")

    st.session_state.turn = "Player 1"

# ----- Display Melds -----
st.subheader("📦 Current Melds")
for meld in st.session_state.melds:
    st.markdown(" - " + ", ".join(f"{c['symbol']}({c['name']})" for c in meld))

# ----- Check Win Condition -----
if not st.session_state.hands["Player 1"]:
    st.balloons()
    st.success("🎉 You win!")
elif not st.session_state.hands["Computer"]:
    st.error("💻 Computer wins!")

st.caption("This game helps reinforce chemistry concepts through play!")
