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
        help_text="A short and concise nae for the "
    )
    question_body = models.TextField(
        verbose_name='Question text',
        help_text="This field can contain markdown syntax"
    )

    def __str__(self):
        return self.question_title
