from django.db import models

# Create your models here.

QUESTION_NAME_LENGTH = 144

class LectionType:
    """
    The type of a lection, meaning the field in which the lection belongs, e.g.
    biochemistry, cloning, technical details.
    """
    name = models.CharField(help_text="Der Name des Gebietes", )

class Lection:
    """
    One lection is a group of questions which build on each other and should be solved
    together. These questions should have similar topics, difficulty and should form
    a compete unit for learning.
    """
    name = models.CharField(help_text="Ein kurzer, ausdrucksstarker Name für die Lektion", )
    lection_type = models.ForeignKey(LectionType, related_name='name', null=False,
                                            blank=False,on_delete=models.CASCADE)

class Question:
    """
    A question is the smallest unit of the learning process. A question has a task that
    can be solved by a user, a correct solution to evaluate the answer and a way to
    provide feedback to the user.
    """
    name = models.CharField(help_text="Ein kurzer, ausdrucksstarker Name für die Frage", )

    __str__(self):
        return "This"
