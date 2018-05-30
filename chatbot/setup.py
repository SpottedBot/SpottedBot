from .base_message import BaseMessage


class MessengerSetup(BaseMessage):
    def __init__(self, greeting, get_started_payload):
        data = {
            'greeting': [
                {
                    "locale": "default",
                    "text": greeting
                }
            ],
            'get_started': {
                'payload': get_started_payload
            }
        }
        super().__init__(**data)

    def send(self, **kwargs):
        super().send('me', 'messenger_profile', **kwargs)


def setup_messenger(greeting='Olá, {{user_first_name}}', get_started_payload='get_started'):
    m = MessengerSetup(greeting, get_started_payload)
    return m.send()
