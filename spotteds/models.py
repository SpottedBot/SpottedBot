from django.db import models
from django.contrib.auth.models import User
from .facebook_page_tools import page_graph
from django.conf import settings
from moderation.models import Moderator
from .wot_wrapper import is_safe
from .notifications import author_notification, target_notification
from project.loghandler import LogHandler
from facebook import GraphAPIError
# Create your models here.

logger = LogHandler(__name__).logger

# Initial spotted count
initial_count = int(settings.INITIAL_COUNT)


class Spotted(models.Model):
    """Spotted

    fields and methods
    """

    @staticmethod
    def total_spotteds():
        # Returns the latest spotted id + initial_count for the total number of spotteds ever sent
        return Spotted.objects.latest('id').spotted_count

    author = models.ForeignKey(  # User Obj from author
        User,
        related_name='authored',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    target = models.ForeignKey(  # Targeted user
        User,
        related_name='targeted',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    approver = models.ForeignKey(
        Moderator,
        related_name='approved_spotteds',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    created = models.DateTimeField(auto_now_add=True, null=True)
    message = models.TextField()  # Spotted message
    attachment = models.URLField()    # Spotted attachment
    post_id = models.CharField(max_length=100, null=True)  # unique post_id to use with Graph
    api_id = models.IntegerField(default=0)  # unique API id
    dismissed = models.BooleanField(default=False)  # used to save the state of spotteds dismissed by the target
    public = models.BooleanField(default=False)  # Whether the spotted is public or not
    reported = models.CharField(default='', max_length=1000)  # When someone reports a spotted, this is the report text
    share_with_crush = models.BooleanField(default=True)   # Whether or not to let crush know who is the author

    @property
    def spotted_count(self):
        return self.id + initial_count

    @property
    def is_attachment_safe(self):
        return True

    def remove_spotted(self, db_remove=False):
        """Remove Spotted

        tries to delete the spotted from facebook and from the DB if db_remove is True
        """

        try:
            # Remove from facebook
            page_graph().delete_object(self.post_id)
        except Exception as e:
            logger.exception("Exception raised while trying to delete spotted(%s) from Facebook", self.post_id)
            pass
        if db_remove:
            # delete from db
            self.delete()
            return None
        # recreate pending spotted if db_remove is False
        ps = PendingSpotted(message=self.message, author=self.author, target=self.target, attachment=self.attachment)
        ps.save()
        self.delete()
        return ps

    def __str__(self):
        return "Spotted #" + str(self.id)


class PendingSpotted(models.Model):
    """Pending Spotted

    fields and methods
    """

    author = models.ForeignKey(  # User Obj from author
        User,
        on_delete=models.SET_NULL,
        related_name='pending_authored',
        blank=True,
        null=True
    )
    target = models.ForeignKey(  # Targeted user
        User,
        on_delete=models.SET_NULL,
        related_name='pending_targeted',
        blank=True,
        null=True
    )
    message = models.TextField()  # Spotted message
    attachment = models.URLField(null=True, blank=True)    # Spotted attachment
    public = models.BooleanField(default=False)  # Whether the spotted is public or not
    polemic = models.BooleanField(default=False)
    api_id = models.IntegerField(default=0)  # unique API id
    share_with_crush = models.BooleanField(default=True)   # Whether or not to let crush know who is the author

    suggestion = models.CharField(default='', max_length=100)

    attachment_safe = models.BooleanField(default=False)

    @property
    def has_attachment(self):
        return self.attachment is not None and self.attachment != ''

    @property
    def is_attachment_safe(self):
        # If there is an attachment and it is not safe
        if not self.attachment_safe and self.has_attachment:
            # Check if really not safe
            res = is_safe(self.attachment)
            # Update spotted
            self.attachment_safe = res
            self.save()
            # Return its value
            return res

        # Else, is safe
        return True

    def post_spotted(self, mod=None):

        # Only post with attachment if safe
        attachment = self.attachment
        if not self.is_attachment_safe or not self.has_attachment:
            attachment = ''

        # Create new Spotted object from self
        s = Spotted(message=self.message, author=self.author, approver=mod, target=self.target, attachment=attachment, public=self.public, api_id=self.api_id, share_with_crush=self.share_with_crush)
        s.save()
        new_id = s.id + initial_count

        # format message
        f_message = "#" + str(new_id) + "\n\n" + self.message

        # post to facebook
        try:
            # Only if not in debug mode
            if not settings.TEST_MODE:
                resp = page_graph().put_wall_post(f_message, {'link': attachment})
            else:
                resp = {'id': 1}

        # Try to catch invalid url exception
        except GraphAPIError as e:
            # If it was the case, resubmit without link
            if e.message == "The url you supplied is invalid":
                resp = page_graph().put_wall_post(f_message)
            # Else, raise the exception and log it
            else:
                logger.exception("Exception raised while trying to post spotted(%s) to Facebook", self.id)
                raise e
        except Exception as e:
            logger.exception("Exception raised while trying to post spotted(%s) to Facebook", self.id)
            raise e

        # save response post id
        s.post_id = resp['id']
        s.save()
        self.delete()

        # send notifications
        if s.author and not settings.TEST_MODE:
            author_notification(s)
        if s.target and not settings.TEST_MODE:
            target_notification(s)
        return s

    def __str__(self):
        return "PendingSpotted #" + str(self.id)
