import re
import requests
import datetime
import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from session import usuario_ocorrencias
from dotenv import load_dotenv

load_dotenv()

api_url = os.getenv("API_URL")

async def start(update: Update, context: CallbackContext) -> None:
    resposta = (
        "Olá! 👋 Sou o EmergêncIA, um bot de registro de ocorrências. "
        "Posso te ajudar a registrar algo?"
    )
    teclado = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="Sim, registrar ocorrência", callback_data="enquete_ocorrencia"),
            InlineKeyboardButton(text="Quero saber mais sobre o serviço", callback_data="enquete_servico")
        ]
    ])
    await update.message.reply_text(resposta, reply_markup=teclado)

async def responder(update: Update, context: CallbackContext) -> None:
    texto_mensagem = update.message.text.strip()
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    padrao_saudacao = r"\b(olá|oi{1,3}|bom dia|boa tarde|boa noite|ei|hello|hey|salve|oi!|olá tudo bem?|oi bot)\b"
    
    if user_id in usuario_ocorrencias:
        estado = usuario_ocorrencias[user_id]["estado"]
        
        if estado == 'registrando_ocorrencia':
            usuario_ocorrencias[user_id]["ocorrencia"] += f"\n{texto_mensagem}"

            teclado = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="Sim", callback_data="sim_ocorrencia"),
                    InlineKeyboardButton(text="Não", callback_data="nao_ocorrencia")
                ]
            ])
            await update.message.reply_text(
                f"📝 Ocorrência atualizada: {usuario_ocorrencias[user_id]['ocorrencia']}\n"
                "Deseja adicionar mais alguma informação? (sim/não)",
                reply_markup=teclado
            )
            usuario_ocorrencias[user_id]["estado"] = 'esperando_confirmacao'

        elif estado == 'esperando_confirmacao':
            if texto_mensagem.lower() in ['sim', 's']:
                await update.message.reply_text("Pode continuar descrevendo a ocorrência.")
                usuario_ocorrencias[user_id]["estado"] = 'registrando_ocorrencia'

            elif texto_mensagem.lower() in ['não', 'nao', 'não quero mais registrar']:
                ocorrencia_final = usuario_ocorrencias[user_id]["ocorrencia"].strip()
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                dados_ocorrencia = {
                    "tipo": "mensagem",
                    "chat_id": user_id,
                    "usuario": user_name,
                    "data_hora": timestamp,
                    "conteudo": ocorrencia_final
                }

                response = requests.post(api_url, json=dados_ocorrencia)

                if response.status_code == 201:
                    await update.message.reply_text("✅ Sua ocorrência foi registrada com sucesso!")
                else:
                    await update.message.reply_text(f"❌ Erro ao registrar ocorrência: {response.status_code}, {response.text}")

                del usuario_ocorrencias[user_id] 
            else:
                await update.message.reply_text("Desculpe, não entendi sua resposta. Deseja adicionar mais alguma informação? (sim/não)")
    else:
        if re.fullmatch(padrao_saudacao, texto_mensagem.lower()) or len(texto_mensagem.split()) <= 2:
            await start(update, context)
        elif texto_mensagem.lower() == "tchau":
            await update.message.reply_text("Tchau! Tenha um ótimo dia!")
        else:
            usuario_ocorrencias[user_id] = {
                "estado": "registrando_ocorrencia",
                "ocorrencia": texto_mensagem
            }

            teclado = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="Sim", callback_data="sim_ocorrencia"),
                    InlineKeyboardButton(text="Não", callback_data="nao_ocorrencia")
                ]
            ])
            await update.message.reply_text(
                f"📝 Ocorrência registrada: {texto_mensagem}\nDeseja adicionar mais alguma informação? (sim/não)",
                reply_markup=teclado
            )
            usuario_ocorrencias[user_id]["estado"] = 'esperando_confirmacao'

async def callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == "enquete_ocorrencia":
        usuario_ocorrencias[user_id] = {
            "estado": "registrando_ocorrencia",
            "ocorrencia": ""
        }
        await query.message.reply_text(
            "📝 Perfeito! Envie agora sua ocorrência. Pode ser uma descrição por texto, foto, áudio ou localização."
        )
    elif query.data == "enquete_servico":
        await query.message.reply_text(
            "Nós registramos qualquer tipo de ocorrência, independente da situação. Conte com a gente para registrar e encaminhar seu relato! Você pode enviar:\n"
            "📄 Texto explicando o ocorrido\n"
            "📸 Fotos\n"
            "🎤 Áudios\n"
            "📍 Localizações\n"
            "Nosso time de agentes analisará cada caso e entrará em contato se necessário."
        )
    elif query.data == "sim_ocorrencia":
        await query.message.reply_text("Pode continuar descrevendo a ocorrência.")
        usuario_ocorrencias[user_id]["estado"] = 'registrando_ocorrencia'
    elif query.data == "nao_ocorrencia":
        ocorrencia_final = usuario_ocorrencias[user_id]["ocorrencia"].strip()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        dados_ocorrencia = {
            "tipo": "mensagem",
            "chat_id": user_id,
            "usuario": query.from_user.first_name,
            "data_hora": timestamp,
            "conteudo": ocorrencia_final
        }

        response = requests.post(api_url, json=dados_ocorrencia)

        if response.status_code == 201:
            await query.message.reply_text("✅ Sua ocorrência foi registrada com sucesso!")
        else:
            await query.message.reply_text(f"❌ Erro ao registrar ocorrência: {response.status_code}, {response.text}")

        del usuario_ocorrencias[user_id]
