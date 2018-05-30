from .postbacks import postback_handler, base_query
from .handover import handover_handler
from chatbot.models import Chat


def message_handler(uid, message):
    if not Chat.is_standby(uid):
        # All messages are replied with the default postback
        base_query(uid)


def message_and_postback_and_handover_handler(messages):
    handlers = {
        'postback': postback_handler,
        'message': message_handler,
        'pass_thread_control': handover_handler
    }
    for message in messages:
        uid = message['sender']['id']
        for handle_key, handle_func in handlers.items():
            if handle_key in message.keys():
                handle_func(uid, message[handle_key])
