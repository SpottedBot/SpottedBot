from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from .facebook_methods import get_graph

# Create your models here.


class FacebookUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    access_token = models.TextField()
    social_id = models.TextField(unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires = models.IntegerField()

    first_name = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    link = models.URLField()

    @property
    def is_expired(self):
        return timezone.now() > self.updated_at + datetime.timedelta(seconds=self.expires)

    @property
    def picture(self):
        return get_graph().get_object(str(self.social_id) + "/picture?width=500&height=500")['url']

    @staticmethod
    def create_or_update(social_id, access_token, expires, first_name, name, link):

        print(social_id, access_token, expires, first_name, name, link)

        if FacebookUser.objects.filter(social_id=social_id):
            obj = FacebookUser.objects.get(social_id=social_id)
            obj.access_token = access_token
            obj.expires = expires
            obj.first_name = first_name
            obj.name = name
            obj.link = link
            print('USER UPDATED')
        else:
            user = User.objects.create_user(username=name)
            user.save()
            obj = FacebookUser(
                user=user,
                social_id=social_id,
                access_token=access_token,
                expires=expires,
                first_name=first_name,
                name=name,
                link=link
            )
            print('USER CREATED')
        obj.save()
        return obj
