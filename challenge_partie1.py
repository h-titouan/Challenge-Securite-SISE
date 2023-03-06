import pandas as pd
import numpy as np
import plotly.express as px

import os
os.chdir("C:/Users/cornuch/Desktop")

src_fw = pd.read_csv("log_fw_3.csv", header=None,sep=';')

#renommage des colonnes
src_fw.columns = ['date','ipsrc', 'ipdst','proto','portsrc','portdst','regle','action','interface','neant','numtransp']

src_fw.info()

#supprimer la colonne 'neant'
src_fw.drop('neant', axis=1, inplace=True)

# Trouver les lignes contenant des cellules vides
lignes_vides = src_fw.isnull().any(axis=1)

# Afficher les lignes contenant des cellules vides
print(src_fw[lignes_vides])

# Supprimer les lignes contenant des cellules vides
src_fw.dropna(inplace=True)

def classementregle(df):
    classeregle=df.regle.value_counts().sort_values(ascending=False)
    classeregle=classeregle.to_frame().reset_index()
    classeregle.columns = ['regle','nombre']
    #return(classeregle['regle'])
    return(classeregle)

def barproto(df):
    diff_proto=df.proto.value_counts()
    diff_proto=diff_proto.sort_index(axis = 0, ascending = True)
    diff_proto=diff_proto.to_frame().reset_index()
    diff_proto.columns=['index','proto']
    #bar plot
    fig_protobar = px.bar(diff_proto, x="index", y="proto", color="index", title="Nombre de protocoles par catégories")
    fig_protobar.update_layout(showlegend = False)
    return(fig_protobar)

def TOP_regleUDP(df,n):
    src_fw_UDP = src_fw[src_fw['proto'] == 'UDP']
    UDPregle=src_fw.regle.value_counts().sort_values(ascending=False)
    UDPregle=UDPregle.to_frame().reset_index()
    UDPregle.columns = ['regle','effectif']
    #return(UDPregle['regle'].head(n))
    return(UDPregle.head(n))

def TOP_regleTCP(df,n):
    src_fw_TCP = src_fw[src_fw['proto'] == 'TCP']
    TCPregle=src_fw.regle.value_counts().sort_values(ascending=False)
    TCPregle=TCPregle.to_frame().reset_index()
    TCPregle.columns = ['regle','nombre']
    return(TCPregle.head(n))

def rapprochement_TCP(df,n):
    TCP = src_fw[(src_fw['proto'] == 'TCP')]
    selection = ['portdst','regle','action'] 
    TCP=TCP[selection]
    #selon les actions
    TCP_deny=TCP[(TCP['action']=='DENY')]
    TCP_permit=TCP[(TCP['action']=='PERMIT')]
    return(TCP,TCP_deny.regle.value_counts(),TCP_deny.portdst.value_counts().head(n),TCP_permit.regle.value_counts(),TCP_permit.portdst.value_counts().head(n))

def pieaction(df):
    df_action=df.action.value_counts()
    df_action=df_action.sort_index(axis = 0, ascending = True)
    df_action=df_action.to_frame().reset_index()
    df_action.columns=['index','action']
    fig_actionpie = px.pie(df_action, values='action', names='index', title='Répartition des protocoles')
    fig_actionpie.show()
    return(fig_actionpie)