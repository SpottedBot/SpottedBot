from chatbot.base_message import BaseMessage
from chatbot.models import Chat
from celery import shared_task


class ThreadMessage(BaseMessage):
    def __init__(self, uid, target_id=None):
        data = {'recipient': {'id': uid}}
        if target_id:
            data['target_app_id'] = target_id
        super().__init__(**data)

    def send(self, connection, **kwargs):
        super().send('me', connection, **kwargs)


@shared_task
def pass_thread_control(uid, target_id='263902037430900'):
    t = ThreadMessage(uid, target_id)
    t.send('pass_thread_control')
    Chat.set_standby(uid)


@shared_task
def received_thread_control(uid):
    Chat.set_active(uid)


@shared_task
def take_thread_control(uid):
    t = ThreadMessage(uid)
    t.send('take_thread_control')
    Chat.set_active(uid)


@shared_task
def request_thread_control(uid):
    t = ThreadMessage(uid)
    t.send('request_thread_control')


def handover_handler(uid, data):
    received_thread_control.delay(uid)
