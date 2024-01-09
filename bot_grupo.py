from datetime import datetime, timedelta
from pprint import pprint
from shutil import move
from config import *
import re
import os
import telebot

bot = telebot.TeleBot(TOKEN_TELE_CRYPTO)

d = {
    "avisos": "avisos",
    "baneados": "baneados"
}

for clave , valor in d.items():
    if not os.path.isdir(valor):
        os.mkdir(valor)
        
MAX_AVISOS = 3

palabras_prohibidas = [
    "bro",
    "de chill",
    "literal",
    "puta"
]

@bot.message_handler(content_types=["new_chat_members"])
def bievenida(m):
    for x in m.new_chat_members:
        bot.send_message(m.chat.id, f'Bienvedido <b>{x.fist_name}</b>', parse_mode='html')



@bot.message_handler(content_types=["unban"])
def cmd_unban(m):
    cid = m.chat.id
    info_member = bot.get_chat_member(cid, m.from_user.id)
    pprint(infor_member.__dict__)
    if not info_member.status in ["creator", "administrator"]:
        return
    
    archivos = os.listdir(d["baneados"])
    
    if archivos:
        bot.send_message(cid, "no hay usuarios baneados")
        return
    else:
        nombre = []
        for archivo in archivos:
            with open(f'{d["baneados"]}/archivo', 'r', encoding="utf-8") as f:
                nombre = f.read(),split("\n")[1]
                nombres.append((nombre, archivo))
        param = m.text.split()
        if len(param) == 1:
            texto = ""
            n = 0
            for nombre, archivo in nombres:
                n+=1
                texto+= f'<code>{n}</code>  {nombre}' 
            bot.send_message(cid, texto, parse_mode="html")
        else:
             indice = int(param[1])
             datos = nombres[indice-1]
             nombre = datos[0]
             icid, iuid = datos[1].split("_")
             res = bot.unban_chat_member(icid, iuid, only_if_banned=True)
             if res:
                 bot.delete_message(cid, m.message_id)
                 bot.send_message(m.chat.id, f'<b>{nombre}</b>  ha sido desbaneado', parse_mode='html')
                 os.remove(f'{d["baenados"]}/{datos[1]}')
            else:
                bot.send_message(cid, f'Error al sebanear a <b>{nombre}</b>', parse_mode="html")







@bot.message_handler(func=lambda x: True)
def mensjaes_recibidos(m):
    cid = m.chat.id
    uid = m.from_user.id
    nombre = m.from_user.first_name
    print(f'{nombre}: {m.texto}')
    if hay_palabrotas(m.text):
        bot.delete_message(cid, m.message_id)
        avisar(cid, uid, nombre)
        
        
def avisar(cid, uid, nombre):
    if not os.path.isfile(f'{d["avisos"]}/{cid}_{uid}'):
        avisos = 1
    else:
        with open(f'{d["avisos"]}/{cid}_{uid}', "r", encoding="utf-8") as f:
            avisos = int(f.read().split("\n")[0])
            avisos += 1
    texto = f'<b>AVISO</b> <code>{avisos}</code> de <code>{avisos}</code>\n'
    texto += f'<i>{nombre}</i>  ha infringido las normas'
    bot.send_message(cid, texto, parse_mode="html")
    if avisos < MAX_AVISOS:
        with open(f'{d["avisos"]}/{cid}_{uid}', "w", encoding="utf-8") as f:
            f.write(f'{avisos}\n{nombre}')
    else:
        fin_ban =   datetime.now() + timedelta(minutes=2)
        try:
            bot.ban_chat_member(cid, uid, until_date=fin_ban)
        except Exception as e:
            print(f'Error: {e}')
            return
        print(f'{nombre} ({uid}) baneado por grirpollas hasta {fin_ban}')
        bot.send_message(cid, f'<b>{nombre}</b> ({uid}) baneado por giripollas', parse_mode='html')
        move(f'{d["avisos"]}/{cid}_{uid}', f'baneados{d["baneados"]}/{cid}_{uid}')
        
        
            



def hay_palabrotas(texto):
    encontrado = False
    for palabra in palabras_prohibidas:
        if re.search(r'\b' + palabra + r'\b', texto, flags=re.IGNORECASE:
            encontrado = True
            break
    return encontrado
     




if __name__ == '__main__':
    print("▲ <code>BOT Iniciado</code>")
    bot.infinity_polling(timeout=60)