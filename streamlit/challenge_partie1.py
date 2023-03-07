import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import plotly.graph_objects as go
import plotly.offline as pyo
import datetime as dt
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

def TOP_regle(df,n,proto):
    df_UDP = df[df['proto'] == proto ]
    UDPregle=df_UDP.regle.value_counts().sort_values(ascending=False)
    UDPregle=UDPregle.to_frame().reset_index()
    UDPregle.columns = ['regle','nombre']
    return(UDPregle.head(n))

def pieaction(df):
    df_action=df.action.value_counts()
    df_action=df_action.sort_index(axis = 0, ascending = True)
    df_action=df_action.to_frame().reset_index()
    df_action.columns=['index','action']
    fig_actionpie = px.pie(df_action, values='action', names='index', title='Répartition des protocoles')
    return(fig_actionpie)

#top n=10 ports inférieurs à p=1024 avec acces autorise
def TOPportpermit(df,p,n):
    df_permit = df[(df['action'] == 'PERMIT')& (df['portdst'].astype(int)<=p)]
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

    df_permit = df[(df['action'] == 'PERMIT')]

    count_by_hour_permit = df_permit.groupby('heure').size()
    count_by_hour_permit=count_by_hour_permit.to_frame().reset_index()
    count_by_hour_permit.columns=['heure','nombre']
    count_by_hour_permit['action'] = 'PERMIT'
    
    df_deny = df[(df['action'] == 'DENY')]

    count_by_hour_deny = df_deny.groupby('heure').size()

    count_by_hour_deny=count_by_hour_deny.to_frame().reset_index()
    count_by_hour_deny.columns=['heure','nombre']
    count_by_hour_deny['action'] = 'DENY'
    
    result = pd.concat([count_by_hour_permit,count_by_hour_deny])
    fig = px.line(result, x="heure", y="nombre", color="action",title="nombre d'actions selon l'heure")
    return(fig)

#affiche le bar plot des refus acceptés sur chaque type de port
def proto(df):
    tab = pd.crosstab(index=df['proto'], columns=df['action'])
    fig = px.bar(tab, barmode='stack', color_discrete_sequence=['red', 'blue'])
    fig.update_yaxes( title='Effectifs')
    fig.update_layout(legend=dict(orientation='h', yanchor='top', y=1.1, xanchor='center', x=0.5))
    return(fig)

def TOP_IPsrc(df,n):
    IPsrc=df.ipsrc.value_counts().sort_values(ascending=False)
    IPsrc=IPsrc.to_frame().reset_index()
    IPsrc.columns = ['IPsrc','nombre']
    return(IPsrc.head(n))


def CAH_permit(df):
    # Créer un tableau de fréquences des ports de destination ayant été accepté
    test = pd.DataFrame(df.loc[df['action'].str.contains('PERMIT'), 'portdst'].value_counts())

    # Sélectionner les comptes ayant une fréquence > 0
    test = test[test['portdst'] > 0]

    # Renommer les colonnes et l'index
    test.columns = ['freq']
    test.index.name = 'portdst'

    # Effectuer une classification hiérarchique ascendante (méthode de Ward) sur les données standardisées
    Z = linkage(test['freq'].values.reshape(-1, 1), 'ward')

    # Afficher le dendrogramme résultant
    fig, ax = plt.subplots(figsize=(10, 5))
    dendrogram(Z, labels=test.index, ax=ax)

    # Tourner les labels de l'axe des x verticalement
    plt.xticks(rotation='vertical')

    plt.title('Classification hiérarchique ascendante des ports de destination ayant au leur accès autorisé')
    plt.xlabel('portdst')
    plt.ylabel('Distance')
    return(fig)


def IPsrc(df,n):
    df_permit = df[df['action'] == 'PERMIT']
    IPsrc_permit=df_permit.ipsrc.value_counts().sort_values(ascending=False)
    IPsrc_permit=IPsrc_permit.to_frame().reset_index()
    IPsrc_permit.columns = ['IPsrc','nombre autorisé']
    df_deny = df[df['action'] == 'DENY']
    IPsrc_deny=df_deny.ipsrc.value_counts().sort_values(ascending=False)
    IPsrc_deny=IPsrc_deny.to_frame().reset_index()
    IPsrc_deny.columns = ['IPsrc','nombre refusé']
    df_IPsrc = pd.merge(IPsrc_permit, IPsrc_deny, how='outer')
    df_IPsrc['nombre refusé'] = df_IPsrc['nombre refusé'].fillna(0)
    df_IPsrc['nombre autorisé'] = df_IPsrc['nombre autorisé'].fillna(0)
    df_IPsrc=df_IPsrc.reset_index()
    value=df_IPsrc.loc[n, 'IPsrc']
    nb_value_deny=df_IPsrc.loc[n, 'nombre refusé']
    nb_value_permit=df_IPsrc.loc[n, 'nombre autorisé']
    
    # create initial scatter plot
    fig = px.scatter(df_IPsrc, x='index', y='nombre autorisé', title="Nombre autorisé et refusé de IP source")

    # add scatter graph for 'nombre autorisé'
    trace1 = go.Scatter(x=df_IPsrc['index'], y=df_IPsrc['nombre autorisé'], mode='markers', name='Autorisé',marker=dict(color='blue'))
    fig.add_trace(trace1)

    # add scatter graph for 'nombre refusé'
    trace2 = go.Scatter(x=df_IPsrc['index'], y=df_IPsrc['nombre refusé'], mode='markers', name='Refusé',marker=dict(color='red'))
    fig.add_trace(trace2)

    # update the layout with a legend
    fig.update_layout(legend=dict(title='Légende', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    
    # add vertical line and text
    fig.add_shape(type='line',
              x0=n, y0=0, x1=n, y1=max(df_IPsrc['nombre autorisé']),
              line=dict(color='green', width=3))
    #texte
    fig.add_annotation(x=n+1, y=max(df_IPsrc['nombre autorisé'])/2,
                   text=f"IP source : {value}",
                   showarrow=False,
                   font=dict(size=14, color='black'))
    fig.add_annotation(x=n+1, y=max(df_IPsrc['nombre autorisé'])/3,
                   text=f"nombre accès refusés : {nb_value_deny}",
                   showarrow=False,
                   font=dict(size=14, color='black'))
    fig.add_annotation(x=n+1, y=max(df_IPsrc['nombre autorisé'])/4,
                   text=f"nombre accès autorisés : {nb_value_permit}",
                   showarrow=False,
                   font=dict(size=14, color='black'))
    return(fig)


#rapprochement regle et action : permit-deny
def tableregle(df):
    TCP = df[(df['proto'] == 'TCP')]
    selection = ['portdst','regle','action'] 
    TCP=TCP[selection]
    TCP['regle'] = TCP['regle'].astype(str)
    
    tabregle = pd.crosstab(index=TCP['regle'], columns=TCP['action'])
    # Definir les données
    data = []
    for col in tabregle.columns:
        sns.set_style('whitegrid')
        fig = sns.barplot(x=tabregle.index, y=tabregle[col])
    return fig.figure

    # Créer un bar chart
    fig = go.Figure(data=data, layout=layout)
    return fig

def portdstregle(TCP,n):
    portdst_n=TCP.portdst.value_counts().sort_values(ascending=False)
    portdst_n[:n]
    top_ports = portdst_n[:n].index
    df_top_ports = TCP[TCP['portdst'].isin(top_ports)]
    tabportdst_n = pd.crosstab(index=df_top_ports['portdst'], columns=df_top_ports['regle'])
    for column in tabportdst_n.columns:
        sns.set_style('whitegrid')
        fig = sns.barplot(x=tabportdst_n.index, y=tabportdst_n[column]).set_title ('Top Destination TCP Ports by Rule')
    return fig.figure