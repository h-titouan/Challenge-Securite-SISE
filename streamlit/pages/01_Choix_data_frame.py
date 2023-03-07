import streamlit as st
import pandas as pd
from chargement_data import lancement_data

st.title('Choix du data frame')

nb_lignes = st.text_input('Combien de lignes voulez-vous selectionner ?', '10000')
st.sidebar.write('Nombre de lignes choisie : ', str(nb_lignes))
st.session_state['nb_lignes'] = int(nb_lignes)

st.session_state['df'] = lancement_data('oui', st.session_state['nb_lignes'])
#st.write(st.session_state['df'])
