from django.test import TestCase
from django.test import Client
from django.urls import reverse
import json

'''
# Create your tests here.
def test_feedback():
	client = Client()
	response = client.post(reverse(viewname='weather_app:feedback'), {"firstName": "Testing",
																	  "lastName": "123",
																	  "email": "test@testing.com",
																	  "feedback": "testing for test",
																	  "csrfmiddlewaretoken": "testing"})
	assert response.status_code == 200
'''

'''
def test_weather():
	client = Client()
	response = client.post(reverse(viewname='weather_app:weather'), {"latitude": "51.5072",
																	 "longitude": "-0.1276"})
	assert response.status_code == 200
'''

'''
def test_chatbot():
	client = Client()
	response = client.post(reverse(viewname='chat_bot:chat_bot'), {'question': 'hello'})

	assert response.status_code == 200
'''
