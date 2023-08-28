import os
import telebot
from dotenv import load_dotenv

load_dotenv()

chave_api = os.environ["API_TOKEN"]

estagioBot = telebot.Telebot(token=chave_api)

estagioBot.polling()