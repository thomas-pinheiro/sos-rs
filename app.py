import streamlit as st     
import streamlit_antd_components as sac
from extra_supply import get_extra_supply
from shelter_info import display_shelter_info, shelter_maps
from data import load_extra_supplies

# Configurar a página
st.set_page_config(
    page_title="SOS Rio Grande do Sul",
    initial_sidebar_state="expanded",
    page_icon="medias/icon.jpg",
    layout="wide"
)

# Estilo personalizado
custom_css = '''
    <style>
    .stApp .main .block-container {
        padding: 30px 50px;
    }
    .stApp [data-testid='stSidebar']>div:nth-child(1)>div:nth-child(2) {
        padding-top: 50px;
    }
    iframe {
        display: block;
    }
    .stRadio div[role='radiogroup']>label {
        margin-right: 5px;
    }
    </style>
'''

# Carregar estilos
with open('style.css') as f:
    custom_css += f'<style>{f.read()}</style>'

st.markdown(custom_css, unsafe_allow_html=True)

# Menu lateral
with st.sidebar:
    menu = sac.menu([
        sac.MenuItem('Início', icon='house-fill'),
        sac.MenuItem('Preciso de Ajuda', icon='building-fill', children=[
            sac.MenuItem('Suprimentos Sobrandro para Doação', icon='box-seam'),
            sac.MenuItem('Mapa de Abrigos', icon='geo-alt')
        ]),
        sac.MenuItem('Quero Ajudar', icon='building-fill', children=[
            sac.MenuItem('Necessitando de Suprimentos', icon='send'),
            sac.MenuItem('Lista Suprimentos em Falta', icon='list-check')
        ])
    ], return_index=True, index=0, open_all=True)

    if st.button("Recarregar", type='primary', use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Conteúdo principal
if menu == 0:
    st.write("Início")
elif menu == 2:
    get_extra_supply()
elif menu == 3:
    st.write("### Mapa de Abrigos")
    shelters_df, supplies_df = load_extra_supplies()
    shelter_maps(shelters_df)
    display_shelter_info(shelters_df, supplies_df)
elif menu == 5:
    st.write("Doe Suprimentos")
elif menu == 6:
    st.write("Suprimentos Necessários")
