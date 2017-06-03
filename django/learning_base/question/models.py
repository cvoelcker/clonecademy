from django.db import models
from polymorphic.models import PolymorphicModel

class Question(PolymorphicModel):
    """
    A question is the smallest unit of the learning process. A question has a task that
    can be solved by a user, a correct solution to evaluate the answer and a way to
    provide feedback to the user.
    """
    question_title = models.TextField(
        verbose_name='Question title',
        help_text="A short and concise name for the "
    )
    question_body = models.TextField(
        verbose_name='Question text',
        help_text="This field can contain markdown syntax"
    )

    feedback = models.TextField(
        verbose_name="feedback",
        help_text="The feedback for the user after sucessfull answer",
        null=True
    )

    feedback_is_set = models.BooleanField(
        verbose_name="feedback is set",
        help_text="If this is true the user will get back the custom feedback"
    )

    def __str__(self):
        return self.question_title
