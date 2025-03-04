import json
import requests
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static

# Função para obter coordenadas via Nominatim
def get_coordinates(address):
    url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json"
    response = requests.get(url, headers={'User-Agent': 'EmergencIA-App'})
    
    if response.status_code == 200 and response.json():
        location = response.json()[0]
        lat = location["lat"]
        lon = location["lon"]

        return float(lat), float(lon)
    return None, None

# Mapeamento de crimes para cores
crime_colors = {
    "Violência Contra Mulher": "pink",
    "Tráfico de Droga": "black",
    "Roubo": "brown",
    "Estelionato": "green",
    "Lesão Corporal": "orange",
}

# Função para carregar e processar os dados
def load_data():
    try:
        with open("/app/chatbot-telegram/flask_app/ocorrencias.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        
        ocorrencias = []
        
        for item in data:
            dados = item.get("dados", {})
            localizacao = dados.get("dados_localizacao", {})
            
            latitude = localizacao.get("latitude")
            longitude = localizacao.get("longitude")
            endereco = f"{localizacao.get('endereco_logradouro', '')}, {localizacao.get('endereco_bairro', '')}, {localizacao.get('nome_municipio', '')}, {localizacao.get('sigla_uf', '')}"
            
            # Se não houver latitude/longitude, geocodifica pelo endereço
            if not latitude or not longitude:
                latitude, longitude = get_coordinates(endereco)
            
            if latitude and longitude:
                tipos_crimes = dados.get("tipos_crimes", ["Desconhecido"])
                crime_tipo = tipos_crimes[0] if tipos_crimes else "Desconhecido"
                crime_cor = crime_colors.get(crime_tipo, "gray")

                ocorrencias.append({
                    "latitude": latitude,
                    "longitude": longitude,
                    "crime": crime_tipo,
                    "cor": crime_cor,
                    "descricao": dados.get("texto_narrativa", {}).get("text", "Sem descrição"),
                })

        return ocorrencias
    except Exception as e:
        st.error(f"Erro ao carregar o JSON: {e}")
        return []

# Configuração da interface no Streamlit
st.title("Mapa de Ocorrências - EmergencIA")

# Carrega os dados
ocorrencias = load_data()

# Criando o mapa
m = folium.Map(location=[-14.235, -51.9253], zoom_start=4)  # Centro do Brasil

# Adicionando ocorrências ao mapa
for ocorrencia in ocorrencias:
    folium.Marker(
        location=[ocorrencia["latitude"], ocorrencia["longitude"]],
        popup=ocorrencia["descricao"],
        icon=folium.Icon(color=ocorrencia["cor"])
    ).add_to(m)

# Exibir o mapa no Streamlit
folium_static(m)
