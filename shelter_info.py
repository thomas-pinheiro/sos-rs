import streamlit as st
import streamlit_antd_components as sac
import folium
from streamlit_folium import st_folium
import pandas as pd
from data import load_data

 
def display_shelter_info(shelters_df, supplies_df, page_size=10):
    # Função para exibir informações de um abrigo
    def display_shelter_details(shelter, supplies_df):
        with st.container(border=True):
            # Nome do abrigo
            st.write(f"### {shelter['name']}")

            # Endereço em tamanho menor
            st.write(f"##### {shelter['address']}")

            # Status do abrigo
            if pd.notna(shelter['capacity']):
                if shelter['shelteredPeople'] >= shelter['capacity']:
                    status = "Lotado"
                    color = "#f45136"
                else:
                    status = "Disponível"
                    color = "#21aa16"
            else:
                status = "Consultar disponibilidade"
                color = "#368df4"
            
            sac.tags(
                [sac.Tag(label=status, bordered=True)],
                format_func='title',
                align='start',
                direction='horizontal',
                size='lg',
                color=color,
                key=f"status_{shelter['id']}"
            )

            all_shelters_df, all_supplies_df = load_data()  
            # Necessita Urgente de
            urgent_needs = all_supplies_df[(all_supplies_df['shelterId'] == shelter['id']) & (all_supplies_df['priority'] >= 10)]
            if not urgent_needs.empty:
                st.write("##### Necessita Urgente de:")
                urgent_tags = [
                    sac.Tag(label=item['supply_name'], color='red' if item['priority'] == 100 else 'orange', bordered=True)
                    for _, item in urgent_needs.iterrows()
                ]
                sac.tags(
                    urgent_tags,
                    format_func='title',
                    align='start',
                    direction='horizontal',
                    size='lg',
                    key=f"urgent_{shelter['id']}"
                )

            # Sobrando para doações
            available_for_donation = supplies_df[(supplies_df['shelterId'] == shelter['id']) & (supplies_df['priority'] == 1)]
            if not available_for_donation.empty:
                st.write("##### Sobrando para doações:")
                donation_tags = [
                    sac.Tag(label=item, color='green', bordered=True)
                    for item in available_for_donation['supply_name'].unique()
                ]
                sac.tags(
                    donation_tags,
                    format_func='title',
                    align='start',
                    direction='horizontal',
                    size='lg',
                    key=f"donation_{shelter['id']}"
                )

            # Atualizado em
            updated_at = pd.to_datetime(shelter['updatedAt']).strftime('%d/%m/%Y %H:%M')
            st.caption(f"**Atualizado em: {updated_at}**")

    # Ordenar os abrigos pela coluna prioritySum em ordem decrescente
    shelters_df = shelters_df.sort_values(by='prioritySum', ascending=False)

    # Contar o número de páginas
    total_shelters = shelters_df.shape[0]
    total_pages = (total_shelters + page_size - 1) // page_size

    # Selecionar a página atual usando sac.pagination
    current_page = sac.pagination(total=total_shelters, page_size=page_size, align='center', jump=True, show_total=True)
    
    # Calcular o índice de início e fim para a página atual
    start_idx = (current_page - 1) * page_size
    end_idx = min(start_idx + page_size, total_shelters)

    # Exibir informações de abrigos na página atual
    current_shelters = shelters_df.iloc[start_idx:end_idx]
    for index, shelter in current_shelters.iterrows():
        display_shelter_details(shelter, supplies_df)

def shelter_maps(shelter_df):
    # Filtrar abrigos com latitude e longitude válidas
    map_df = shelter_df.dropna(subset=['latitude', 'longitude'])

    # Criar o mapa com folium
    if not map_df.empty:
        # Centralizar o mapa na média das latitudes e longitudes
        map_center = [map_df['latitude'].mean(), map_df['longitude'].mean()]
        m = folium.Map(location=map_center)

        # Adicionar marcadores ao mapa
        for _, row in map_df.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=folium.Popup(f"<b style='font-size: 16px;'>{row['name']}</b><br><span style='font-size: 14px;'>{row['address']}</span>", max_width=300),
                tooltip=folium.Tooltip(f"<span style='font-size: 16px;'>{row['name']}</span>")
            ).add_to(m)

        # Exibir o mapa no Streamlit
        st_data = st_folium(m, use_container_width=True, height=400)
