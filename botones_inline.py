from config import *
from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup
from bs4 import BeautifulSoup
import telebot
import requests
import pickle
import os

#constantes
N_RES_PAG = 5
MAX_ANCHO_ROW = 8
DIR = {"busqueda":"./busqueda/"}
for key in DIR:
    try:
        os.mkdir(key)
    except:
        pass




bot = telebot.TeleBot(TOKEN_TELEGRAM)

@bot.message_handler(commands=['botones'])
def cmd_botones(message):
    markup = InlineKeyboardMarkup(row_width=2)
    b1 = InlineKeyboardButton("Vamonos a buscar google", url="https://duckduckgo.com/")
    b2 = InlineKeyboardButton("AMZ", url="https://amazon.com")
    b3 = InlineKeyboardButton("Más conocimiento", url="https://wikipedia.com")
    b_cerrar = InlineKeyboardButton("Cerrar", callback_data="cerrar")
    markup.add(b1, b2, b3, b_cerrar)
    bot.send_message(message.chat.id, "Mis mejores enlaces", reply_markup=markup)

@bot.callback_query_handler(func=lambda x:True)
def respuesta_botones_inline(call):
    cid = call.from_user.id
    mid = call.message.id
    if call.data == "cerrar":
        bot.delete_message(cid, mid)
        return
    datos = pickle.load(open(f'{DIR["busqueda"]}{cid}_{mid}', 'rb'))
    if call.data == "anterior":
        if datos["pag"] == 0:
            bot.answer_callback_query(call.id, "Ya esta en la primera página")
        else:
            datos["pag"] -= 1
            pickle.dump(datos, open(f'{DIR["busqueda"]}{cid}_{mid}', 'wb'))
            mostrar_pag(datos["lista"], cid, datos["pag"], mid)
        return
    elif call.data == "siguiente":
        if datos["pag"] * N_RES_PAG + N_RES_PAG >= len(datos["lista"]):
            bot.answer_callback_query(call.id, "Ya esta en la última página")
        else:

            datos["pag"] += 1
            pickle.dump(datos, open(f'{DIR["busqueda"]}{cid}_{mid}', 'wb'))
            mostrar_pag(datos["lista"], cid, datos["pag"], mid)
        return


@bot.message_handler(commands=['buscar'])
def cmd_buscar(message):
    texto_buscar = " ".join(message.text.split()[1:])
    if not texto_buscar:
        texto = 'Debes introducir una busqueda.\n'
        texto += f'<code>{message.text}</code>\n'
        bot.send_message(message.chat.id, texto, parse_mode='html')
        return 1
    else:
        print(f'Buscando en Google: "{texto_buscar}"')
        url = f'https://www.google.com.mx/search?q={texto_buscar.replace(" ", "+")}&num=50'
        #url = f'https://duckduckgo.com/?q={texto_buscar.replace(" ", "+")}&num=100'
        user_agent = "Mozilla/5.0 (X11; CrOS aarch64 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.95 Safari/537.36"
        headers = {"user-agent": user_agent}
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            print(f'ERROR al buscar es: {res.status_code}{res.reason}')
            bot.send_message(message.chat.id, "Se ha producido un error intentato más tarde.")
            return 1
        else:
            soup = BeautifulSoup(res.text, "html.parser")
            elementos = soup.find_all("div", class_="g")
            lista = []
            for elemento in elementos:
                try:
                    titulo = elemento.find("h3").text
                    url = elemento.find("a").attrs.get("href")
                    if not "http" in url:
                        url ="https://www.google.com.mx/" + url
                    if [titulo, url] in lista:
                        continue
                    lista.append([titulo, url])
                except:
                    continue
        mostrar_pag(lista, message.chat.id)
            
def mostrar_pag(lista, cid, page=0, mid=None):
    markup = InlineKeyboardMarkup(row_width=MAX_ANCHO_ROW)
    b_anterior = InlineKeyboardButton("🔙" ,callback_data="anterior")
    b_cerrar = InlineKeyboardButton("x", callback_data="cerrar")
    b_siguiente = InlineKeyboardButton("🎯" ,callback_data="siguiente")
    inicio = page*N_RES_PAG
    fin = inicio + N_RES_PAG
    if fin > lista:
        fin = len(lista)
    
    mensaje = f'<i>Resultados {inicio + 1}-{fin} de {len(lista)} </i>\n\n'
    n = 1
    botones = []
    for item in lista[inicio:fin]:
        botones.append(InlineKeyboardButton(str(n), url=item[1]))
        mensaje += f'<b>[{n}]</b> {item[0]}\n'
        n += 1
    markup.add(*botones)
    markup.row(b_anterior, b_cerrar, b_siguiente)
    if mid:
        bot.edit_message_text(mensaje, cid, mid, reply_markup=markup, parse_mode="html", disable_web_page_preview=True)
    else:
        res = bot.send_message(cid, mensaje, reply_markup=markup, parse_mode="html", disable_web_page_preview=True)
        mid = res.message_id
        datos = {"pag":0, "lista":lista}
        pickle.dump(datos, open(f'{DIR["busqueda"]}{cid}_{mid}', 'wb'))




if __name__ == '__main__':
    print("INICIANDO EL BOLT")
    bot.infinity_polling()
