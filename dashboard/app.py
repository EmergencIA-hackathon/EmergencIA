import streamlit as st
import pandas as pd
import json
import folium
from streamlit_folium import folium_static

# Configurar o layout da página
st.set_page_config(page_title="Monitoramento de Ocorrências", layout="wide")

# Definição das cores por tipo de ocorrência
colors = {
    "Violência Contra Mulher": "pink",
    "Tráfico de Drogas": "black",
    "Roubo": "brown",
    "Estelionato": "green",
    "Lesão Corporal": "orange"
}

# Função para carregar os dados do JSON
def load_data():
    try:
        with open("/app/chatbot-telegram/flask_app/ocorrencias.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Erro ao carregar o JSON: {e}")
        return pd.DataFrame()

# Criar o mapa
def create_map(df):
    mapa = folium.Map(location=[-14.235, -51.9253], zoom_start=4)  # Centro do Brasil

    for _, row in df.iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=f"{row['tipo']} - {row['descricao']}",
            icon=folium.Icon(color=colors.get(row["tipo"], "gray"))
        ).add_to(mapa)

    return mapa

# Carregar os dados
df = load_data()

# Exibir o mapa se houver dados
if not df.empty:
    st.title("Monitoramento de Ocorrências no Brasil")
    st.write("Cada marcador representa um registro do arquivo `ocorrencias.json`.")
    folium_static(create_map(df))
else:
    st.warning("Nenhum dado disponível no momento.")
