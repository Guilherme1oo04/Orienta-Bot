from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

def tecladoStart():

    keyboardStart = InlineKeyboardMarkup()
    button_start = InlineKeyboardButton("Start", callback_data="start")
    keyboardStart.add(button_start)

    return keyboardStart

def tecladoSimNao():
    
    keyboardSN = InlineKeyboardMarkup()
    buttonSim = InlineKeyboardButton("Sim", callback_data="Sim")
    buttonNao = InlineKeyboardButton("Não", callback_data="Nao")
    keyboardSN.add(buttonSim, buttonNao)

    return keyboardSN

def tecladoInicio():

    keyboardInicio = InlineKeyboardMarkup()
    button_sobre = InlineKeyboardButton('Sobre', callback_data="sobre")
    button_duvidas = InlineKeyboardButton('Duvidas', callback_data="duvidas")
    keyboardInicio.add(button_sobre, button_duvidas)

    return keyboardInicio

def tecladoDuvidas():

    keyboardDuvidas = InlineKeyboardMarkup()
    empresa = InlineKeyboardButton("Empresa", callback_data="empresa")
    checkEstagiario = InlineKeyboardButton("Checklist Estagiário", callback_data="checklistEstagio")
    sice = InlineKeyboardButton("Sice", callback_data="sice")
    dicasRelatorio = InlineKeyboardButton("Dicas Relatorio", callback_data="dicasRelatorio")
    mediacao = InlineKeyboardButton("Mediação", callback_data= "mediacao")
    bolsaEstagio = InlineKeyboardButton("Bolsa Estagio", callback_data="bolsaEstagio")
    keyboardDuvidas.row(empresa, checkEstagiario).row(sice, dicasRelatorio).row(mediacao, bolsaEstagio)

    return keyboardDuvidas

def tecladoSice():

    keyboardSice = InlineKeyboardMarkup()
    autoAvaliacao = InlineKeyboardButton("Auto Avaliação", callback_data="autoAvaliacao")
    avaliacaoOrientador = InlineKeyboardButton("Avaliação do Orientador", callback_data="avaliacaoOrientador")
    envioRelatorio = InlineKeyboardButton("Envio do Relatório", callback_data="envioRelatorio")
    keyboardSice.row(autoAvaliacao).row(avaliacaoOrientador).row(envioRelatorio)

    return keyboardSice