import os
import telebot
import json
from keyboards import keyboards
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

chave_api = os.environ["API_TOKEN"]

estagioBot = telebot.TeleBot(token=chave_api)

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


#Teclado inicial
keyboardInicio = keyboards.tecladoInicio()

@estagioBot.message_handler(func=lambda message: not message.text.startswith('/'))
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

@estagioBot.message_handler(commands=["digiteDuvida"])
def command_digiteDuvida(message):
    texto = "Digite palavras-chave sobre as suas dúvidas, o bot tentará encontrar a(s) resposta(s) adequada(s) para o que deseja saber\n\nEvite digitar utilizando acentos e caracteres especiais, pois o bot não consegue identificá-los"
    estagioBot.reply_to(message, texto)
    estagioBot.register_next_step_handler(message, espera_duvida)

def espera_duvida(message):
    if (message.text != ""):
        texto_inicio = "Estes são os tópicos respondidos que podem te ajudar com a sua dúvida:\n"
        texto = ""

        palavras_chave = message.text.lower().split()
        dataframe = pd.read_csv("palavras_chave.csv")

        for palavra in palavras_chave:
            is_present = dataframe["palavra_chave"].isin([palavra])

            indices = dataframe.index[is_present].tolist()

            if (len(indices) > 0):
                if (texto_inicio not in texto):
                    texto += texto_inicio

                for x in indices:
                    linha = dataframe.iloc[int(x)]

                    if (linha.iloc[1].replace(" ", "") not in texto):
                        texto += f"\n{linha.iloc[1]}".replace(" ", "")

        if (texto != ""):
            estagioBot.reply_to(message, texto)
        else:
            estagioBot.reply_to(message, "Desculpe, não foi encontrado algo relacionado ao que você digitou!")



@estagioBot.callback_query_handler(func= lambda call: call.data == "digiteDuvida")
def callback_digiteDuvida(callback):
    command_digiteDuvida(callback.message)


@estagioBot.message_handler(commands=["mediacao"])
def command_mediacao(message):
    texto = "INSERT MEDIAÇÃO TEXT"

    estagioBot.reply_to(message, texto)
    estagioBot.reply_to(message, "Deseja ver outras dúvidas?", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "mediacao")
def callback_mediacao(callback):
    command_mediacao(callback.message)
    
#teclado checklist
keyboardCheckList = keyboards.tecladoChecklist()

@estagioBot.message_handler(commands=["checklistEstagio"])
def command_checklistEstagio(message):
    texto = "texto do checklist do estagio"
    
    estagioBot.reply_to(message, texto)
    estagioBot.reply_to(message, "Deseja ver outras dúvidas?", reply_markup=keyboardCheckList)

@estagioBot.callback_query_handler(func= lambda call: call.data == "checklistEstagio")
def callback_checklistEstagio(callback):
    command_checklistEstagio(callback.message)


@estagioBot.message_handler(commands=["frequencia"])
def command_frequencia(message):
    texto = "texto da frequencia"
    
    estagioBot.reply_to(message, texto)
    estagioBot.reply_to(message, "Deseja ver outras dúvidas?", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "frequencia")
def callback_frequencia(callback):
    command_frequencia(callback.message)


@estagioBot.message_handler(commands=["projetoSocial"])
def command_projetoSocial(message):
    texto = "texto do projeto social"
    
    estagioBot.reply_to(message, texto)
    estagioBot.reply_to(message, "Deseja ver outras dúvidas?", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "projetoSocial")
def callback_projetoSocial(callback):
    command_projetoSocial(callback.message)


@estagioBot.message_handler(commands=["cronograma"])
def command_cronograma(message):
    texto = "texto de cronograma"
    
    estagioBot.reply_to(message, texto)
    estagioBot.reply_to(message, "Deseja ver outras dúvidas?", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "cronograma")
def callback_cronograma(callback):
    command_cronograma(callback.message)


@estagioBot.message_handler(commands=["avaliacao"])
def command_avaliacao(message):
    texto = "Texto de avaliacao"
    
    estagioBot.reply_to(message, texto)
    estagioBot.reply_to(message, "Deseja ver outras dúvidas?", reply_markup=keyboardSN)

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


# Teclado - dicas de relatório
keyboardRelatorio = keyboards.tecladoDicasRelatorio()
# Dicas de relatório
@estagioBot.message_handler(commands=["dicasRelatorio"])
def command_dicasRelatorio(message):
    estagioBot.reply_to(message, "Essas são as dicas que posso te passar", reply_markup=keyboardRelatorio)

@estagioBot.callback_query_handler(func= lambda call: call.data == "dicasRelatorio")
def callback_dicasRelatorio(callback):
    command_dicasRelatorio(callback.message)


@estagioBot.message_handler(commands=["relatorioAbnt"])
def command_relatorioAbnt(message):
    texto = """
Margens e espaçamento:
As margens devem ser de 2,5 cm em todos os lados da página.
O texto deve ser digitado em espaço 1,5 entre as linhas.

Fonte e tamanho:
Utilize fonte Times New Roman ou Arial, tamanho 12 para o texto do relatório.
Para títulos e subtítulos, utilize fonte tamanho 14 ou 16, em negrito.

Numeração de páginas:
A numeração deve ser colocada no canto superior direito da página, a partir da introdução.
A capa e a folha de rosto não devem ser numeradas.

Citações e referências:
Utilize o sistema autor-data para citações no texto, seguindo as regras da ABNT.
Inclua uma lista de referências bibliográficas ao final do relatório, em ordem alfabética.

Notas de rodapé:
Utilize notas de rodapé para fornecer informações adicionais ou explicar termos técnicos.
As notas de rodapé devem ser numeradas sequencialmente e colocadas na parte inferior da página.

Ilustrações e tabelas:
As ilustrações (como gráficos, imagens e diagramas) devem ser numeradas e acompanhadas de uma legenda explicativa.
As tabelas também devem ser numeradas e ter uma legenda descritiva.
"""
    estagioBot.reply_to(message, texto)
    estagioBot.reply_to(message, "Deseja ver outras dúvidas?", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "relatorioAbnt")
def callback_relatorioAbnt(callback):
    command_relatorioAbnt(callback.message)


@estagioBot.message_handler(commands=["relatorioEstrutura"])
def command_relatorioEstrutura(message):
    texto = """
Capa e Folha de Rosto:
A capa deve conter o nome da instituição, título do relatório, nome do autor, local e data.
A folha de rosto deve conter as mesmas informações da capa, além do nome do orientador e do curso.

Sumário:
O sumário é essencial para organizar o conteúdo do relatório. Ele deve listar os títulos e subtítulos das seções, com a indicação das páginas correspondentes.

Introdução:
Na introdução, apresente o contexto do estágio, o objetivo do relatório e a importância do trabalho realizado.

Desenvolvimento:
Divida o relatório em seções e subseções, de acordo com a estruturação do seu estágio.
Explique as atividades desenvolvidas, os métodos utilizados e os resultados obtidos.
Utilize referências bibliográficas para fundamentar suas informações e citações.

Conclusão:
Na conclusão, faça um resumo dos principais resultados alcançados no estágio.
Avalie o cumprimento dos objetivos propostos e discuta os aprendizados adquiridos durante o período.
"""
    estagioBot.reply_to(message, texto)
    estagioBot.reply_to(message, "Deseja ver outras dúvidas?", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "relatorioEstrutura")
def callback_relatorioEstrutura(callback):
    command_relatorioEstrutura(callback.message)


# Teclado Empresa
keyboardEmpresa = keyboards.tecladoEmpresa()
# Comando Empresa
@estagioBot.message_handler(commands=["empresa"])
def command_empresa(message):
    texto = "Essas são algumas dúvidas relacionadas à empresas conectadas ao estágio"

    estagioBot.reply_to(message, texto, reply_markup=keyboardEmpresa)

@estagioBot.callback_query_handler(func= lambda call: call.data == "empresa")
def callback_empresa(callback):
    command_empresa(callback.message)

@estagioBot.message_handler(commands=["cargaHoraria"])
def command_cargaHoraria(message):
    texto = "texto carga horaria"

    estagioBot.reply_to(message, texto)
    estagioBot.reply_to(message, "Deseja ver outras dúvidas?", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "cargaHoraria")
def callback_cargaHoraria(callback):
    command_cargaHoraria(callback.message)

@estagioBot.message_handler(commands=["processoSeletivo"])
def command_processoSeletivo(message):
    texto = "texto processo seletivo"

    estagioBot.reply_to(message, texto)
    estagioBot.reply_to(message, "Deseja ver outras dúvidas?", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "processoSeletivo")
def callback_processoSeletivo(callback):
    command_processoSeletivo(callback.message)

@estagioBot.message_handler(commands=["juridico"])
def command_juridico(message):
    texto = "texto juridico"

    estagioBot.reply_to(message, texto)
    estagioBot.reply_to(message, "Deseja ver outras dúvidas?", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "juridico")
def callback_juridico(callback):
    command_juridico(callback.message)

@estagioBot.message_handler(commands=["bolsaEstagio"])
def command_bolsaEstagio(message):
    texto = "A bolsa estágio é um valor em dinheiro que o estagiário recebe pelas 300 horas trabalhadas. Esse valor é dividido e enviado para o estagiário de acordo com as horas que ele estagiou no mês. \n\nPara saber quanto irá ganhar, digite o tempo(em horas) que você estagiou durante o mês:"

    estagioBot.reply_to(message, texto)
    estagioBot.register_next_step_handler(message, aguardar_valorBolsa)

def aguardar_valorBolsa(message):

    if (message.text.isnumeric()):
        valor_bolsa = float(message.text) * 4.54

        valor_bolsa = str(valor_bolsa).replace(".", ",")

        mensagem = f"Você receberá: R${valor_bolsa}"

    else:
        mensagem = "Número inválido, não é possível calcular o valor a receber!"

    estagioBot.reply_to(message, mensagem)
    estagioBot.reply_to(message, "Deseja ver outras dúvidas?", reply_markup=keyboardSN)
    
@estagioBot.callback_query_handler(func= lambda call: call.data == "bolsaEstagio")
def callback_bolsaEstagio(callback):
    command_bolsaEstagio(callback.message)


estagioBot.polling()