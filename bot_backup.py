from config import *
import telebot
import shutil
import os

ADMINS = (
    1414138652,
)

bot = telebot.TeleBot(TOKEN_TELE_CRYPTO)

def es_admin(cid, info=True):
    if cid in ADMINS:
        return True
    else:
        if info:
            print(f'α {cid} no se encuentra autorizado')
            bot.send_message(cid, f'α {cid} no se encuentra autorizado', parse_mode="html")
            return False
        return False
    
@bot.message_handler(commands=["backup"])
def cmd_backup(m):
    if es_admin(m.chat.id):
        print("Comprimiendo archivos")
        shutil.make_archive("../backup_bot", "zip")
        print("Enviando documentos 🃏")
        bot.send_document(m.chat.id, open("../backup_bot.zip", "rb"), caption="🃏 backup del bot")
        print("Eliminando del disco duro")
        os.remove("../backup_bot.zip")


if __name__ == '__main__':
    print("シ Iniciando el bot ")
    bot.infinity_polling()