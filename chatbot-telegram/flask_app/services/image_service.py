from PIL import Image
import pytesseract
import asyncio
import re
import os
from session import usuario_ocorrencias
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

async def handle_image(update: Update, context: CallbackContext):
    await processar_imagem_com_ocr(update, context)

async def processar_imagem_com_ocr(update: Update, context: CallbackContext):
    file = await context.bot.get_file(update.message.photo[-1].file_id)
    file_name = f"imagem_{update.message.message_id}.jpg"

    try:
        await file.download_to_drive(file_name)
        img = await asyncio.to_thread(Image.open, file_name)
        texto = await asyncio.to_thread(pytesseract.image_to_string, img)
        
        padrao_cpf = r"\d{3}\.\d{3}\.\d{3}-\d{2}"
        match_cpf = re.search(padrao_cpf, texto)
        cpf_info = f"CPF identificado: {match_cpf.group(0)}" if match_cpf else "Nenhum CPF identificado."
    
    except Exception as e:
        cpf_info = f"Erro ao processar a imagem: {str(e)}"
    
    user_id = update.message.from_user.id
    
    if user_id not in usuario_ocorrencias:
        usuario_ocorrencias[user_id] = {"estado": "registrando_ocorrencia", "ocorrencia": ""}
    
    usuario_ocorrencias[user_id]["ocorrencia"] += f'\nImagem: {file_name}\n{cpf_info}'
    usuario_ocorrencias[user_id]["estado"] = 'esperando_confirmacao'
    
    teclado = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="Sim", callback_data="sim_ocorrencia"),
            InlineKeyboardButton(text="Não", callback_data="nao_ocorrencia")
        ]
    ])
    
    await update.message.reply_text(
        f"📝 Resumo da ocorrência:\n\n"
        f"{usuario_ocorrencias[user_id]['ocorrencia']}\n\n"
        "Deseja adicionar mais alguma coisa? (sim/não)",
        reply_markup=teclado
    )
    
    if os.path.exists(file_name):
        os.remove(file_name)

