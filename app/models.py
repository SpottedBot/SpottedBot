from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from social.apps.django_app.default.models import UserSocialAuth
from helpers.facebook_utils import global_id, profile_from_scope

'''
The model relationship is as follows:

<--  == ForeignKey
<--> == OneToOne

Spotted --> User <-- UserSocialAuth
Profile <--> User

From User you can get:
User.first_name
User.last_name
User.username

From UserSocialAuth you can get:
UserSocialAuth.user
UserSocialAuth.uid
UserSocialAuth.provider
UserSocialAuth.extra_data (dict with keys 'id', 'access_token' and 'expires')

Examples:
Retrieve a User from an UID:
$ UserSocialAuth.objects.get(uid=<uid>).user

Retrieve all spotteds from user:
$ Spotted.objects.filter(author=<userObj>)
'''


class Spotted(models.Model):
    author = models.ForeignKey(  # User Obj from author
        User,
        on_delete=models.CASCADE, blank=True, null=True
    )
    target = models.CharField(max_length=100)   # UID from target
    message = models.TextField()  # Spotted message
    attachment = models.URLField()    # Spotted attachment
    spam = models.BooleanField(default=False)   # Spam bool
    post_id = models.CharField(max_length=100)  # unique post_id to use with Graph
    dismissed = models.BooleanField(default=False)  # used to save the state of spotteds dismissed by the target

    def __str__(self):
        return "Spotted #" + str(self.id)


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    global_id = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user.username) + "'s profile"


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        u = Profile(user=instance)
        u.save()


def update_user_profile(sender, instance, created, **kwargs):
    if created:
        u = instance.user
        u.profile.global_id = global_id(profile_from_scope(instance.uid))
        u.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(update_user_profile, sender=UserSocialAuth)
