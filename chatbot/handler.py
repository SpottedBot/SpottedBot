from .handlers import standby, messaging

from collections import OrderedDict


def handler(messages):
    handlers = OrderedDict([
        ('standby', standby.standby_handler),
        ('messaging', messaging.message_and_postback_and_handover_handler)
    ])
    for message in messages:
        for handle_key, handle_func in handlers.items():
            if handle_key in message.keys():
                handle_func(message[handle_key])
