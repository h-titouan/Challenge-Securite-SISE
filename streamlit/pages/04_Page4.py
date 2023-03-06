import streamlit as st
from chargement_data import lancement_data
from challenge_partie1 import CAH_permit, IPsrc

if 'df' in st.session_state:
    data = st.session_state['df']
else : 
    data = lancement_data()

barre = st.sidebar.slider('IP Source associé à l\'index ', 0, 30000, 1500)
st.sidebar.write('IP Source choisie : ', str(barre))
st.session_state['barre'] = barre

#st.plotly_chart(CAH_permit(data))
st.plotly_chart(IPsrc(data,st.session_state['barre']))
