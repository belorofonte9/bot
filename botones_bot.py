from config import *
from telebot.types import ReplyKeyboardMarkup
from telebot.types import ForceReply #citar mensajes
from telebot.types import ReplyKeyboardRemove #quitar botonera definitivamente
import telebot

bot = telebot.TeleBot(TOKEN_TELEGRAM)
usuarios = {}

@bot.message_handler(commands=['start', 'ayuda', 'help'])
def cmd_start(message):
    bot.send_message(message.chat.id, 'Usar el comando /alta para introducir datos')

@bot.message_handler(commands=['alta'])
def cmd_alta(message):
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, 'como te llamas?', reply_markup=markup)
    bot.register_next_step_handler(msg, preguntar_edad)

def preguntar_edad(message):
    usuarios[message.chat.id] = {}
    usuarios[message.chat.id]["nombre"] = message.text
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, 'cuantos años tienes?', reply_markup=markup)
    bot.register_next_step_handler(msg, preguntar_sexo)

def preguntar_sexo(message):
    if not message.text.isdigit():
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, 'ERROR: Debes de mandar un numero\n Cuantos años tienes?')
        bot.register_next_step_handler(msg, preguntar_sexo)
    else:
        usuarios[message.chat.id]["edad"] = int(message.text)
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Pulsa el botón", resize_keyboard=True)
        markup.add("Hombre", "Mujer")
        msg = bot.send_message(message.chat.id, 'Cual es tu sexo', reply_markup=markup)
        bot.register_next_step_handler(msg, guardar_datos_usuario)

def guardar_datos_usuario(message):
    if message.text != "Hombre" and message.text != "Mujer":
        msg = bot.send_message(message.chat.id, 'ERROR: Sexo no valido.\n Pulsa un botón')
        bot.register_next_step_handler(msg, guardar_datos_usuario)
    else:
        usuarios[message.chat.id]["sexo"] = message.text
        texto = "Datos introducidos: \n"
        texto += f'<code>Nombre:</code> {usuarios[message.chat.id]["nombre"]}\n'
        texto += f'<code>Edad..:</code> {usuarios[message.chat.id]["edad"]}\n'
        texto += f'<code>Sexo..:</code> {usuarios[message.chat.id]["sexo"]}\n'
        markup = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, texto, parse_mode="html", reply_markup=markup)
        print(usuarios)
        #en este punto debemos de guardar los datos en un BBDD
        del usuarios[message.chat.id] #eliminamos todos los datos de la memoria para ya no usarlos


if __name__ == '__main__':
    print('INCIANDO BOT')
    bot.infinity_polling()