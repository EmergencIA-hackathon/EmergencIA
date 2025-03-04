from session import usuario_ocorrencias
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
import os

async def receber_arquivo(update: Update, context: CallbackContext) -> None:
    documento = update.message.document
    if documento:
        file = await documento.get_file()  #AQUI TEMOS O ARQUIVO ENVIADO

    user_id = update.message.from_user.id
    
    if user_id not in usuario_ocorrencias:
        usuario_ocorrencias[user_id] = {"estado": "registrando_ocorrencia", "ocorrencia": ""}
    
    usuario_ocorrencias[user_id]["ocorrencia"] += f'\nDocumento: {documento.file_name}\n'
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
