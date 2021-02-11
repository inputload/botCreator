from models.blocks import *

events = {
    'start': [TextMessage('start message 1'), TextMessage('start message 2')],
    CommandTriger('hop'): [TextMessage('hep', Keyboard(['hohoho', 'bugaga']))],
    CommandTriger('hep'): [TextMessage('hop', Keyboard([]))],
    TextTriger('hohoho'): [TextMessage('1111')],
    TextTriger('bugaga'): [TextMessage('2222')],
}

Bot(token="1627788403:AAFfcUm-x1oQS1INacBb8f_UGLhnhagMmr8", events=events).start()