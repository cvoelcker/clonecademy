from django.db import models
from learning_base.models import Question


class InformationText(Question):
    """
    A 'question' that only displays an informative text
    to the user. It requires no input and is only used to
    convey additional learning material to the reader.
    @author: Claas Voelcker
    """

    __name__ = "info_text"

    image = models.TextField(
        blank=True,
    )

    text_field = models.TextField()

    def not_solvable(self):
        return False

    def evaluate(self, data):
        return True

    def num_correct_answers(self):
        return 0

    def get_serializer(self):
        from learning_base.info import serializer
        return serializer.InformationTextSerializer

    def get_edit_serializer(self):
        from learning_base.info import serializer
        return serializer.InformationTextSerializer

    def __str__(self):
        return "Learning text {}".format(self.id)
