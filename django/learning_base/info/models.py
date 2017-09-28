"""
Models for information type questions
"""
from django.db import models
from learning_base.models import Question


class InformationText(Question):
    """
    A 'question' that only displays an informative text
    to the user. It requires no input and is only used to
    convey additional learning material to the reader.
    :author: Claas Voelcker
    """

    __name__ = "info_text"

    image = models.TextField(
        blank=True,
    )

    text_field = models.TextField()

    @staticmethod
    def not_solvable():
        """
        always solvable
        :author: Claas Voelcker
        :return: False
        """
        return False

    @staticmethod
    def evaluate(data):
        """
        always correctly solved
        :author: Claas Voelcker
        :return: True
        """
        return True

    @staticmethod
    def num_correct_answers():
        """
        has no answers
        :author: Claas Voelcker
        """
        return 0

    @staticmethod
    def get_serializer():
        """
        returns the correct serializer
        :author: Claas Voelcker
        :return: serializer for the question
        """
        from . import serializer
        return serializer.InformationTextSerializer

    @staticmethod
    def get_edit_serializer():
        """
        returns the serializer for editing
        :author: Claas Voelcker
        :return: serializer for the question
        """
        return InformationText.get_serializer()

    @staticmethod
    def get_points():
        """
        has no points for a correct answer
        :author: Claas Voelcker
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
        always solvable
        :author: Claas Voelcker
        :return: False
        """
        return False

    @staticmethod
    def evaluate(data):
        """
        always correctly solved
        :author: Claas Voelcker
        :return: True
        """

        return True

    @staticmethod
    def num_correct_answers():
        """
        has no answers
        :author: Claas Voelcker
        """
        return 0

    @staticmethod
    def get_serializer():
        """
        returns the correct serializer
        :author: Claas Voelcker
        :return: serializer for the question
        """
        from . import serializer
        return serializer.InformationYoutubeSerializer

    @staticmethod
    def get_edit_serializer():
        """
        returns the serializer for editing
        :return: serializer for the question
        """
        from . import serializer
        return serializer.InformationYoutubeSerializer

    @staticmethod
    def get_points():
        """
        has no points for a correct answer
        :author: Claas Voelcker
        """
        return 0

    def __str__(self):
        """
        :return: string representation from the id
        """
        return "Learning text {}".format(self.id)
