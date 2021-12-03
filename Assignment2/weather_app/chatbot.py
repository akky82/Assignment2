from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from . import functions


weather_bot = ChatBot(name="Django")

chatbot_input = input("You: ")
# chatbot_response = weather_bot.get_reponse(chatbot_input)

keywords = chatbot_input.strip("?").split()
if "temperature" in keywords:
	lat = keywords[-2]
	lon = keywords[-1]
	resp = functions.call_weather(lat, lon)
	print(resp)
