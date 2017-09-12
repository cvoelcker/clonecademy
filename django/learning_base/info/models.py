"""
x
"""
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

    @staticmethod
    def not_solvable():
        """
        x
        """
        return False

    @staticmethod
    def evaluate(data):
        """
        x
        """
        return True

    @staticmethod
    def num_correct_answers():
        """
        x
        """
        return 0

    @staticmethod
    def get_serializer():
        """
        x
        """
        from . import serializer
        return serializer.InformationTextSerializer

    @staticmethod
    def get_edit_serializer():
        """
        x
        """
        from . import serializer
        return serializer.InformationTextSerializer

    @staticmethod
    def get_points():
        """
        x
        """
        return 0

    def __str__(self):
        return "Learning text {}".format(self.id)


class InformationYoutube(Question):
    """
    A 'question' that only displays an informative text
    to the user. It requires no input and is only used to
    convey additional learning material to the reader.
    @author: Claas Voelcker
    """

    __name__ = "info_text_youtube"

    url = models.TextField(
        blank=True,
    )

    text_field = models.TextField()

    @staticmethod
    def not_solvable():
        """
        x
        """
        return False

    @staticmethod
    def evaluate(data):
        """
        x
        """
        return True

    @staticmethod
    def num_correct_answers():
        """
        x
        """
        return 0

    @staticmethod
    def get_serializer():
        """
        x
        """
        from . import serializer
        return serializer.InformationYoutubeSerializer

    @staticmethod
    def get_edit_serializer():
        """
        x
        """
        from . import serializer
        return serializer.InformationYoutubeSerializer

    @staticmethod
    def get_points():
        """
        x
        """
        return 0

    def __str__(self):
        """
        x
        """
        return "Learning text {}".format(self.id)
