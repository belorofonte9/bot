import requests
import telebot
from io import BytesIO

# Configura la URL de la radio y el token de tu bot de Telegram
URL_RADIO = "https://api.soundcloud.com/tracks/179992000″ params=”color=00aabb&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false” width=”100%” height=”166″ iframe=”true” "  # Reemplaza esto con la URL de la radio que deseas transmitir
TELEGRAM_BOT_TOKEN = "TOKEN_TELE_CRYPTO"  # Reemplaza esto con el token de tu bot de Telegram

# Inicializa el bot de Telegram
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Envía /transmitir para empezar a transmitir la radio.")

@bot.message_handler(commands=['transmitir'])
def transmit_radio(message):
    try:
        audio_stream = obtener_stream_de_radio(URL_RADIO)
        enviar_audio_a_telegram(message.chat.id, audio_stream)
        bot.send_message(message.chat.id, "Transmisión de radio enviada correctamente.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ocurrió un error: {e}")

def obtener_stream_de_radio(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        raise Exception("No se pudo obtener el stream de la radio")

def enviar_audio_a_telegram(chat_id, audio_stream):
    bot.send_audio(chat_id, audio_stream)

if __name__ == "__main__":
    print("BOT INICIADO")
    bot.infinity_polling()
