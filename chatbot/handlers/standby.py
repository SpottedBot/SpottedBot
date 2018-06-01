from chatbot.models import Chat
from .messaging import message_and_postback_and_handover_handler


def standby_handler(messages):
    for message in messages:
        # if it is a standby message with only postback, then it is that
        # nasty case where facebook echoes the bots postback messages even
        # when it has the control of the chat
        if message.get('postback', False) and not message.get('message', False):
            # just ignore it
            continue

        sender = message['sender']['id']
        recipient = message['recipient']['id']
        is_echo = message['message'].get('is_echo', False)

        # If echo, the sender is the page
        if is_echo:
            # Reset standby counter
            Chat.set_standby(recipient)
            # append to log if log is enabled
            Chat.append_log(recipient, message['message'].get('text', ''), True)
            continue

        # if chat is not standby(expired)
        if not Chat.is_standby(sender) and Chat.check_expired(sender):
            message_and_postback_and_handover_handler([message])
            continue

        # If the chat is on standby
        if Chat.is_standby(sender):
            # reset standby
            Chat.set_standby(sender)
            # append to log if log is enabled
            Chat.append_log(sender, message['message'].get('text', ''), False)
            continue
