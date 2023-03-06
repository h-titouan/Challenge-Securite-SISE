import streamlit as st
from challenge_partie1 import action_heure,portdst_heure

st.title('Analyse temporelle')

st.plotly_chart(action_heure(st.session_state['df']))
st.plotly_chart(portdst_heure(st.session_state['df']))