from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json


# Read the questions from a JSON file and use them to train the chat bot
file_path = 'chat_bot/files/qa_data.json'
qa_data = ''
with open(file_path, 'r') as f:
    qa_data = json.load(f)

train = []

for i, j in enumerate(qa_data):
    train.append(j['question'])
    train.append(j['answer'])

chatbot = ChatBot('Django')
trainer = ListTrainer(chatbot)
trainer.train(train)


def talk(msg):
    return chatbot.get_response(msg)
