import streamlit as st
import pandas as pd

shelters_url = 'https://docs.google.com/spreadsheets/d/1xRt5dn4d4L-aBBNdKGvGjN3u0q9N0QDl65Y3AzJLaVE/export?format=csv&gid=0'
supplies_url = 'https://docs.google.com/spreadsheets/d/1xRt5dn4d4L-aBBNdKGvGjN3u0q9N0QDl65Y3AzJLaVE/export?format=csv&gid=1877968488'

# Função para carregar dados do Google Sheets
@st.cache_data(show_spinner="Carregando dados, por favor aguarde...", ttl=1200)
def load_data():
    shelters_df = pd.read_csv(shelters_url)
    supplies_df = pd.read_csv(supplies_url)

    # Converter latitude e longitude para float e substituir vírgulas por pontos
    shelters_df['latitude'] = shelters_df['latitude'].astype(str).str.replace(',', '.').astype(float)
    shelters_df['longitude'] = shelters_df['longitude'].astype(str).str.replace(',', '.').astype(float)

    # Ordenar supplies_df pela coluna priority em ordem decrescente
    supplies_df = supplies_df.sort_values(by='priority', ascending=False)
    return shelters_df, supplies_df

@st.cache_data(show_spinner="Carregando dados, por favor aguarde...", ttl=1200)
def load_extra_supplies():
    shelters_df = pd.read_csv(shelters_url)
    supplies_df = pd.read_csv(supplies_url)

    # Converter latitude e longitude para float e substituir vírgulas por pontos
    shelters_df['latitude'] = shelters_df['latitude'].astype(str).str.replace(',', '.').astype(float)
    shelters_df['longitude'] = shelters_df['longitude'].astype(str).str.replace(',', '.').astype(float)

    # Filtrar suprimentos com tag "RemainingSupplies"
    supplies_df['tags'] = supplies_df['tags'].astype(str)
    supplies_df = supplies_df[supplies_df['tags'].str.contains('RemainingSupplies')]
    
    # Ordenar supplies_df pela coluna priority em ordem decrescente
    supplies_df = supplies_df.sort_values(by='priority', ascending=False)
    return shelters_df, supplies_df
