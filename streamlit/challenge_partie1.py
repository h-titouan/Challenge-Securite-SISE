import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

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

def TOP_IPsrc(df,n):
    IPsrc=df.ipsrc.value_counts().sort_values(ascending=False)
    IPsrc=IPsrc.to_frame().reset_index()
    IPsrc.columns = ['IPsrc','nombre']
    return(IPsrc.head(n))
