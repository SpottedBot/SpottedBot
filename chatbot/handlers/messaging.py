from .postbacks import postback_handler, base_query
from chatbot.messages import template_message, simple_message
from .handover import handover_handler, pass_thread_control
from chatbot.models import Chat
from api.api_interface import api_process_raw_bot_message
from celery import chain


def message_handler(uid, message):
    if Chat.is_standby(uid):
        # Ignore if, the user is standby
        return

    if not Chat.is_accepting_raw(uid):
        # If not accepting raw, return base
        return base_query(uid)

    # Set last sent raw message
    Chat.set_last_raw_message(uid, message['text'])
    # Process raw message
    response = api_process_raw_bot_message(message['text'])
    result = response['result']
    result_status = response['result_status']

    if result_status:
        # Some response was found
        buttons = [
            {
                'type': 'postback',
                'title': 'Era isso :)',
                'payload': 'raw_solution_found'
            },
            {
                'type': 'postback',
                'title': 'Não ajudou :(',
                'payload': 'raw_solution_not_found'
            }
        ]
        payload = {
            'template_type': 'button',
            'text': result,
            'buttons': buttons
        }
        return template_message.delay(uid, payload)

    # If no response was found, handover to human
    Chat.set_raw_solution_not_found(uid)
    message = 'Boa pergunta :p\nVou consultar os universitários e já volto'
    chain(simple_message.si(uid, message), pass_thread_control.si(uid))()


def message_and_postback_and_handover_handler(messages):
    handlers = {
        'postback': postback_handler,
        'message': message_handler,
        'pass_thread_control': handover_handler
    }
    for message in messages:
        sender = message['sender']['id']
        if message.get('message', False) and message['message'].get('is_echo', False):
            # Ignore echoes from the bot
            continue
        for handle_key, handle_func in handlers.items():
            if handle_key in message.keys():
                handle_func(sender, message[handle_key])
