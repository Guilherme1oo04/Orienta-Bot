import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv()

chave_api = os.environ["API_TOKEN"]

estagioBot = telebot.TeleBot(token=chave_api)

#Teclado inicial
keyboardInicio = ReplyKeyboardMarkup(resize_keyboard=True)

#Botão sobre
button_sobre = KeyboardButton('/sobre')
#Botão dúvidas
button_duvidas = KeyboardButton('/duvidas')

keyboardInicio.add(button_sobre, button_duvidas)

@estagioBot.message_handler(commands=['start'])
def handle_start(message):
    texto = "Olá, seja bem vindo! \nEsse é o Orienta Bot. para prosseguir, escolha uma das opções"
    estagioBot.reply_to(message, texto, reply_markup=keyboardInicio)

estagioBot.polling()