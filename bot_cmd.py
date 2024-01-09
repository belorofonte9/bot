from config import *
import telebot
import subprocess

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


@bot.message_handler(commands=["c"])
def cmd_comando(m):
    if es_admin(m.chat.id):
        param = m.text.split()
        if len(param) == 1:
            bot.send_message(m.chat.id, "✘ No se enviaron parametros")
        else:
            comando = " ".join(param[1:])
            r = subprocess.run(
                comando, 
                shell=True, 
                stdout=subprocess.PIPE,
                stderr = subprocess.PIPE,
                universal_newlines = True
            )
            texto = ""
            #r.return_code
            if r.returncode:
                texto += f'✘ ERROR: {r.returncode}\n '
            else:
                if not r.stdout and not stderr:
                    texto += "☑ Comando ejecutado correctamente\n "
            if r.stdout:
                texto += r.stdout
            if r.stderr:
                texto += r.stderr
            bot.send_message(m.chat.id, texto)
if __name__ == '__main__':
    print("シ Iniciando el bot ")
    bot.infinity_polling()