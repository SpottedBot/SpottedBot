from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from .facebook_methods import get_graph

# Create your models here.


@property
def has_facebook(self):
    return hasattr(self, 'facebookuser')


User.add_to_class('has_facebook', has_facebook)


class FacebookUser(models.Model):
    """Facebook User

    Has some info about the Facebook OAuth user.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    access_token = models.TextField()

    # Scope User ID
    social_id = models.TextField(unique=True)

    # Last time the user was updated
    updated_at = models.DateTimeField(auto_now=True)

    # Expiration time
    expires = models.IntegerField()

    first_name = models.CharField(max_length=50)
    name = models.CharField(max_length=150)

    # Direct link to user's profile
    link = models.URLField(max_length=2000)

    @property
    def is_expired(self):

        # Returns true if expired. False otherwise
        return timezone.now() > self.updated_at + datetime.timedelta(seconds=self.expires)

    @property
    def thumbnail(self):
        """50x50 thumbnail"""
        return "https://graph.facebook.com/{}/picture?width=50&height=50".format(self.social_id)

    @property
    def hd_thumbnail(self):
        """500x500 thumbnail"""
        return "https://graph.facebook.com/{}/picture?width=500&height=500".format(self.social_id)

    @property
    def picture(self):
        """500x500 thumbnail"""
        return self.hd_thumbnail

    @staticmethod
    def create_or_update(social_id, access_token, expires, first_name, name, link):
        """Create or Update a Facebook User

        Receives a social_id and, if not yet saved, creates a new FacebookUser
        Update it otherwise
        """

        # Tries to find the user
        if FacebookUser.objects.filter(social_id=social_id):

            # if it is found, get it and update it
            obj = FacebookUser.objects.get(social_id=social_id)
            obj.access_token = access_token
            obj.expires = expires
            obj.first_name = first_name
            obj.name = name
            obj.link = link

        else:
            def f_usname(name, n=0):
                """
                appends n to the end of the username, automatically adding 1 if exists
                """
                if not User.objects.filter(username=name + '_' + str(n)).exists():
                    return name + '_' + str(n)
                return f_usname(name, n + 1)

            # If it is not found, create a new user and then a new facebookuser
            user = User.objects.create_user(username=f_usname(name))
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
        obj.save()
        return obj
