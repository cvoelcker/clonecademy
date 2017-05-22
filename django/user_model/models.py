from django.db import models
from django.contrib.auth.models import User
from learning_base import models as lb_models
from django.core.exceptions import ValidationError

class LearningGroup(models.Model):
    """
    A user group
    """
    name = models.CharField(help_text="The name of the user group", max_length=144)

    def __str__(self):
        return self.name

class Profile(models.Model):
    """
    The profile of a user, storing information about its completed courses etc.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(LearningGroup, null=True, on_delete=models.SET_NULL)
    date_registered = models.DateField()

    def __str__(self):
        return self.name


class Completion(models.Model):
    """
    A field holding reference for a user that completed a course. This makes it possible
    to track, when a user completed the course
    """
    person = models.ForeignKey(Profile, on_delete=models.CASCADE)
    course = models.ForeignKey(lb_models.Course, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.name


class Progress(models.Model):
    """
    A field tracking a users progress in different modules.
    """
    person = models.ForeignKey(Profile, on_delete=models.CASCADE)
    course = models.ForeignKey(lb_models.Course, on_delete=models.CASCADE)
    date = models.DateField()
    #question_id = models.ForeignKey(lb_models.Question)

    def clean():
        if(question_id.getCourse != course):
            raise ValidationError(_('Course has no matching question'))

    def __str__(self):
        return self.name
