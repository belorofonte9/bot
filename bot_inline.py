import telebot
from config import *
from telebot.types import InlineQueryResultArticle
from telebot.types import InputTextMessageContent
from bs4 import BeautifulSoup
import requests

bot = telebot.TeleBot(TOKEN_TELEGRAM_INLINE)

def buscar_google(texto):
    lista = []
    user_agent = 'Mozilla/5.0 (X11; CrOS aarch64 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.95 Safari/537.36'
    headers = {
        "User-Agent": user_agent,
        'referer': 'https://www.google.com.mx/'
    }
    texto_url = texto.replace(" ", "+")
    url = f'https://www.google.com.mx/search?q={ texto_url}&mum=20'
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
            enlace  = e.find_all("a").attrs.get("href")
            if titulo and enlace and not (titulo, descripcion, enlace) in lista:
                lista.append((titulo, descripcion, enlace))
    print(f'Encontrados {len(lista)} enlaces')
    return lista

@bot.inline_handler(lambda q: True)