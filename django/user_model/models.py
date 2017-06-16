from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime
from clonecadamy.settings import FRONT_END_HOSTNAME, PROFILE_PATH
from django.apps import apps
# from learning_base import models as lb_models


# TODO: Refactor everything into one fucking app

class LearningGroup(models.Model):
    """
    A user group (currently not used)
    """
    name = models.CharField(help_text="The name of the user group", max_length=144)

    def __str__(self):
        return self.name

class ProfileManager(models.Manager):
    def create_both(self, username, email, password="", group=None, first_name='', last_name='', age=None):
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        if LearningGroup.objects.filter(name=group):
            group = LearningGroup.objects.filter(name=group)
        else:
            group=None
        profile = Profile(
            user=user,
            group=group,
            first_name=first_name,
            last_name=last_name,
            age=age
        )
        profile.save()
        return


class Profile(models.Model):
    """
    The profile of a user, storing information about its completed courses etc.
    """
    objects = ProfileManager()

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    group = models.OneToOneField(
        LearningGroup,
        blank=True,
        null=True
    )

    is_mod = models.BooleanField(
        default=False
    )

    is_trusted_mod = models.BooleanField(
        default=False
    )

    requested_mod = models.DateField(
        default=None,
        null=True,
        blank=True
    )

    #Optional info from the user
    first_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    age = models.IntegerField(
        blank=True,
        null=True
    )

    def get_link_to_profile(self):
        '''
        Returns the link to the users profile page
        '''
        #TODO: Implement correct user profile access string
        return "clonecademy.com/this/users/profile"

    def __str__(self):
        return self.user.__str__()


class Try(models.Model):
    '''
    A try represents a submission of an answer. Each time an answer is submitted, a Try
    object is created in the database, detailing answer, wether it was answered
    correctly and the time of the submission.
    '''
    person = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
    )

    question = models.ForeignKey(
        apps.get_model('learning_base', 'Question', require_ready=False),
        null=True,
        on_delete=models.SET_NULL,
    )

    answer = models.TextField(
        verbose_name="The given answer",
        help_text="The answers as pure string",
        null=True
    )

    date = models.DateTimeField(
        default=datetime.now,
        null=True
    )

    solved = models.BooleanField(
        default=False
    )

    def __unicode__(self):
        return "Solution_{}_{}_{}".format(self.question, self.solved, self.date)

