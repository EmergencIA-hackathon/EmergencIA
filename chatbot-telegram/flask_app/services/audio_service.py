import requests
import speech_recognition as sr
import asyncio
from io import BytesIO
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from session import usuario_ocorrencias

def baixar_audio(file_url: str):
    return requests.get(file_url)

async def transcrever_audio(file_url: str) -> str:
    recognizer = sr.Recognizer()
    
    audio_response = await asyncio.to_thread(baixar_audio, file_url)
    
    if audio_response.status_code == 200:
        audio_data = BytesIO(audio_response.content)
        try:
            audio = await asyncio.to_thread(AudioSegment.from_file, audio_data)
            with NamedTemporaryFile(delete=True) as temp_wav_file:
                await asyncio.to_thread(audio.export, temp_wav_file, format="wav")
                temp_wav_file.seek(0)
                with sr.AudioFile(temp_wav_file.name) as source:
                    audio_content = recognizer.record(source)
                    return await asyncio.to_thread(recognizer.recognize_google, audio_content, language='pt-BR')
        except Exception as e:
            return f"Erro ao processar o áudio: {str(e)}"
    return "Erro ao baixar o áudio."

async def handle_audio(update: Update, context: CallbackContext) -> None:
    file_id = update.message.voice.file_id if update.message.voice else update.message.audio.file_id
    file = await context.bot.get_file(file_id)
    file_url = file.file_path
    transcricao = await transcrever_audio(file_url)
    
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    if user_id in usuario_ocorrencias:
        estado = usuario_ocorrencias[user_id]["estado"]

        if estado == "esperando_confirmacao":
            if transcricao.lower() in ['sim', 's']:
                await update.message.reply_text("Pode continuar descrevendo a ocorrência.")
                usuario_ocorrencias[user_id]["estado"] = "registrando_ocorrencia"
                return
        
        if estado == "registrando_ocorrencia":
            usuario_ocorrencias[user_id]["ocorrencia"] += f" {transcricao}"
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
            usuario_ocorrencias[user_id]["estado"] = "esperando_confirmacao"
            return

    usuario_ocorrencias[user_id] = {
        "estado": "esperando_confirmacao",
        "ocorrencia": transcricao
    }
    
    teclado = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="Sim", callback_data="sim_ocorrencia"),
            InlineKeyboardButton(text="Não", callback_data="nao_ocorrencia")
        ]
    ])
    await update.message.reply_text(
        f"📝 Ocorrência registrada: '{transcricao}'\nDeseja adicionar mais alguma coisa? (sim/não)",
        reply_markup=teclado
    )
