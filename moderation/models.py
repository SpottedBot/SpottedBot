from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
now = timezone.localtime(timezone.now())


@property
def is_moderator(self):
    """Is Moderator.

    User property to check if the user is a moderator
    """
    try:
        self.moderator.id
        return True
    except:
        return False


# Monkeypatch the property to user
User.add_to_class('is_moderator', is_moderator)


class Moderator(models.Model):
    """Moderator.

    Fields and methods
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True
    )

    def log_action(self):
        for work in self.workhours.all():
            # For every workhour, register action
            work.action_took()

    def __str__(self):
        return self.user.facebookuser.name


WEEK_DAYS = (
    (0, 'Segunda'),
    (1, 'Terça'),
    (2, 'Quarta'),
    (3, 'Quinta'),
    (4, 'Sexta'),
    (5, 'Sábado'),
    (6, 'Domingo')
)
WEEK_DAY_NAMES = {
    '0': 'Segunda',
    '1': 'Terça',
    '2': 'Quarta',
    '3': 'Quinta',
    '4': 'Sexta',
    '5': 'Sábado',
    '6': 'Domingo'
}
HOURS = [(i, str(i) + ":00") for i in range(24)]
DURATION = [(i, str(i) + ":00") for i in range(1, 25)]


class WorkHour(models.Model):
    """Work Hour.

    Represents each individual moderator's work shifts
    Used for internal staff control
    """

    moderator = models.ForeignKey(
        Moderator,
        on_delete=models.CASCADE,
        related_name='workhours',
    )

    # Work's day(of the week) hour and duration
    day = models.IntegerField(choices=WEEK_DAYS)
    hour = models.IntegerField(choices=HOURS)
    duration = models.IntegerField(choices=DURATION)

    # Last time worked(at the right time)
    last_worked = models.DateTimeField(null=True)

    # Returns the last work start moment as datetime obj
    @property
    def last_work(self):
        now2 = now.replace(hour=self.hour, minute=0)
        return now2 - datetime.timedelta((now2.weekday() - self.day) % 7)

    @property
    def weekday(self):
        return WEEK_DAY_NAMES[str(self.day)]

    # True if worked this week. False otherwise
    @property
    def has_worked(self):
        return self.last_work <= self.last_worked <= self.last_work + datetime.timedelta(hours=self.duration)

    # Simply call this whenever a moderator makes a change(or login, dunno)
    def action_took(self):

        if self.last_work <= now <= self.last_work + datetime.timedelta(hours=self.duration):
            self.last_worked = now
            self.save()
