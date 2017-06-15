from django.db import models
from django.contrib.auth.models import User
from learning_base import models as lb_models
from learning_base.question import models as question_model
from django.core.exceptions import ValidationError
from datetime import datetime
from clonecadamy.settings import FRONT_END_HOSTNAME, PROFILE_PATH


class LearningGroup(models.Model):
    """
    A user group
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
        #related_name = "profile"
        #could ease access to the corespending profile from a given user
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
        #TODO: Implement correct user prile access strin
        return "clonecademy.com/this/users/profile"

    def __str__(self):
        return self.user.__str__()


class Try(models.Model):
    person = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=False
    )
    question = models.ForeignKey(
        question_model.Question,
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
        return "Question: {} was solved {} on {}".format(self.question, self.solved, self.date)


class CourseCompletion(models.Model):
    """
    A field holding reference for a user that completed a course. This makes it possible
    to track, when a user completed the course
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

    # question_id = models.ForeignKey(lb_models.Question)

    def clean():
        if (question_id.getCourse != course):
            raise ValidationError(_('Course has no matching question'))

    def __str__(self):
        return self.name
