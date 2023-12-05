import streamlit as st
from slider_with_buttons import slider

estimates = slider(["gammon %", "win %", "gammon %"], [0, 50, 100], key="estimates")

st.write(estimates)
