import re
import requests
import datetime
import os
import pytz
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from session import usuario_ocorrencias
from dotenv import load_dotenv

load_dotenv()

api_url = os.getenv("API_URL")
fuso_horario = pytz.timezone("America/Recife")

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

    padrao_saudacao = r"(?:^|\s)(olá|oi{1,3}|bom dia|boa tarde|boa noite|ei|hello|hey|salve)(?:$|\s)"

    # Se a mensagem for uma saudação, inicia o bot e retorna
    if re.search(padrao_saudacao, texto_mensagem.lower()):
        await start(update, context)
        return

    if user_id in usuario_ocorrencias and usuario_ocorrencias[user_id]["estado"] == "esperando_confirmacao":
        await update.message.reply_text("Você já está registrando uma ocorrência. Responda 'Sim' ou 'Não' para confirmar.")
        return  

    if user_id not in usuario_ocorrencias:
        usuario_ocorrencias[user_id] = {
            "estado": "registrando_ocorrencia",
            "ocorrencia": ""
        }

    if usuario_ocorrencias[user_id]["estado"] == "esperando_confirmacao":
        await update.message.reply_text("Você já está registrando uma ocorrência. Responda 'Sim' ou 'Não' para confirmar.")
        return  
   
    usuario_ocorrencias[user_id]["ocorrencia"] += f"\n{texto_mensagem}"
    
    teclado = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="Sim", callback_data="sim_ocorrencia"),
            InlineKeyboardButton(text="Não", callback_data="nao_ocorrencia")
        ]
    ])
    
    await update.message.reply_text(
        f"📝 Ocorrência atualizada:\n{usuario_ocorrencias[user_id]['ocorrencia']}\nDeseja adicionar mais alguma informação?",
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
            "📝 <b>ENVIE AGORA SUA OCORRÊNCIA</b>\n\n"
            "Para que possamos te ajudar da melhor forma possível, comece enviando sua documentação pessoal, como sua <b>identidade (RG)</b>. Caso não esteja com ela no momento, não se preocupe! Você pode continuar o envio normalmente, informando seu <b>nome completo e CPF</b>.\n\n"
            "🔹 <b>Importante:</b> Em casos de <b>violência contra a mulher</b> ou <b>tráfico</b>, não é necessário se identificar, pois a denúncia pode ser <b>anônima</b>.\n\n"
            "📌 <b>SUA OCORRÊNCIA PODE CONTER:</b>\n\n"
            "📍 <b>Sua localização</b> – Você pode digitá-la, falar ou enviá-la tocando no símbolo 📎 e selecionando <b>Localização</b>.\n\n"
            "📝 <b>Descrição detalhada</b> – Explique com o máximo de detalhes o que aconteceu.\n\n"
            "🎙️ <b>Áudios</b> – Respire fundo, mantenha a calma e fale de forma clara para que possamos entender melhor.\n\n"
            "📷 <b>Imagens</b> – Caso tenha fotos que possam ajudar, envie-as. Podem ser <b>documentos, veículos, locais ou até mesmo suspeitos</b> (se houver). <b>Tente nos enviar imagens de boa qualidade, para uma melhor análise.</b>\n\n"
            "⚠️ <b>Manter a calma é essencial!</b> Quanto mais informações você nos enviar, mais rápido poderemos agir. Após finalizar sua ocorrência, fique tranquilo, pois estaremos <b>trabalhando para te ajudar.</b>",
            parse_mode="HTML")
    elif query.data == "enquete_servico":
        await query.message.reply_text(
            "Nós registramos qualquer tipo de ocorrência, independente da situação. Conte com a gente para registrar e encaminhar seu relato! Você pode enviar:\n"
            "📄 Texto explicando o ocorrido\n"
            "📸 Fotos\n"
            "🎤 Áudios\n"
            "📍 Localizações\n"
            "Nosso time de agentes analisará cada caso e entrará em contato se necessário.")
    elif query.data == "sim_ocorrencia":
        await query.message.reply_text("Pode continuar descrevendo a ocorrência.")
        usuario_ocorrencias[user_id]["estado"] = 'registrando_ocorrencia'
    elif query.data == "nao_ocorrencia":
        await finalizar_ocorrencia(query.message, user_id)

async def finalizar_ocorrencia(message, user_id):
    if user_id not in usuario_ocorrencias:
        return  

    ocorrencia_final = usuario_ocorrencias[user_id]["ocorrencia"].strip()
    timestamp = datetime.datetime.now(fuso_horario).strftime("%Y-%m-%d %H:%M:%S")

    dados_ocorrencia = {
        "tipo": "mensagem",
        "chat_id": user_id,
        "usuario": message.chat.first_name,
        "data_hora": timestamp,
        "conteudo": ocorrencia_final
    }

    response = requests.post(api_url, json=dados_ocorrencia)

    if response.status_code == 201:
        await message.reply_text("✅ Sua ocorrência foi registrada com sucesso!")
    else:
        await message.reply_text(f"❌ Erro ao registrar ocorrência: {response.status_code}, {response.text}")

    del usuario_ocorrencias[user_id]

