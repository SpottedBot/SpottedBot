import time as t
from .base_message import BaseMessage
from celery import shared_task


class Message(BaseMessage):
    def __init__(self, uid, messaging_type='RESPONSE'):
        data = {'recipient': {'id': uid}}
        if messaging_type:
            data['messaging_type'] = messaging_type
        super().__init__(**data)

    def send_message(self, text='', attachment_type='', attachment_payload='', quick_replies=[], **kwargs):
        self._message = {}
        if text:
            self._message['text'] = text
        if attachment_type:
            if attachment_type == 'template':
                self._message['attachment'] = {
                    'type': attachment_type,
                    'payload': attachment_payload
                }
            elif attachment_type in ['image', 'audio', 'video', 'file']:
                self._message['attachment'] = {
                    'type': attachment_type,
                    'payload': {'url': attachment_payload}
                }
            else:
                raise ValueError('Attachment must be of type image, audio, video, file or template')

        if quick_replies:
            self._message['quick_replies'] = quick_replies
        if not self._message:
            raise ValueError('Message must be defined')
        self.message = self._message
        self.data.append('message')
        self.send(**kwargs)

    def send_action(self, typing=True, **kwargs):
        self._action = ('typing_on' if typing else 'typing_off')
        self.sender_action = self._action
        self.data.append('sender_action')
        self.send(**kwargs)

    def mark_read(self, **kwargs):
        self._action = 'mark_seen'
        self.sender_action = self._action
        self.data.append('sender_action')
        self.send(**kwargs)

    def send(self, **kwargs):
        super().send('me', 'messages', **kwargs)


def typing(uid, type_on=True):
    m = Message(uid)
    m.send_action(type_on)


def sim_typing(uid, time):
    typing(uid)
    t.sleep(time)


@shared_task
def simple_message(uid, message):
    sim_typing(uid, min(5, len(message) / 50))
    m = Message(uid)
    m.send_message(message)


@shared_task
def attachment_message(uid, m_type, url):
    sim_typing(uid, 1)
    m = Message(uid)
    m.send_message(attachment_type=m_type, attachment_url=url)


@shared_task
def template_message(uid, payload):
    sim_typing(uid, 1)
    m = Message(uid)
    m.send_message(attachment_type='template', attachment_payload=payload)
