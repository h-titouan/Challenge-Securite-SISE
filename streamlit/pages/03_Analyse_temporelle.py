import streamlit as st
from chargement_data import lancement_data
from challenge_partie1 import action_heure,portdst_heure

st.title('Analyse temporelle')

if 'df' in st.session_state:
    data = st.session_state['df']
else : 
    data = lancement_data()

st.plotly_chart(action_heure(data))
st.plotly_chart(portdst_heure(data))