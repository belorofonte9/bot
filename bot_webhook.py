from config import *
from flask import Flask, request
from pyngrok import ngrok, conf
from waitress import serve
import telebot
import time

bot = telebot.TeleBot(TOKEN_TELEGRAM)
web_server = Flask(__name__)

@web_server.route('/', methods=['POST'])
def webhook():
    if request.headers.get("content_type") == "application/json":
        update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return "OK", 200


@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id, "HOLA", parse_mode="html")


@bot.message_handler(content_types=['text'])
def bot_texto(message):
    bot.send_message(message.chat.id, message.text, parse_mode="html")

if __name__ == '__main__':
    print("INICIANDO EL BOLT")
    #bot.infinity_polling()
    conf.get_default().config_path = "./config_ngrok.yml"
    conf.get_default().region = "us"
    ngrok.set_auth_token(NGROK_TOKEN)
    ngrok_tunel = ngrok.connect(6000, bind_tls=True)
    ngrok_url = ngrok_tunel.public_url
    print("URL NGROK", ngrok_url)
    bot.remove_webhook()
    time.sleep(3)
    bot.set_webhook(url=ngrok_url)
    #web_server.run(host="0.0.0.0", port=6000)
    serve(web_server, host="0.0.0.0", port=6000)
