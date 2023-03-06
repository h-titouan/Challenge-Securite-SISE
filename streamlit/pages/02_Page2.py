import pandas as pd
import streamlit as st
import plotly.express as px
from challenge_partie1 import classementregle,barproto,TOP_regle,rapprochement_TCP,pieaction,TOPportpermit, proto,TOP_IPsrc
from chargement_data import lancement_data

if 'df' in st.session_state:
    data = st.session_state['df']
else : 
    data = lancement_data()

st.title('titre')
left, _, center, _, right = st.columns(
    (3, 1, 3, 1, 3)
    )

with left:
    st.write('Classement des différentes règles')
    st.write(classementregle(data))

st.plotly_chart(barproto(data))

top = st.sidebar.slider('Top combien? ', 0, 20, 5)
st.sidebar.write('Top choisi : ', str(top))
st.session_state['top'] = top

port = st.sidebar.slider('Nb de port ', 0, max(data.portdst), 1024)
st.sidebar.write('Top choisi : ', str(port))
st.session_state['port'] = port

with center :
    st.write('Meilleure règle des ICMP')
    st.write(TOP_regle(data,st.session_state['top'], proto = 'ICMP'))

with right : 
    st.write('Meilleure règle des TCP')
    st.write(TOP_regle(data,st.session_state['top'], proto = 'TCP'))

#st.table(rapprochement_TCP(st.session_state['df'],n = 5))

st.plotly_chart(pieaction(data))

st.pyplot(TOPportpermit(data,st.session_state['port'],st.session_state['top']))

#Fonctionne pas
st.write(proto(data))

st.write(TOP_IPsrc(data, st.session_state['top']))
