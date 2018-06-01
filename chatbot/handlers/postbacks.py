from chatbot.messages import simple_message, template_message
from .handover import pass_thread_control
from chatbot.models import Chat
from celery import chain
from chatbot.personality import PersonalityGen

from django.conf import settings
from django.urls import reverse


def postback_handler(uid, postback):
    handlers = {
        'get_started': greetings,
        'base_query': base_query,
        'send_spotted': send_spotted,
        'ask_question': ask_question,
        'raw_solution_found': raw_solution_found,
        'raw_solution_not_found': raw_solution_not_found,
        'other': other
    }
    if not Chat.is_standby(uid):
        handlers[postback['payload']](uid)


def greetings(uid):
    p = PersonalityGen()
    greet = p.greetings
    follow = p.polite_followback
    hold = p.hold_spotted
    lets = p.lets_talk
    message = f'{greet} {follow}\n{hold} {lets}'
    simple_message(uid, message)
    base_query(uid)


def base_query(uid):
    p = PersonalityGen()
    message = p.base_messages
    buttons = [
        {
            'type': 'postback',
            'title': 'Mandar spotted',
            'payload': 'send_spotted'
        },
        {
            'type': 'postback',
            'title': 'Dúvidas ou problemas',
            'payload': 'ask_question'
        },
        {
            'type': 'postback',
            'title': 'Nenhum dos dois!',
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
    p = PersonalityGen()
    message = p.send_spotted1
    message2 = p.send_spotted2
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
    message = 'Conta aí qual é a sua dúvida :)'
    simple_message.delay(uid, message)
    Chat.set_accept_raw(uid)


def raw_solution_found(uid):
    message = 'Foi um prazer ajudar!'
    Chat.set_raw_solution_found(uid)
    simple_message.delay(uid, message)


def raw_solution_not_found(uid):
    message = 'Então espera um pouco que alguém já vem te ajudar <3'
    Chat.set_raw_solution_not_found(uid)
    chain(simple_message.si(uid, message), pass_thread_control.si(uid))()


def other(uid):
    message = 'Sem problemas! Fala aí como podemos te ajudar!'
    chain(simple_message.si(uid, message), pass_thread_control.si(uid))()
