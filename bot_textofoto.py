from config import *
from imagekitio import ImageKit
from base64 import b64encode
import telebot


ik = ImageKit(public_key=IK_PUBLIC, private_key=IK_PRIVATE, url_endpoint=IK_URL)
bot = telebot.TeleBot(TOKEN_TELE_CRYPTO)


def ik_subir_imagen(ruta_imagen):
    with open(ruta_imagen, "rb") as f:
        imagen = b64encode(f.read())
    print("♔ ♕ ♖ ♗ ♘ ♙ ♚ ♛ ♜ ♝ ♞ ♟ subiendo imagen a imagekit")
    try:
        res = ik.upload_file(file=imagen, file_name="imagen.jpg")
    except Exception as e:
        return f'ERROR: ✘ {e.message}'
    
    status_code = res.response_metadata.http_status_code
    
    if status_code == 200:
        return res.response_metadata.raw
    else:
        return f'ERROR: ✘ {status_code}'


def enviar_foto(cid, foto, texto=None):
    print(f'El mansaje tiene {len(texto)} caracteres')
    if len(texto) <= 1024:
        bot.send_photo(cid, open("eav1.jpeg", "rb"), caption=texto2 ,parse_mode="html")
    else:
        url_foto = ik_subir_imagen(foto).get("url")
        mensaje = f'<a href="{url_foto}"> </a>\n{texto}'
        if len(mensaje) <= 4096:
            bot.send_message(cid, mensaje, parse_mode="html")
        else:
            bot.send_message(cid, "<b>Contiene más caracteres de los pérmitidos</b>")
        



@bot.message_handler(commands=["foto"])
def cmd_foto(m):
    cid = m.chat.id
    texto1 = "Prueba de <b>mensaje corto</b>"
    texto2 = "♞" *2000
    #bot.send_photo(cid, open("eav1.jpeg", "rb"), caption=texto1 ,parse_mode="html")
    enviar_foto(cid, "eav1.jpeg", texto2)
    
if __name__ == '__main__':
    print("Se comienza con el bot 𝄡 ")
    bot.infinity_polling()