import telebot
import logging
import random
from threading import Thread

logging.basicConfig(level=logging.INFO, format='%(message)s')


class Bot:
    def __init__(self, token: str, events):
        self.bot = telebot.TeleBot(token=token, parse_mode='markdown')
        self.events = events
        self.name = f"{self.bot.get_me().username}"
        self.activator = Thread(target=lambda: self.bot.polling(none_stop=True))
        self.status = "Working"
        self.todo()

    def start(self):
        self.activator.start()
        self.status = "Working"
        logging.info(f"{self.name} started")

    def stop(self):
        self.activator = Thread(target=lambda: self.bot.polling(none_stop=True))
        self.status = "Stopped"
        logging.info(f"{self.name} stoped")

    def todo(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            for event in self.events['start']:
                if event.type == 'send_message':
                    event.do(self=self.bot, chat_id=message.chat.id, text=event.data['text'])

        def triger(command, events):
            @self.bot.message_handler(commands=[command])
            def do(message):
                for event in events:
                    if event.type == 'send_message':
                        event.do(self=self.bot, chat_id=message.chat.id, text=event.data['text'])

        events = self.events.copy()
        events.pop('start')

        for event in events:
            Thread(target=triger, args=(event.data['command'], events[event])).start()


class CommandTriger:
    def __init__(self, command):
        self.data = {'command': command}
        self.type = 'command_triger'


class TextMessage:
    def __init__(self, text, keyboard):
        self.do = telebot.TeleBot.send_message
        self.data = {'text': text}
        self.type = 'send_message'
