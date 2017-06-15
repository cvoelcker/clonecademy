from django.db import models
from django.contrib.auth.models import User
from learning_base import models as lb_models
from django.core.exceptions import ValidationError
from datetime import datetime
from clonecadamy.settings import FRONT_END_HOSTNAME, PROFILE_PATH


class LearningGroup(models.Model):
    """
    A user group (currently not used)
    """
    name = models.CharField(help_text="The name of the user group", max_length=144)

    def __str__(self):
        return self.name


class Profile(models.Model):
    """
    The profile of a user, storing information about its completed courses etc.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    group = models.OneToOneField(
        LearningGroup,
        blank=True,
        null=True
    )

    date_registered = models.DateField()

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
        null = True,
        blank = True
    )

    last_name = models.CharField(
        max_length=100,
        null = True,
        blank = True
    )

    age = models.IntegerField(
        null = True,
        blank = True
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
        lb_models.Question,
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


class CourseCompletion(models.Model):
    """
    A field holding reference for a user that completed a course. This makes it possible
    to track, when a user completed the course.
    """
    person = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        lb_models.Course,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    def __str__(self):
        return self.name


#TODO: Implement which questions are solved (maybe via the Try's?)
class Progress(models.Model):
    """
    A field tracking a users progress in different modules.
    """
    person = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        lb_models.Course,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    def __str__(self):
        return self.name
