import streamlit as st
from data import load_extra_supplies
from shelter_info import display_shelter_info, shelter_maps
import unicodedata

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def get_extra_supply():
    # Carregar dados
    shelters_df, supplies_df = load_extra_supplies()

    # Obter a lista de itens disponíveis para seleção, removendo acentos antes de ordenar
    available_items = supplies_df['supply_name'].unique()
    available_items_no_accents = sorted(available_items, key=remove_accents)

    # Adicionar uma seleção de item na interface
    selected_items = st.multiselect("##### Buscar itens:", available_items_no_accents, placeholder="Escolha itens para encontrar abrigos")

    # Remover acentos dos itens selecionados
    selected_items_no_accents = [remove_accents(item) for item in selected_items]

    # Se nenhum item for selecionado, definir calculation_option como "Todos os itens selecionados"
    if not selected_items:
        calculation_option = "Todos os itens selecionados"
    else:
        cl1, cl2, cl3 = st.columns(3)
        with cl1:
            # Opção de Calculo
            calculation_option = st.selectbox("##### Tipo de Busca:", ("Todos os itens selecionados", "Pelo menos um dos itens selecionados"), placeholder="Selecione o tipo de busca", index=0)

    # Filtrar abrigos que têm os itens selecionados disponíveis para doação
    if calculation_option == "Todos os itens selecionados":
        shelters_with_selected_items = supplies_df.groupby('shelterId').filter(lambda x: all(remove_accents(item) in x['supply_name'].apply(remove_accents).values for item in selected_items_no_accents))['shelterId'].unique()
    else:
        shelters_with_selected_items = supplies_df[supplies_df['supply_name'].apply(remove_accents).isin(selected_items_no_accents)]['shelterId'].unique()

    filtered_shelters_df = shelters_df[shelters_df['id'].isin(shelters_with_selected_items)]

    shelter_maps(filtered_shelters_df)

    # Exibir informações de abrigos que têm o item selecionado disponível para doação
    display_shelter_info(filtered_shelters_df, supplies_df)