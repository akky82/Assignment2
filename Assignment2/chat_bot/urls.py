from django.urls import path
from . import views
from chat_bot.views import ChatBotView


app_name = "chat_bot"

urlpatterns = [
    path('chat_bot/', ChatBotView.as_view(), name="chat_bot"),
]
