from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from api.api_interface import api_submit_message_log


class Chat(models.Model):
    uid = models.CharField(max_length=200, unique=True)
    standby = models.BooleanField(default=False)
    standby_dt = models.DateTimeField(default=timezone.now)

    log_conversation = models.BooleanField(default=False)
    conversation_id = models.CharField(null=True, max_length=32)

    last_raw_message = models.TextField(null=True)
    accept_raw_input = models.BooleanField(default=False)
    accept_raw_input_dt = models.DateTimeField(default=timezone.now)

    # Get or create a new chat
    @staticmethod
    def set_get_or_create(uid):
        chat, created = Chat.objects.get_or_create(uid=uid)
        if created:
            chat = chat.update_conversation_id()
        return chat

    # Chat standby and expiration

    @staticmethod
    def check_expired(uid):
        chat = Chat.set_get_or_create(uid=uid)
        return (timezone.now() - chat.standby_dt).days > 0

    @property
    def standby_expired(self):
        exp = Chat.check_expired(self.uid)
        if exp:
            from .handlers.handover import take_thread_control
            take_thread_control(self.uid)
        return exp

    @staticmethod
    def is_standby(uid):
        chat = Chat.set_get_or_create(uid=uid)
        return chat.standby and not chat.standby_expired

    @staticmethod
    def set_standby(uid):
        chat = Chat.set_get_or_create(uid=uid)
        chat.standby = True
        chat.standby_dt = timezone.now()
        chat.save()

    @staticmethod
    def set_active(uid):
        chat = Chat.set_get_or_create(uid=uid)
        chat.standby = False
        chat.log_conversation = False
        chat.save()
        chat.update_conversation_id()

    # Chat listener and logger

    @staticmethod
    def set_listened_standby(uid):
        Chat.set_standby(uid)
        chat = Chat.set_get_or_create(uid)
        chat.log_conversation = True
        chat.save()
        # Send the last message sent by the user,
        # so that the context is maintained
        last_message = chat.last_raw_message or '500 Mensagem Vazia'
        Chat.append_log(uid, last_message, False)

    @staticmethod
    def append_log(uid, message, from_page):
        chat = Chat.set_get_or_create(uid=uid)
        if chat.log_conversation:
            sender = 'page' if from_page else 'user'
            conversation_id = chat.conversation_id
            api_submit_message_log(conversation_id, message, sender)

    # Raw input allower

    @staticmethod
    def set_last_raw_message(uid, message):
        chat = Chat.set_get_or_create(uid)
        chat.last_raw_message = message
        chat.save()

    @staticmethod
    def set_accept_raw(uid):
        chat = Chat.set_get_or_create(uid)
        chat.accept_raw_input = True
        chat.accept_raw_input_dt = timezone.now()
        chat.save()

    @staticmethod
    def set_raw_solution_found(uid):
        chat = Chat.set_get_or_create(uid)
        chat.accept_raw_input = False
        chat.save()

    @staticmethod
    def set_raw_solution_not_found(uid):
        Chat.set_raw_solution_found(uid)
        Chat.set_listened_standby(uid)

    @staticmethod
    def is_accepting_raw(uid):
        chat = Chat.set_get_or_create(uid)
        if chat.accept_raw_input:
            # If raw input has expired, set is as found
            if (timezone.now() - chat.accept_raw_input_dt).seconds // 60 > 10:
                Chat.set_raw_solution_found(uid)
        return Chat.set_get_or_create(uid).accept_raw_input

        return Chat.set_get_or_create(uid).accept_raw_input

    # Conversation id generator

    def update_conversation_id(self):
        self.conversation_id = get_random_string(32)
        self.save()
        return self
