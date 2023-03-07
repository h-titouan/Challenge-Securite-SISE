import streamlit as st
from chargement_data import lancement_data
from challenge_partie1 import CAH_permit

if 'df' in st.session_state:
    data = st.session_state['df']
else : 
    data = lancement_data()

st.title('Machine Learning')

st.pyplot(CAH_permit(data))
