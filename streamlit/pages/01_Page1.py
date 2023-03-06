import streamlit as st
import pandas as pd
from chargement_data import lancement_data

st.session_state['df'] = lancement_data('oui')
#st.write(st.session_state['df'] )
