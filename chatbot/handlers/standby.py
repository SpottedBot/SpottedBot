from chatbot.models import Chat
from .messaging import message_and_postback_and_handover_handler


def standby_handler(messages):
    for message in messages:
        uid = message['sender']['id']
        # if chat is not standby(expired)
        if not Chat.is_standby(uid) and Chat.check_expired(uid):
            return message_and_postback_and_handover_handler([message])
        # ignore the first bugged messages and take control
        # if chat is standby, ignore
