from config import *
import telebot
import requests
from telebot.types import InlineQueryResultArticle
from telebot.types import InputTextMessageContent 
from bs4 import BeautifulSoup


bot = telebot.TeleBot(TOKEN_TELE)

def buscar_google(texto):
    lista = []
    user_agent = "Mozilla/5.0 (X11; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/114.0"
    headers = {
        "User-Agent": user_agent,
        'referer': 'https://www.google.com/'        
    }
    texto_url = texto.replace(" ", "+")
    url = f'https://www.google.com/search?q={texto_url}&num=10'
    r = requests.get(url, headers=headers, timeout=10)
    if r.ok:
        soup = BeautifulSoup(r.text, "html.parser")
        elementos = soup.find_all("div", {"class": "g"})
        for e in elementos:
            try:
                titulo = e.find("h3").text.strip()
            except:
                continue
            descripcion = e.find_all("span")[-1].text.strip()
            #enlace = e.find_all("a").attrs={"class": "g"}.get("href")
            enlace = e.find_all("a")
            if titulo and enlace and not (titulo, descripcion, enlace) in lista:
                lista.append((titulo, descripcion, enlace))
    print(f'Encontrados{len(lista)} enlaces')
    return lista

@bot.inline_handler(lambda q : True)
def texto_inline(m):
    if not m.query:
        return
    print(f'Buscando de Google: {m.query}')
    res = buscar_google(m.query)
    if not res:
        print("Se obtuvo ningún ressultado")
        return
    lista = []
    n = 0
    for titulo, descripcion, url in res[0:50]:
        n+=1
        obj = InlineQueryResultArticle(
            id = str(n),
            title = titulo,
            description = descripcion,
            #thumb_url = '', #imagen que se muestre en los resultados
            input_message_content = InputTextMessageContent(url),
        ) 
        lista.append(obj)
    if not lista:
        return
    try:
        bot.answer_inline_query(m.id, lista, cache_time=30)
    except Exception as e:
        print(e)
if __name__ == '__main__':
    print("BOT")
    bot.infinity_polling()
        