import streamlit as st
import streamlit_antd_components as sac
import folium
from streamlit_folium import st_folium

def display_shelter_info(shelters_df, supplies_df, page_size=10):
    # Função para exibir informações de um abrigo
    def display_shelter_details(shelter, supplies_df):
        with st.container(border=True):
            # Nome do abrigo
            st.subheader(shelter['name'])

            # Endereço
            st.write(shelter['address'])

            # Verificar se precisa de doações
            needs_donations = supplies_df[(supplies_df['shelterId'] == shelter['id']) & (supplies_df['tags'].str.contains('NeedDonations'))]
            if not needs_donations.empty:
                st.write("Necessita urgente doações de:")
                sac.tags(
                    [sac.Tag(label=item, bordered=True) for item in needs_donations['supply_name'].unique()],
                    format_func='title', align='start', direction='horizontal',
                    key=f"donations_{shelter['id']}"
                )

            # Verificar se precisa de voluntários
            needs_volunteers = supplies_df[(supplies_df['shelterId'] == shelter['id']) & (supplies_df['tags'].str.contains('NeedVolunteers'))]
            if not needs_volunteers.empty:
                st.write("Necessita voluntários:")
                sac.tags(
                    [sac.Tag(label=item, bordered=True) for item in needs_volunteers['supply_name'].unique()],
                    format_func='title', align='start', direction='horizontal',
                    key=f"volunteers_{shelter['id']}"
                )

            # Verificar se tem itens disponíveis para doação
            available_supplies = supplies_df[supplies_df['shelterId'] == shelter['id']]
            if not available_supplies.empty:
                sac.tags([sac.Tag(label="Abrigo tem itens disponíveis para doação!", bordered=True, color='green')],
                        format_func='title', align='start', direction='horizontal',
                        key=f"available_{shelter['id']}")
    
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
