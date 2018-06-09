from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from api.api_interface import api_submit_message_log


class Chat(models.Model):
    """Chat model.

    Represents an ongoing dialog between the bot and a person
    """

    # Facebook user id
    uid = models.CharField(max_length=200, unique=True)
    # Whether or not the bot has control of the chat
    standby = models.BooleanField(default=False)
    # Timeout dt for the control handover
    standby_dt = models.DateTimeField(default=timezone.now)

    # Whether or not to send the conversation log to the API
    log_conversation = models.BooleanField(default=False)
    # Anonymized conversation id
    conversation_id = models.CharField(null=True, max_length=32)

    # Last raw message sent
    last_raw_message = models.TextField(null=True)
    # Whether or not to accept input messages that are not postovers
    accept_raw_input = models.BooleanField(default=False)
    # Timeout dt for the raw input acceptance
    accept_raw_input_dt = models.DateTimeField(default=timezone.now)

    @staticmethod
    def set_get_or_create(uid):
        # Get or create a new chat
        chat, created = Chat.objects.get_or_create(uid=uid)
        if created:
            chat = chat.update_conversation_id()
        return chat

    # Chat standby and expiration

    @staticmethod
    def check_expired(uid):
        # True if it has, False otherwise
        chat = Chat.set_get_or_create(uid=uid)
        return (timezone.now() - chat.standby_dt).days > 0

    @property
    def standby_expired(self):
        # Checks if the standby period has expired
        exp = Chat.check_expired(self.uid)
        if exp:
            # If it has, take thread control from page
            from .handlers.handover import take_thread_control
            take_thread_control(self.uid)
        return exp

    @staticmethod
    def is_standby(uid):
        # public method that returns true if the chat is in standby
        chat = Chat.set_get_or_create(uid=uid)
        return chat.standby and not chat.standby_expired

    @staticmethod
    def set_standby(uid):
        # Sets the chat as standby
        chat = Chat.set_get_or_create(uid=uid)
        chat.standby = True
        chat.standby_dt = timezone.now()
        chat.save()

    @staticmethod
    def set_active(uid):
        # Sets the chat as active
        chat = Chat.set_get_or_create(uid=uid)
        chat.standby = False
        chat.log_conversation = False
        chat.save()
        chat.update_conversation_id()

    # Chat listener and logger

    @staticmethod
    def set_listened_standby(uid):
        # Sets the chat as standby and also starts sending
        # messages to the API
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
        # Append message to the API log
        chat = Chat.set_get_or_create(uid=uid)
        if chat.log_conversation:
            sender = 'page' if from_page else 'user'
            conversation_id = chat.conversation_id
            api_submit_message_log(conversation_id, message, sender)

    # Raw input allower

    @staticmethod
    def set_last_raw_message(uid, message):
        # Set last raw message as input
        chat = Chat.set_get_or_create(uid)
        chat.last_raw_message = message
        chat.save()

    @staticmethod
    def set_accept_raw(uid):
        # Enables raw messages
        chat = Chat.set_get_or_create(uid)
        chat.accept_raw_input = True
        chat.accept_raw_input_dt = timezone.now()
        chat.save()

    @staticmethod
    def set_raw_solution_found(uid):
        # Disables raw message when solution to query
        # is found
        chat = Chat.set_get_or_create(uid)
        chat.accept_raw_input = False
        chat.save()

    @staticmethod
    def set_raw_solution_not_found(uid):
        # Disables raw messages when solution
        # to query is not found, setting as listened
        # standby
        Chat.set_raw_solution_found(uid)
        Chat.set_listened_standby(uid)

    @staticmethod
    def is_accepting_raw(uid):
        # Checks if the chat is accepting raw messages
        chat = Chat.set_get_or_create(uid)
        if chat.accept_raw_input:
            # If raw input has expired, set is as found
            if (timezone.now() - chat.accept_raw_input_dt).seconds // 60 > 10:
                Chat.set_raw_solution_found(uid)
        return Chat.set_get_or_create(uid).accept_raw_input

        return Chat.set_get_or_create(uid).accept_raw_input

    # Conversation id generator

    def update_conversation_id(self):
        # Updates the anonymized chat id
        self.conversation_id = get_random_string(32)
        self.save()
        return self
