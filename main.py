import os
import telebot
import json
from keyboards import keyboards
from dotenv import load_dotenv

load_dotenv()

chave_api = os.environ["API_TOKEN"]

estagioBot = telebot.TeleBot(token=chave_api)

#Teclado Start
keyboardStart = keyboards.tecladoStart()

#Teclado Sim / Não
keyboardSN = keyboards.tecladoSimNao()

#feedback
keyboardFeedback = keyboards.tecladoFeedback()

@estagioBot.callback_query_handler(func= lambda call: call.data == "Sim" or call.data == "Nao")
def responseSN(callback):
    if (callback.data == "Sim"):
        command_duvidas(callback.message)

    elif (callback.data == "Nao"):
        estagioBot.reply_to(callback.message, "Obrigado por utilizar, Nos ajude dando um feedback", reply_markup=keyboardFeedback )


@estagioBot.message_handler(commands=['feedback'])
def command_feedback(message):
    estagioBot.reply_to(message, "Escreva seu feedback no teclado")
    estagioBot.register_next_step_handler(message, aguardar_feedback)

def aguardar_feedback(message):
    if message.text:
        feedbackText = message.text
        estagioBot.reply_to(message, "Feedback recebido: " + feedbackText)

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
    
@estagioBot.callback_query_handler(func= lambda call: call.data == "feedback")
def callback_feedback(callback):
    command_feedback(callback.message)
            

#Resposta padrão do bot caso não seja um comando
@estagioBot.message_handler(func=lambda message: not message.text.startswith('/'))
def handle_text(message):
    estagioBot.reply_to(message, 'Para utilizar o bot, comece com o botão start abaixo', reply_markup=keyboardStart)

@estagioBot.callback_query_handler(func= lambda call: call.data == "start")
def callback_start(callback):
    handle_start(callback.message)


#Teclado inicial

keyboardInicio = keyboards.tecladoInicio()

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


keyboardDuvidas = keyboards.tecladoDuvidas()

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
keyboardCheckList = keyboards.tecladoChecklist()

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


#Teclado sice
keyboardSice = keyboards.tecladoSice()
#Comandos - Sice
@estagioBot.message_handler(commands=["sice"])
def command_sice(message):

    texto = "O Sice é uma plataforma usada pelo estado do Ceará para enviar coisas relacionadas ao estágio \nEssas são as principais dúvidas relacionadas ao Sice"

    estagioBot.reply_to(message, texto, reply_markup=keyboardSice)

@estagioBot.callback_query_handler(func= lambda call: call.data == "sice")
def callback_sice(callback):
    command_sice(callback.message)


@estagioBot.message_handler(commands=["autoAvaliacao"])
def command_autoAvaliacao(message):

    texto = "explicação da auto avaliação"
    estagioBot.reply_to(message, texto)
    estagioBot.reply_to(message, "Deseja ver outras dúvidas?", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "autoAvaliacao")
def callback_autoAvaliacao(callback):
    command_autoAvaliacao(callback.message)


@estagioBot.message_handler(commands=["avaliacaoOrientador"])
def command_avaliacaoOrientador(message):

    texto = "explicação da avaliação do orientador"
    estagioBot.reply_to(message, texto)
    estagioBot.reply_to(message, "Deseja ver outras dúvidas?", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "avaliacaoOrientador")
def callback_avaliacaoOrientador(callback):
    command_avaliacaoOrientador(callback.message)     


@estagioBot.message_handler(commands=["envioRelatorio"])
def command_envioRelatorio(message):

    texto = "explicação do envio do relatório"
    estagioBot.reply_to(message, texto)
    estagioBot.reply_to(message, "Deseja ver outras dúvidas?", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "envioRelatorio")
def callback_envioRelatorio(callback):
    command_envioRelatorio(callback.message)


estagioBot.polling()