from django.db import models
from django.contrib.auth.models import User
# from social.apps.django_app.default.models import UserSocialAuth

'''
The model relationship is as follows:

<-- == ForeignKey

Spotted --> User <-- UserSocialAuth

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
