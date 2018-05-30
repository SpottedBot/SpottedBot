from chatbot.messages import simple_message, template_message
from .handover import pass_thread_control
from chatbot.models import Chat
from celery import chain

from django.conf import settings
from django.urls import reverse


def postback_handler(uid, postback):
    handlers = {
        'get_started': greetings,
        'base_query': base_query,
        'send_spotted': send_spotted,
        'ask_question': ask_question,
        'other': other
    }
    if not Chat.is_standby(uid):
        handlers[postback['payload']](uid)


def greetings(uid):
    message = 'Olar! Tudo bom?\nSegura esse spotted aí! Vamos conversar primeiro\n:)'
    simple_message(uid, message)
    base_query(uid)


def base_query(uid):
    message = 'Me fala como que eu posso te ajudar'
    buttons = [
        {
            'type': 'postback',
            'title': 'Mandar spotted',
            'payload': 'send_spotted'
        },
        {
            'type': 'postback',
            'title': 'Tirar dúvidas',
            'payload': 'ask_question'
        },
        {
            'type': 'postback',
            'title': 'Outro',
            'payload': 'other'
        },
    ]
    payload = {
        'template_type': 'button',
        'text': message,
        'buttons': buttons
    }
    template_message.delay(uid, payload)


def send_spotted(uid):
    message = 'Não digite ainda!\nNão aceitamos mais spotteds por inbox (privacidade e tal)'
    message2 = 'Agora você manda pelo nosso site. Lá sua privacidade é garantida :)'
    url = settings.ROOT_URL + reverse('custom_auth:facebook_login')
    button = {
        'type': 'web_url',
        'url': url,
        'title': 'Enviar now!'
    }
    payload = {
        'template_type': 'button',
        'text': message2,
        'buttons': [button]
    }
    chain(simple_message.si(uid, message), template_message.si(uid, payload))()


def ask_question(uid):
    message = 'Conta qual é a sua dúvida que nós te responderemos em breve :)'
    simple_message.delay(uid, message)
    pass_thread_control.delay(uid)


def other(uid):
    message = 'Sem problemas! Fala aí como podemos te ajudar!'
    simple_message.delay(uid, message)
    pass_thread_control.delay(uid)
