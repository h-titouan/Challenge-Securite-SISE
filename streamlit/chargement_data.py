import streamlit as st
import pandas as pd
#importation necessaire pour la selection des variables
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

    
def filter_dataframe(df: pd.DataFrame):
    modifier = st.checkbox("Ajouter des filters")
    if not modifier:
        st.write(df)
        return df
    df = df.copy()

    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]
    st.experimental_data_editor(df, key="data_editor") 
    return df

def lancement_data(filtre = 'non'):
    data = pd.read_csv('C:/Users/laura/Downloads/log_fw_3.csv/log_fw_3.csv', sep = ';', header=None)
    data.columns = ['date','ipsrc', 'ipdst','proto','portsrc','portdst','regle','action','interface','neant','numtransp']
    #supprimer la colonne 'neant'
    data.drop('neant', axis=1, inplace=True)
    # Trouver les lignes contenant des cellules vides
    lignes_vides = data.isnull().any(axis=1)
    # Supprimer les lignes contenant des cellules vides
    data.dropna(inplace=True)
    if filtre == 'oui':
        data = filter_dataframe(data)
    return data


