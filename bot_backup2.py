from config import *
import os
import telebot
import zipfile
import tempfile

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

def zipdir(nombre_archivo, carpeta='.', excluir=[]):
    ruta_zip = f'{tempfile.gettempdir()}/{nombre_archivo}'
    with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED) as f:
        for root, dirs, files in os.walk(carpeta):
            for file in files:
                ruta = os.path.join(root, file)
                comprimir = True
                for ex  in excluir:
                    if ex in ruta or ex.replace('/','\\') in ruta:
                        print(f'✘ Omitiendo {ruta}')
                        comprimir = False
                        break
                if comprimir:
                     print(f'♞ Comprimiendo {ruta}')
                     f.write(ruta)
    return ruta_zip

@bot.message_handler(commands=["backup"])
def cmd_backup(m):
    cid = m.chat.id
    excluir = ('/.git/','/.pytest_cache/','/reports/','/__pycache__/', '*.mp3')
    if es_admin(cid):
        ruta_zip = zipdir('mi_bot.zip', ".", excluir)
        bot.send_document(cid, open(ruta_zip, 'rb'), parse_mode="html")
        os.remove(ruta_zip)
        print("♚ Backup finalizado")
            
if __name__ == '__main__':
    print("シ Iniciando el bot ")
    bot.infinity_polling()