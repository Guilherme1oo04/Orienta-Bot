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
    texto = "É um encontro mensal com o orientador para avaliar o seu desempenho durante o mês. Acontece, geralmente, no final do mês e você deve levar a frequência assinada pelo seu supervisor. Também é um  momento para discutir questões acerca do projeto social da classe."

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
    texto = "A frequência deve ser assinada pelo supervisor, orientador de estágio, estudante e gestor da escola. O estagiário não tem direito a faltas abonadas (o abono de faltas se trata de um direito que o trabalhador tem de faltar ao trabalho, sem que haja descontos no seu salário). Atestados justificam as ausências, mas as faltas deverão ser repostas."
    estagioBot.reply_to(message, texto)

    texto2 = "ATENÇÃO: \n - A frequência deve ser assinada de caneta azul, não conter rasuras, manchas, nem estar amassado. \n - O estagiário deverá solicitar a assinatura diária da frequência pelo supervisor. \n - O aluno que entregar a frequência fora do prazo, receberá o valor da bolsa somente no mês seguinte."
    estagioBot.reply_to(message, texto2)

    estagioBot.reply_to(message, "Deseja ver outras dúvidas?", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "frequencia")
def callback_frequencia(callback):
    command_frequencia(callback.message)


@estagioBot.message_handler(commands=["projetoSocial"])
def command_projetoSocial(message):
    texto = "Projetos sociais são trabalhos desenvolvidos de modo a impactar positivamente no desenvolvimento social, econômico ou cultural de uma comunidade, sociedade ou grupo. É uma forma de avaliação necessária para a conclusão do curso. Cada curso deverá desenvolver um projeto em conjunto com a classe."
    
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

    texto = 'A autoavaliação é um espaço que você pode acessar através da plataforma SICE. Neste espaço, você responderá a perguntas como "O que aprendi?", "O que precisa ser aprimorado?" e "Qual foi a contribuição do estágio para o meu desenvolvimento pessoal?". É essencial completar essa avaliação todos os meses imediatamente após a *_mediação_*(/mediacao). Uma sugestão: procure responder usando um computador, já que o sistema pode não salvar as informações se você preencher a partir de um celular.'
    estagioBot.reply_to(message, texto, parse_mode="Markdown")

    texto2 = 'A seguir um tutorial para acessar a autoavaliação:\n\n1. Acesse o link: https://sice.seduc.ce.gov.br/sice/login.jsf\n2. Siga os passos indicados:'
    estagioBot.reply_to(message, texto2)

    path = os.path.dirname(os.path.realpath(__file__))
    assets_path = os.path.join(path, 'assets')

    img1 = open(str(os.path.join(assets_path, "img-seçao-estagiario.png")), "rb")
    estagioBot.send_photo(message.chat.id, img1)

    img2 = open(str(os.path.join(assets_path, "img-seçao-autoAvaliaçao.png")), "rb")
    estagioBot.send_photo(message.chat.id, img2)

    texto3 = "3. Pronto! Agora basta selecionar o ícone indicado e responder as questões. Lembre-se de salvar suas respostas."
    estagioBot.reply_to(message, texto3)

    img3 = open(str(os.path.join(assets_path, "img-autoAvaliaçao-novo.png")), "rb")
    estagioBot.send_photo(message.chat.id, img3)

    estagioBot.reply_to(message, "Deseja ver outras dúvidas?", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "autoAvaliacao")
def callback_autoAvaliacao(callback):
    command_autoAvaliacao(callback.message)


@estagioBot.message_handler(commands=["avaliacaoOrientador"])
def command_avaliacaoOrientador(message):

    texto = 'A avaliação do orientador é um espaço que você pode acessar através da plataforma SICE. Neste espaço, você responderá a perguntas relacionadas ao seu orientador como "Realizou orientações antes do início do estágio?", "Esclarece as dúvidas?" e "Faz acompanhamento individual?". É essencial completar essa avaliação todos os meses imediatamente após a *_mediação_*(/mediacao). Uma sugestão: procure responder usando um computador, já que o sistema pode não salvar as informações se você preencher a partir de um celular.'
    estagioBot.reply_to(message, texto, parse_mode="Markdown")

    texto2 = 'A seguir um tutorial para acessar a avaliação do orientador:\n\n1. Acesse o link: https://sice.seduc.ce.gov.br/sice/login.jsf\n2. Siga os passos indicados:'
    estagioBot.reply_to(message, texto2)

    path = os.path.dirname(os.path.realpath(__file__))
    assets_path = os.path.join(path, 'assets')

    img1 = open(str(os.path.join(assets_path, "img-seçao-estagiario.png")), "rb")
    estagioBot.send_photo(message.chat.id, img1)

    img2 = open(str(os.path.join(assets_path, "img-seçao-avaliaçaoOrientador.png")), "rb")
    estagioBot.send_photo(message.chat.id, img2)

    texto3 = "3. Pronto! Agora basta selecionar o ícone indicado e responder as questões. Lembre-se de salvar suas respostas."
    estagioBot.reply_to(message, texto3)

    img3 = open(str(os.path.join(assets_path, "img-avaliaçaoOrientador-novo.png")), "rb")
    estagioBot.send_photo(message.chat.id, img3)

    estagioBot.reply_to(message, "Deseja ver outras dúvidas?", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "avaliacaoOrientador")
def callback_avaliacaoOrientador(callback):
    command_avaliacaoOrientador(callback.message)     


@estagioBot.message_handler(commands=["envioRelatorio"])
def command_envioRelatorio(message):

    texto = "O Relatório Final do Estágio é um espaço que você pode acessar através da plataforma SICE. Neste espaço, você enviará o arquivo correspondente ao seu relatório de conclusão do curso. É essencial você se certificar que a estrutura e o modelo do seu texto está correto, visite /dicasRelatorio."
    estagioBot.reply_to(message, texto)

    texto2 = 'A seguir um tutorial para acessar o envio do relatório final de estágio:\n\n1. Acesse o link: https://sice.seduc.ce.gov.br/sice/login.jsf\n2. Siga os passos indicados:'
    estagioBot.reply_to(message, texto2)

    path = os.path.dirname(os.path.realpath(__file__))
    assets_path = os.path.join(path, 'assets')

    img1 = open(str(os.path.join(assets_path, "img-seçao-estagiario.png")), "rb")
    estagioBot.send_photo(message.chat.id, img1)

    img2 = open(str(os.path.join(assets_path, "img-seçao-relatorioFinal.png")), "rb")
    estagioBot.send_photo(message.chat.id, img2)

    texto3 = "3. Pronto! Agora basta selecionar o ícone indicado e anexar seu documento."
    estagioBot.reply_to(message, texto3)

    img3 = open(str(os.path.join(assets_path, "img-relatorioFinal-novo.png")), "rb")
    estagioBot.send_photo(message.chat.id, img3)

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
    texto = "Aqui estão algumas dicas úteis para ajudá-lo a escrever um relatório de acordo com as normas da ABNT:"
    estagioBot.reply_to(message, texto)

    texto2 = "1. Entenda o propósito do relatório: Antes de começar, compreenda o motivo pelo qual está escrevendo o relatório e qual é o seu público-alvo. Isso o ajudará a estruturar o conteúdo de forma adequada."
    estagioBot.reply_to(message, texto2)

    texto3 = "2. Organize seu tempo: Planeje com antecedência para ter tempo suficiente para pesquisa, redação e revisão do relatório. Evite deixar tudo para a última hora."
    estagioBot.reply_to(message, texto3)

    texto4 = "3. Siga a estrutura da ABNT: Use a estrutura padrão da ABNT, conforme mencionada na resposta anterior. Certifique-se de que todos os elementos, como capa, sumário, referências, etc., estejam presentes."
    estagioBot.reply_to(message, texto4)

    texto5 = "4. Seja claro e conciso: Evite linguagem excessivamente técnica. Use uma linguagem clara e evite jargões que possam não ser compreendidos pelo seu público."
    estagioBot.reply_to(message, texto5)

    texto6 = "5. Siga rigorosamente as *regras de formatação da ABNT* em relação a margens(/relatorioEstrutura), espaçamento, fonte, numeração de páginas, citações, e outros detalhes de estilo. Utilize um editor de texto que ofereça suporte a essas formatações."
    estagioBot.reply_to(message, texto6, parse_mode="Markdown")

    texto7 = "Lembre-se de que um relatório acadêmico deve ser escrito de forma profissional e imparcial, evitando opiniões pessoais a menos que seja solicitado."
    estagioBot.reply_to(message, texto7)

    estagioBot.reply_to(message, "Deseja ver outras dúvidas?", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "relatorioAbnt")
def callback_relatorioAbnt(callback):
    command_relatorioAbnt(callback.message)


@estagioBot.message_handler(commands=["relatorioEstrutura"])
def command_relatorioEstrutura(message):
    texto = "Aqui estão as principais diretrizes relacionadas a margens, espaçamento, fonte, numeração de páginas, citações e outros detalhes de estilo:"
    estagioBot.reply_to(message, texto)

    texto2 = "1. Margens:\n - As margens devem seguir o seguinte padrão:\n  - Superior: 3 cm\n  - Inferior: 2 cm.\n  - Esquerda: 3 cm.\n  - Direita: 2 cm.\n"
    estagioBot.reply_to(message, texto2)

    texto3 = "2. Espaçamento:\n - O texto deve ser digitado com espaçamento de 1,5 entre linhas."
    estagioBot.reply_to(message, texto3)

    texto4 = "3. Fonte:\n - A fonte recomendada é Arial ou Times New Roman, tamanho 12."
    estagioBot.reply_to(message, texto4)

    texto5 = "4. Numeração de Páginas:\n - A numeração de páginas deve ser posicionada no canto superior direito da página, a 2 cm da borda superior.\n - A contagem começa a partir da folha de rosto, mas as páginas preliminares (como capa, sumário e lista de figuras) não devem ser numeradas. A contagem de página deve começar na primeira página do conteúdo (introdução, por exemplo), em algarismos arábicos."
    estagioBot.reply_to(message, texto5)

    texto6 = "5. Citações:\n - As citações diretas devem ser colocadas entre aspas e indicar a autoria, o ano e a página (se aplicável).\n -  Citações longas (com mais de três linhas) devem ser destacadas com recuo à esquerda de 4 cm, sem aspas, com espaçamento simples e fonte tamanho 10.\n - As referências bibliográficas completas devem ser listadas nas referências, seguindo as normas da ABNT."
    estagioBot.reply_to(message, texto6)

    texto7 = "6. Referências Bibliográficas:\n - As referências devem seguir um formato específico, dependendo do tipo de fonte (livros, artigos, sites, etc.). Certifique-se de consultar a norma da ABNT correspondente para cada tipo de fonte. Normalmente, as referências são organizadas em ordem alfabética."
    estagioBot.reply_to(message, texto7)

    texto8 = "3. Títulos das Seções:\n - Os títulos das seções (introdução, metodologia, resultados, conclusão, etc.) devem ser escritos em maiúsculas e minúsculas, em negrito, com alinhamento à esquerda e sem numeração."
    estagioBot.reply_to(message, texto8)

    texto9 = "Lembre-se de que essas são diretrizes gerais da ABNT. As instituições acadêmicas podem ter suas próprias variações e regras específicas. Portanto, é importante consultar as normas da ABNT vigentes e as diretrizes específicas da sua instituição para garantir a conformidade total."
    estagioBot.reply_to(message, texto9)

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
    texto = "O período total de estágio pode durar até 6 meses, porém há algumas divisões entre as atividades, não restritas somente ao trabalho em campo. \n\nOs cursos de Informática e Fruticultura possuem 300h de estágio em campo. \nOs cursos de Administração e Finanças possuem 250h de estágio em campo. \n\nAlém disso, atividades como: Semana preparatória, relatórios, projeto social e mediação, possuem uma carga horária total de 100h."

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
    texto1 = "SEGUROS CONTRA ACIDENTES PESSOAIS: \nO inciso IV do Artigo 9° da Lei n° 11.788/2008 e o parágrafo 4° do Artigo 5° do Decreto N°. 30.933/12, todos os estudantes ao estagiários estarão cobertos por seguro contra acidentes pessoais."
    estagioBot.reply_to(message, texto1)

    texto2 = "O seguro contra acidentes pessoais será concedido a todos os estudantes que tiverem seus estágios formalizados através de TCE entre a escola, o estudante e a concedente de estágio e mediante a inserção do estudante na apólice no SICE."
    estagioBot.reply_to(message, texto2)

    texto3 = "FREQUÊNCIA DOS ESTUDANTES: \nO estagiário não tem direito a faltas abonadas (o abono de faltas se trata de um direito que o trabalhador tem de faltar ao trabalho, sem que haja descontos no seu salário). Atestados justificam as ausências, mas as faltas deverão ser repostas."
    estagioBot.reply_to(message, texto3)

    texto4 = "PRAZO DE DURAÇÃO DO ESTÁGIO: \nAté 6 (seis) meses consecutivos para os cursos com carga horária total de 400 (quatrocentas) horas. Administração, Finanças, Fruticultura, Informática."
    estagioBot.reply_to(message, texto4)

    estagioBot.reply_to(message, "Deseja ver outras dúvidas?", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "juridico")
def callback_juridico(callback):
    command_juridico(callback.message)

@estagioBot.message_handler(commands=["bolsaEstagio"])
def command_bolsaEstagio(message):
    texto = "A bolsa estágio é um valor recebido mensalmente. Seu valor é calculado com base nas horas trabalhadas por mês e multiplicado por um valor que pode variar anualmente, em 2023 o valor da hora é $ 4,52. \nPara calcular o valor que você receberá informe quantas horas foram trabalhadas:"

    estagioBot.reply_to(message, texto)
    estagioBot.register_next_step_handler(message, aguardar_valorBolsa)

def aguardar_valorBolsa(message):

    if (message.text.isnumeric()):
        valor_bolsa = float(message.text) * 4.54

        valor_bolsa = str(valor_bolsa).replace(".", ",")

        mensagem = f"Excelente, você receberá: R${valor_bolsa}"

    else:
        mensagem = "Número inválido, não é possível calcular o valor a receber!"

    estagioBot.reply_to(message, mensagem)
    estagioBot.reply_to(message, "Deseja ver outras dúvidas?", reply_markup=keyboardSN)
    
@estagioBot.callback_query_handler(func= lambda call: call.data == "bolsaEstagio")
def callback_bolsaEstagio(callback):
    command_bolsaEstagio(callback.message)


estagioBot.polling()