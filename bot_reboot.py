from config import *
import os
import sys
import plataform    
import telebot

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
    
@bot.message_handler(commands=["restart"])
def cmd_restart(m):
    if es_admin(m.chat.id):
        print(f"Se estra reiniciando el bot###\n")
        bot.send_message(m.chat.id, "Reiniciando el bot 卐", parse_mode="HTML")
        bot.stop_polling()
        os.execv(sys.executable, [sys.executable] + [sys.argv])
        if plataform.system() == "Windows":
            os.system("shutdown /r")
        elif plataform.system() == "Linux":
            os.system("reboot now")
             



if __name__ : '__main__':
    bot.infinity_polling()