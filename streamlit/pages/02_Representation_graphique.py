import pandas as pd
import streamlit as st
import plotly.express as px
from challenge_partie1 import classementregle,barproto,TOP_regle,pieaction,TOPportpermit, proto, tableregle, portdstregle, IPsrc
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

port = st.sidebar.slider('Nb de port ', 0, int(max(data.portdst)), 1024)
st.sidebar.write('Top choisi : ', int(port))
st.session_state['port'] = port

with center : 
    st.write('Meilleure règle des TCP')
    st.write(TOP_regle(data,st.session_state['top'], proto = 'TCP'))

st.plotly_chart(pieaction(data))

st.pyplot(TOPportpermit(data,st.session_state['port'],st.session_state['top']))

st.plotly_chart(proto(data))

st.pyplot(tableregle(data))

nb_port = st.sidebar.text_input('Combien de port voulez vous afficher', '5')
st.sidebar.write('Nombre de port choisi : ', str(nb_port))
st.session_state['nb_port'] = int(nb_port)

st.pyplot(portdstregle(data, st.session_state['nb_port']))

barre = st.sidebar.text_input('IP Source associé à l\'index', '0')
st.sidebar.write('IP Source choisie : ', str(barre))
st.session_state['barre'] = int(barre)
st.plotly_chart(IPsrc(data,st.session_state['barre']))