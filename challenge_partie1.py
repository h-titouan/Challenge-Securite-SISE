import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

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

def TOP_regleICMP(df,n):
    df_ICMP = df[df['proto'] == 'ICMP']
    ICMPregle=df_ICMP.regle.value_counts().sort_values(ascending=False)
    ICMPregle=ICMPregle.to_frame().reset_index()
    ICMPregle.columns = ['regle','effectif']
    return(ICMPregle.head(n))

def TOP_regleUDP(df,n):
    df_UDP = df[df['proto'] == 'UDP']
    UDPregle=df_UDP.regle.value_counts().sort_values(ascending=False)
    UDPregle=UDPregle.to_frame().reset_index()
    UDPregle.columns = ['regle','effectif']
    return(UDPregle.head(n))

def TOP_regleTCP(df,n):
    df_TCP = df[df['proto'] == 'TCP']
    TCPregle=df_TCP.regle.value_counts().sort_values(ascending=False)
    TCPregle=TCPregle.to_frame().reset_index()
    TCPregle.columns = ['regle','nombre']
    return(TCPregle.head(n))


def rapprochement_TCP(df,n):
    TCP = df[(df['proto'] == 'TCP')]
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
    return(fig_actionpie)

#top n=10 ports inférieurs à p=1024 avec acces autorise
def TOPportpermit(df,p,n):
    df_permit = df[(df['action'] == 'PERMIT')& (df['portdst']<=p)]
    df_portdst=df_permit.portdst.value_counts()
    df_portdst=df_portdst.sort_values(axis = 0, ascending = False)
    df_portdst=df_portdst.to_frame().reset_index()
    df_portdst.columns=['portdst','nombre']
    df_portdst['portdst'] = df_portdst['portdst'].astype(str)
    if n<= df_portdst.shape[0]:
        df_portdst=df_portdst.head(n)
    #bar plot
    sns.set_style('whitegrid')
    fig = sns.barplot(x=df_portdst['portdst'], y=df_portdst['nombre'])
    return fig.figure


def action_heure(df):
    # Convertir la colonne 'Date' en type datetime pour pouvoir extraire l'heure
    df['date'] = pd.to_datetime(df['date'])

    # Extraire l'heure de la colonne 'Date'
    df['heure'] = df['date'].dt.hour

    unique_actions = df['action'].unique()
    dataframes = []
    
    for action in unique_actions:
        df_action = df[df['action'] == action]
        count_by_hour = df_action.groupby('heure').size()
        count_by_hour = count_by_hour.to_frame().reset_index()
        count_by_hour.columns = ['heure', 'nombre']
        count_by_hour['action'] = action
        dataframes.append(count_by_hour)

    result = pd.concat(dataframes)
    
    fig = px.line(result, x='heure', y='nombre', color='action', title="nombre d'actions selon l'heure")
    return fig

def portdst_heure(df):
    # Convertir la colonne 'Date' en type datetime pour pouvoir extraire l'heure
    df['date'] = pd.to_datetime(df['date'])

    # Extraire l'heure de la colonne 'Date'
    df['heure'] = df['date'].dt.hour
    
    df_deny=df[df['action'] == 'DENY']
    
    df_portdst=df_deny.portdst.value_counts()
    df_portdst=df_portdst.sort_values(axis = 0, ascending = False)
    df_portdst=df_portdst.to_frame().reset_index()
    df_portdst.columns=['portdst','nombre']

    #unique_portdst = df['portdst'].unique()
    unique_portdst=df_portdst['portdst'].head(10).values
    dataframes = []
    
    for portdst in unique_portdst:
        df_port = df_deny[df_deny['portdst'] == portdst]
        count_by_hour = df_port.groupby('heure').size()
        count_by_hour = count_by_hour.to_frame().reset_index()
        count_by_hour.columns = ['heure', 'nombre']
        count_by_hour['portdst'] = portdst
        dataframes.append(count_by_hour)

    result = pd.concat(dataframes)
    
    fig = px.line(result, x='heure', y='nombre', color='portdst', title="nombre de ports attaqués selon l'heure")
    return fig

#affiche le bar plot des refus acceptés sur chaque type de port
def proto(df):
    tab = pd.crosstab(index=df['proto'], columns=df['action'])
    graph=tab.plot(kind='bar', stacked=True, legend=True, ylim=[0,800000], color=['red','blue'], ylabel='Effectifs')
    plt.legend(loc='upper left', bbox_to_anchor=(0,1), ncol=1, borderaxespad=0)
    return(graph)
