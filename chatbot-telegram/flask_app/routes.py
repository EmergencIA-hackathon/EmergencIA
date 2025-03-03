import os
import json
from flask import Blueprint, redirect, request, jsonify, session
from telegram import Update
from flask_app.controllers.bot_controller import processar_update, bot, get_loop
import asyncio
import aiohttp
import nest_asyncio
from datetime import datetime

nest_asyncio.apply()

api = Blueprint('api', __name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, "ocorrencias.json")

cached_data = []

def carregar_ocorrencias():
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4, ensure_ascii=False)
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def salvar_ocorrencia(nova_ocorrencia):
    if not nova_ocorrencia:
        return  # evita salvar ocorrências vazias

    ocorrencias = carregar_ocorrencias()
    ocorrencias.append(nova_ocorrencia)
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(ocorrencias, file, indent=4, ensure_ascii=False)

async def acionar_agentes(text):
    url = os.getenv("API_AGENTES_URL")
    data = { "texto_informal": text }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return await response.json()

@api.route('/')
def index():
    return "Servidor Flask funcionando!"

@api.route('/webhook', methods=['POST'])
def webhook():
    """Recebe atualizações do Telegram via webhook e as processa utilizando o loop global."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Dados inválidos recebidos"}), 400

    # verifica se é uma mensagem normal
    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]
        user_name = message["from"]["first_name"]
        timestamp = message["date"]
        text = message.get("text", "Mensagem sem texto")

        data_formatada = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        nova_ocorrencia = {
            "tipo": "mensagem",
            "chat_id": chat_id,
            "usuario": user_name,
            "data_hora": data_formatada,
            "conteudo": text
        }


        salvar_ocorrencia(nova_ocorrencia)
        asyncio.run_coroutine_threadsafe(processar_update(Update.de_json(data, bot=bot)), get_loop())
        response = jsonify({"message": "Webhook recebido"})
        return response, 200

    # verifica se é um callback de uma enquete ou botão
    elif "callback_query" in data:
        callback_query = data["callback_query"]
        user_id = callback_query["from"]["id"]
        data_resposta = callback_query["data"]

        asyncio.run_coroutine_threadsafe(processar_update(Update.de_json(data, bot=bot)), get_loop())
        return jsonify({"message": "Voto recebido com sucesso"}), 200

    return jsonify({"error": "Tipo de dado não suportado"}), 400

@api.route('/ocorrencias', methods=['GET'])
def listar_ocorrencias():
    return jsonify(carregar_ocorrencias())


@api.route('/ocorrencias', methods=['POST'])
async def adicionar_ocorrencia():
    dados = request.json
    if all(k in dados for k in ["tipo", "conteudo", "chat_id", "usuario", "data_hora"]):
        salvar_ocorrencia(dados)

        text = dados["conteudo"]
        user = dados["usuario"]

        cached_data.append({
            "usuario": user,
            "dados": await acionar_agentes(text)
            })

        return jsonify({"mensagem": "Ocorrência registrada com sucesso!"}), 201
    return jsonify({"erro": "Formato inválido. Certifique-se de enviar 'tipo', 'conteudo', 'chat_id', 'usuario' e 'data_hora'."}), 400

@api.get('/dados')
def dados_api_agentes():
    if (cached_data != []):
        return jsonify(cached_data)
    
    return jsonify({"Mensagem":"Tem nada aqui não, paizão"})
