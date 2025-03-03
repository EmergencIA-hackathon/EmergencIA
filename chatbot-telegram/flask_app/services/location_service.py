from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from models.location_model import coordenadas_para_endereco
from session import usuario_ocorrencias

async def receber_localizacao(update: Update, context: CallbackContext):
    if update.message and update.message.location:
        latitude = update.message.location.latitude
        longitude = update.message.location.longitude
        endereco = await coordenadas_para_endereco(latitude, longitude)
        
        user_id = update.message.from_user.id

        if user_id in usuario_ocorrencias:
            estado = usuario_ocorrencias[user_id]["estado"]
            
            if estado == 'registrando_ocorrencia':
                usuario_ocorrencias[user_id]["ocorrencia"] += f"\n📍 Localização: {endereco} (Latitude: {latitude}, Longitude: {longitude})"
                
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
                usuario_ocorrencias[user_id]["estado"] = 'esperando_confirmacao'

        else:
            usuario_ocorrencias[user_id] = {
                "estado": "registrando_ocorrencia",
                "ocorrencia": f"📍 Localização: {endereco} (Latitude: {latitude}, Longitude: {longitude})"
            }
            
            teclado = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="Sim", callback_data="sim_ocorrencia"),
                    InlineKeyboardButton(text="Não", callback_data="nao_ocorrencia")
                ]
            ])
            await update.message.reply_text(
                f"📝 Resumo da ocorrência:\n\n"
                f"{usuario_ocorrencias[user_id]['ocorrencia']}\n\n"
                "Deseja registrar mais alguma coisa? (sim/não)",
                reply_markup=teclado
            )
            usuario_ocorrencias[user_id]["estado"] = 'esperando_confirmacao'
    else:
        await update.message.reply_text("Não foi possível obter a sua localização.")
