import os
import telebot
import json
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

chave_api = os.environ["API_TOKEN"]

estagioBot = telebot.TeleBot(token=chave_api)

#Teclado Start
keyboardStart = InlineKeyboardMarkup()
button_start = InlineKeyboardButton("Start", callback_data="start")
keyboardStart.add(button_start)

#Teclado Sim / Não
keyboardSN = InlineKeyboardMarkup()
buttonSim = InlineKeyboardButton("Sim", callback_data="Sim")
buttonNao = InlineKeyboardButton("Não", callback_data="Nao")
keyboardSN.add(buttonSim, buttonNao)

#feedback
keyboardFeedback = InlineKeyboardMarkup()
feedback = InlineKeyboardButton("Feedback", callback_data="feedback")
keyboardFeedback.add(feedback)

@estagioBot.callback_query_handler(func= lambda call: call.data == "Sim" or call.data == "Nao")
def responseSN(callback):
    if (callback.data == "Sim"):
        command_duvidas(callback.message)

    elif (callback.data == "Nao"):
        estagioBot.reply_to(callback.message, "Obrigado por utilizar, Nos ajude dando um feedback",reply_markup=keyboardFeedback )

@estagioBot.message_handler(commands=['feedback'])
def command_feedback(message):
    estagioBot.reply_to(message, "insert feedback msg")
    

    
@estagioBot.callback_query_handler(func= lambda call: call.data == "feedback")
def callback_feedback(callback):
    command_feedback(callback.message)
   

@estagioBot.message_handler(func=lambda message: True)
def handle_feedback(message):
    if message.text:
        feedbackText = message.text
        print("a")
        estagioBot.send_message(message.chat.id, "Feedback recebido: " + feedbackText)
        if not os.path.exists('user_message.json'):
            with open('user_message.json', 'w') as file:
                json.dump([], file)
        with open('user_message.json', 'r') as file:
            message_data = json.load(file)

            
        if not isinstance(message_data, list):
            message_data = []


        message_data.append({"user_message": feedbackText})

        

        with open('user_message.json','w') as file:
            json.dump(message_data, file)
            

#Resposta padrão do bot caso não seja um comando
@estagioBot.message_handler(func=lambda message: not message.text.startswith('/'))
def handle_text(message):
    estagioBot.reply_to(message, 'Para utilizar o bot, comece com o botão start abaixo', reply_markup=keyboardStart)

@estagioBot.callback_query_handler(func= lambda call: call.data == "start")
def callback_start(callback):
    handle_start(callback.message)


#Teclado inicial

keyboardInicio = InlineKeyboardMarkup()
button_sobre = InlineKeyboardButton('Sobre', callback_data="sobre")
button_duvidas = InlineKeyboardButton('Duvidas', callback_data="duvidas")
keyboardInicio.add(button_sobre, button_duvidas)

@estagioBot.message_handler(commands=['start'])
def handle_start(message):
    texto = "Olá, seja bem vindo! \nEsse é o Orienta Bot. para prosseguir, escolha uma das opções"
    estagioBot.reply_to(message, texto, reply_markup=keyboardInicio)


@estagioBot.message_handler(commands=['sobre'])
def command_sobre(message):
    estagioBot.reply_to(message, "Explicação do projeto")
    estagioBot.reply_to(message, "Deseja ver alguma das dúvidas respondidas?", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "sobre")
def callback_sobre(callback):
    command_sobre(callback.message)


keyboardDuvidas = InlineKeyboardMarkup()
empresa = InlineKeyboardButton("Empresa", callback_data="empresa")
checkEstagiario = InlineKeyboardButton("Checklist Estagiário", callback_data="checklistEstagio")
sice = InlineKeyboardButton("Sice", callback_data="sice")
dicasRelatorio = InlineKeyboardButton("Dicas Relatorio", callback_data="dicasRelatorio")
mediacao = InlineKeyboardButton("Mediação", callback_data= "mediacao")
bolsaEstagio = InlineKeyboardButton("Bolsa Estagio", callback_data="bolsaEstagio")
keyboardDuvidas.row(empresa, checkEstagiario).row(sice, dicasRelatorio).row(mediacao, bolsaEstagio)

@estagioBot.message_handler(commands=["duvidas"])
def command_duvidas(message):
    
    texto = "Essas são as dúvidas respondidas, escolha alguma para poder ver as respostas"
    estagioBot.reply_to(message, texto, reply_markup=keyboardDuvidas)

@estagioBot.callback_query_handler(func= lambda call: call.data == "duvidas")
def callback_duvidas(callback):
    command_duvidas(callback.message)


@estagioBot.message_handler(commands=["mediacao"])
def command_mediacao(message):
    
    texto = "INSERT MEDIAÇÃO TEXT"
    estagioBot.reply_to(message, texto, reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "mediacao")
def callback_mediacao(callback):
    command_mediacao(callback.message)
    
#teclado checklist
keyboardCheckList = InlineKeyboardMarkup()
frequencia = InlineKeyboardButton("Frequência", callback_data="frequencia")
projetoSocial = InlineKeyboardButton("Projeto Social", callback_data="SocialProject")
cronograma = InlineKeyboardButton("Cronograma", callback_data="cronograma")
avaliacao = InlineKeyboardButton("Avaliação", callback_data="avaliacao")
keyboardCheckList.row(frequencia, projetoSocial).row( cronograma, avaliacao)

@estagioBot.message_handler(commands=["checklistEstagio"])
def command_checklistEstagio(message):
    
    estagioBot.reply_to(message, "INSERT C. E. TEXT", reply_markup=keyboardCheckList)

@estagioBot.callback_query_handler(func= lambda call: call.data == "checklistEstagio")
def callback_checklistEstagio(callback):
    command_checklistEstagio(callback.message)


@estagioBot.message_handler(commands=["frequencia"])
def command_frequencia(message):
    
    estagioBot.reply_to(message, "INSERT frequencia TEXT", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "frequencia")
def callback_frequencia(callback):
    command_frequencia(callback.message)


@estagioBot.message_handler(commands=["SocialProject"])
def command_SocialProject(message):
    
    estagioBot.reply_to(message, "INSERT SocialProject TEXT", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "SocialProject")
def callback_SocialProjecta(callback):
    command_SocialProject(callback.message)


@estagioBot.message_handler(commands=["cronograma"])
def command_cronograma(message):
    
    estagioBot.reply_to(message, "INSERT cronograma TEXT", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "cronograma")
def callback_cronograma(callback):
    command_cronograma(callback.message)


@estagioBot.message_handler(commands=["avaliacao"])
def command_avaliacao(message):
    
    estagioBot.reply_to(message, "INSERT avaliacao TEXT", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "avaliacao")
def callback_avaliacao(callback):
    command_avaliacao(callback.message)


estagioBot.polling()