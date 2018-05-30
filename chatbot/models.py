from django.db import models
from django.utils import timezone


class Chat(models.Model):
    uid = models.CharField(max_length=200, unique=True)
    standby = models.BooleanField(default=False)
    standby_dt = models.DateTimeField(default=timezone.now)

    @property
    def standby_expired(self):
        exp = (timezone.now() - self.standby_dt).days > 0
        if exp:
            from .handlers.handover import take_thread_control
            take_thread_control(self.uid)
        return exp

    @staticmethod
    def check_expired(uid):
        chat, _ = Chat.objects.get_or_create(uid=uid)
        return (timezone.now() - chat.standby_dt).days > 0

    @staticmethod
    def is_standby(uid):
        chat, _ = Chat.objects.get_or_create(uid=uid)
        return chat.standby and not chat.standby_expired

    @staticmethod
    def set_standby(uid):
        chat, _ = Chat.objects.get_or_create(uid=uid)
        chat.standby = True
        chat.standby_dt = timezone.now()
        chat.save()

    @staticmethod
    def set_active(uid):
        chat, _ = Chat.objects.get_or_create(uid=uid)
        chat.standby = False
        chat.save()
