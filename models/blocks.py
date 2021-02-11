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
                    event.do(self=self.bot, chat_id=message.chat.id, text=event.data)

        def command_triger(command, events):
            @self.bot.message_handler(commands=[command])
            def do(message):
                for event in events:
                    keys = False
                    if event.keys:
                        keys = event.keys.data
                    if event.type == 'send_message':
                        event.do(self=self.bot, chat_id=message.chat.id, text=event.data, reply_markup=keys)

        def text_triger(triger, events):
            @self.bot.message_handler(content_types=["text"], func=lambda message: message.text == triger)
            def do(message):
                for event in events:
                    keys = False
                    if event.keys:
                        keys = event.keys.data
                    if event.type == 'send_message':
                        event.do(self=self.bot, chat_id=message.chat.id, text=event.data, reply_markup=keys)

        events = self.events.copy()
        events.pop('start')

        for event in events:
            if event.type == 'command_triger':
                Thread(target=command_triger, args=(event.data, events[event])).start()
            elif event.type == 'text_triger':
                Thread(target=text_triger, args=(event.data, events[event])).start()


class CommandTriger:
    def __init__(self, command):
        self.data = command
        self.type = 'command_triger'


class TextTriger:
    def __init__(self, triger):
        self.data = triger
        self.type = 'text_triger'


class TextMessage:
    def __init__(self, text, keyboard=''):
        self.do = telebot.TeleBot.send_message
        self.data = text
        self.keys = keyboard
        self.type = 'send_message'


class Keyboard:
    def __init__(self, buttons):
        self.type = 'keyboard'
        if buttons:
            data = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            for button in buttons:
                data.add(button)
        else:
            data = telebot.types.ReplyKeyboardRemove()
        self.data = data