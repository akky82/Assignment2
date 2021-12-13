import requests
from datetime import datetime
import json
import pytz
from django.shortcuts import render
from django.views import View
from .forms import ChatBotForm
from . import chat_bot
from django.views.decorators.csrf import csrf_exempt

api_key = "6a0c0dd6f5fe299a55e79d388afb256f"
file_path = 'chat_bot/files/qa_data.json'


# Function to call openweather API using either the city name or longitude/latitude
def call_weather(lat, lon, *city):
	if city:
		url = 'http://api.openweathermap.org/data/2.5/weather?q=%s&units=metric&appid=%s' % (city[0], api_key)
	else:
		url = 'http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&units=metric&appid=%s' % (lat, lon, api_key)

	resp = requests.get(url)
	data = json.loads(resp.text)
	print(data)
	return data


# Function to ask the chatbot a question, if general in the given json it will give a response, otherwise make
# an API call based on information form the user
def ask_question(request):
	question = ''
	error_msg = "I'm sorry, I don't understand the question."
	reply = error_msg
	with open(file_path, 'r') as f:
		qa_data = f.read()

	if request:
		form = ChatBotForm(request)
		if form.is_valid():
			question = form.cleaned_data['question']
			if question in qa_data:
				reply = chat_bot.talk(question)
				return reply

			keywords = question.strip("?").split()
			# print(keywords)

			# Check whether the user is giving co-ordinates, if not, assume a city name, call_weather
			# using the appropriate arguments
			if "co-ords" in keywords or "co-ordinates" in keywords:
				print(keywords)
				lat = keywords[-2]
				lon = keywords[-1]
				weather_data = call_weather(lat, lon)
			else:
				city_name = str(keywords[-1])
				weather_data = call_weather(0, 0, city_name)

			# Check to see if the city name exists within the API database by checking for error 404
			if weather_data['cod'] == '404':
				reply = "Sorry, that city isn't in my database"
				return reply

			# Branch to respond based on keyword input by user, respond accordingly
			if "temperature" in keywords:
				reply = "The current temperature in " + weather_data['name'] \
						+ " is " + str(weather_data['main']['temp']) + "&deg;C"
			elif "humidity" in keywords:
				reply = "The current humidity in " + weather_data['name'] \
						+ " is " + str(weather_data['main']['humidity']) + "%"
			elif "conditions" in keywords or "description" in keywords:
				reply = "The current conditions in " + weather_data['name'] + " are " \
						+ str(weather_data['weather'][0]['description'])
			elif "sunrise" in keywords:
				sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M %p')
				reply = "The sunrise in " + weather_data['name'] + " should be at " + str(sunrise)
			elif "sunset" in keywords:
				sunset = datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M %p')
				# datetime_converted = datetime.now(pytz.timezone(weather_data['timezone']))
				# print(datetime_converted)
				# sunset = datetime.fromtimestamp(datetime_converted.strftime('%H:%M %p'))
				reply = "The sunset in " + weather_data['name'] + " should be at " + str(sunset)
			elif "weather" in keywords:
				reply = "The current conditions in " + weather_data['name'] + " are " \
						+ str(weather_data['weather'][0]['description']) + ", the temperature is " \
						+ str(weather_data['main']['temp']) + "&deg;C, and the humidity is "\
						+ str(weather_data['main']['humidity']) + "%"
			else:
				reply = error_msg

	return reply


class ChatBotView(View):
	@csrf_exempt
	def get(self, request):
		form = ChatBotForm()
		return render(request, 'chat_bot.html', {'form': form})

	@csrf_exempt
	def post(self, request):
		question = request.POST['question']
		reply = ask_question(request.POST)

		form = ChatBotForm()
		return render(request, 'chat_bot.html', {'form': form, 'question': question, 'reply': reply})
