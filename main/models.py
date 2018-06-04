from django.db import models
from django.utils.crypto import get_random_string

# Create your models here.


class NagMessage(models.Model):
    nag_id = models.CharField(max_length=32)
    message = models.TextField(null=True)
    enable = models.BooleanField(default=False)

    @staticmethod
    def get():
        if NagMessage.objects.count() == 0:
            nag = NagMessage(
                nag_id=get_random_string(32),
                message=''
            )
            nag.save()
        else:
            nag = NagMessage.objects.first()
        return nag

    @staticmethod
    def update(message, enable):
        nag = NagMessage.get()
        nag.nag_id = get_random_string(32)
        nag.message = message
        nag.enable = enable if message else False
        nag.save()
