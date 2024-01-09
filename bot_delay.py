from config import *
import telebot
import time
import os

bot = telebot.TeleBot(TOKEN_TELE_CRYPTO)

CARPETA = "modo_lento"

if not os.path.isdir(CARPETA):
    os.mkdir(CARPETA)
    
MODO_LENTO = 10

@bot.message_handler(commands=['start'])
def cmd_start(m):
    texto = "▲ <code>BOT Iniciado</code>"
    bot.send_message(m.chat.id, texto, parse_mode="html")

def usuario_tiene_que_esperar(cid):
    def guardar_timestamp(cid):
        with open(f'{CARPETA}/{cid}', "w", encoding="utf-8") as f:
            f.write(f'{int(time.time())}')
    if not os.path.isfile(f'{CARPETA}/{cid}'):
        guardar_timestamp(cid)
        return False
    with open(f'{CARPETA}/{cid}', "r", encoding="utf-8") as f:
        timestamp = int(f.read())
    sec = int(time.time()) - timestamp
    if sec >= MODO_LENTO:
        guardar_timestamp(cid)
        return False
    else:
        mensaje = f'Debes esperar <code>{MODO_LENTO - sec}</code> segundos  ❄ '
        bot.send_message(cid, mensaje, parse_mode='html')
        return True
@bot.message_handler(func=lambda x: True)
def mensajes_recibidos(m):
    if usuario_tiene_que_esperar(m.chat.id):
        bot.delete_message(m.chat.id, m.message_id)
        return
    textos = "<b>PROCESANDO...</b>"
    bot.send_message(m.chat.id, textos, parse_mode='html')

if __name__ == '__main__':
    print("Se comienza con el bot 𝄡 ")
    bot.infinity_polling(timeout=60)

        