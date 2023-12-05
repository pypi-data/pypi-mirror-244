import streamlit as st
from slider_with_buttons import slider

player_win = slider("Player Win %", 50, key="player_win")
player_g = slider("Player Gammon %", 0, key="player_g")

st.write("Player Win %", player_win)
st.write("Player Gammon %", player_g)
