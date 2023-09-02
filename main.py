import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv()

chave_api = os.environ["API_TOKEN"]

estagioBot = telebot.TeleBot(token=chave_api)

#Teclado Start
keyboardStart = ReplyKeyboardMarkup(resize_keyboard=True)
button_start = KeyboardButton("/start")
keyboardStart.add(button_start)

#Teclado Sim / Não
keyboardSN = ReplyKeyboardMarkup(resize_keyboard=True)
buttonSim = KeyboardButton("Sim")
buttonNao = KeyboardButton("Não")
keyboardSN.add(buttonSim, buttonNao)

#Resposta padrão do bot caso não seja um comando
@estagioBot.message_handler(func=lambda message: not message.text.startswith('/'))
def handle_text(message):
    estagioBot.reply_to(message, 'Para utilizar o bot, comece com o botão /start abaixo', reply_markup=keyboardStart)

#Teclado inicial
keyboardInicio = ReplyKeyboardMarkup(resize_keyboard=True)
button_sobre = KeyboardButton('/sobre')
button_duvidas = KeyboardButton('/duvidas')
keyboardInicio.add(button_sobre, button_duvidas)

@estagioBot.message_handler(commands=['start'])
def handle_start(message):
    texto = "Olá, seja bem vindo! \nEsse é o Orienta Bot. para prosseguir, escolha uma das opções"
    estagioBot.reply_to(message, texto, reply_markup=keyboardInicio)


@estagioBot.message_handler(commands=['sobre'])
def command_sobre(message):
    estagioBot.reply_to(message, "Explicação do projeto")
    estagioBot.reply_to(message, "Deseja ver alguma das dúvidas respondidas?", reply_markup=keyboardSN)
    estagioBot.register_next_step_handler(message, responseSN)

def responseSN(message):
    if (message.text == "Sim"):
        command_duvidas(message)

    elif (message.text == "Não"):
        estagioBot.reply_to(message, "Obrigado por utilizar, Nos ajude dando um feedback")

@estagioBot.message_handler(commands=["duvidas"])
def command_duvidas(message):
    estagioBot.reply_to(message, "Duvidas")

estagioBot.polling()