from config import *
import telebot
import time
import threading

bot  = telebot.TeleBot(TOKEN_TELEGRAM)

@bot.message_handler(commands=["start", "ayuda", "help"])
def cmd_start(message):
    bot.reply_to(message, "hola como andamos")

@bot.message_handler(content_types=["text"])
def bot_mensajes_texto(message):
    text_html = '<b>NEGRITA</b>' + '\n'
    text_html += '<i>cursiva</i>' + '\n'
    text_html += '<u>subrayado</u>' + '\n'
    text_html += '<s>tachado</s>' + '\n'
    text_html += '<code>monoespaciado</code>' + '\n'
    text_html += '<span class="tg-spoiler">spoiler</span>' + '\n'
    text_html += '<a href="https://google.com/">ENLACE</a>' + '\n'
    #markdown texts

    texto_mark = '*NEGRita*' + '\n'
    texto_mark += '_cursiva_' + '\n'
    texto_mark += '__subrayado__' + '\n'
    texto_mark += '~tachado~' + '\n'
    texto_mark += '```monoespacio```' + '\n'
    texto_mark += '||spoiler||' + '\n'
    texto_mark += '[enlace](https://www.google.com/)' + '\n'


    if message.text.startswith('/'):
        bot.send_message(message.chat.id, "Insecto atiende las indicaciones")
    else:
        #x = bot.send_message(message.chat.id, '<b>INSECTO</b>', parse_mode="html", disable_web_page_preview=True)
        #time.sleep(5)
        #bot.edit_message_text("<code>YA valio</code>", message.chat.id, x.message_id, parse_mode="html")
        #bot.delete_message(message.chat.id, message.message_id)
        foto = open("./img/cuadros.jpg", "rb")
        bot.send_photo(message.chat.id, foto, caption="quiobolas", parse_mode="html")

def recibir_msj():
    #bucle para saber si hay mensajes
    bot.infinity_polling()


if __name__ == '__main__':
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Damos la Bievenida a...."),
        telebot.types.BotCommand("/kaboom", "Ofertas gordas"),
    ])
    print('Inicidando el bot')
    hilo_bot = threading.Thread(name="hilo-bot", target=recibir_msj)
    hilo_bot.start()
    print("este hilo ya valio se no veo este mensaje")

    
