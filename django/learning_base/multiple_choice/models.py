"""
module containing all models for multiple choice questions
"""

from django.db import models
from learning_base.models import Question


class MultipleChoiceQuestion(Question):
    """
    A simple multiple choice question
    :Leonhard Wiedmann:
    """
    __name__ = "multiple_choice"

    question_image = models.TextField(
        verbose_name="The Image for the question",
        blank=True,
    )

    feedback_image = models.TextField(
        verbose_name="The Image for the question",
        blank=True,
    )

    def num_correct_answers(self):
        """
        :author: Claas Voelcker
        :return: the number of correct answers
        """
        return len(MultipleChoiceAnswer.objects.filter(
            question=self, is_correct=True))

    def not_solvable(self):
        """
        Checks whether the question is actually solvable
        :author: Claas Voelcker
        :return: True if the number of answers is 0
        """
        return self.num_correct_answers() == 0

    def evaluate(self, data):
        """
        data: Map of answers
        :return: True if and only if the array of provided answers are exactly
        the correct answers
        :author: Tobias Huber
        """

        # get all correct answers, map them to their id and make a
        # (mathematical) set out of it"
        answers = set([x.id for x in
                       self.multiplechoiceanswer_set.filter(is_correct=True)])
        return answers == set(data)

    def __str__(self):
        return self.title

    def answer_set(self):
        """
        shorthand for the answer set
        :author: Leonhard Wiedmann
        :return: the QuerySet of all answers
        """
        return self.multiplechoiceanswer_set.all()

    @staticmethod
    def get_serializer():
        """
        reverse for the serializer
        :author: Claas Voelcker
        :return: the fitting serializer
        """
        from . import serializer
        return serializer.MultipleChoiceQuestionSerializer

    def get_points(self):
        """
        returns the points value of the question
        :return: 2 if the course is hard, else 1
        """
        return 2 if self.module.course.category == 2 else 1

    @staticmethod
    def get_edit_serializer():
        """
        reverse for the serializer
        :author: Claas Voelcker
        :return: the fitting serializer
        """
        from . import serializer
        return serializer.MultipleChoiceQuestionEditSerializer


class MultipleChoiceAnswer(models.Model):
    """
    A possible answer to a multiple choice question
    :author: Claas Voelcker
    """
    question = models.ForeignKey(
        MultipleChoiceQuestion,
        on_delete=models.CASCADE
    )

    text = models.TextField(
        verbose_name="Answer text",
        help_text="The answers text"
    )

    is_correct = models.BooleanField(
        verbose_name='is the answer correct?',
        default=False
    )

    img = models.TextField(
        verbose_name="The Image for the answer",
        blank=True
    )

    def __str__(self):
        return self.text

    @staticmethod
    def get_serializer():
        """
        reverse for the serializer
        :author: Claas Voelcker
        :return: the fitting serializer
        """
        from learning_base.multiple_choice import serializer
        return serializer.MultipleChoiceAnswerSerializer

    @staticmethod
    def get_edit_serializer():
        """
        reverse for the serializer
        :author: Claas Voelcker
        :return: the fitting serializer
        """
        from learning_base.multiple_choice import serializer
        return serializer.MultipleChoiceAnswerEditSerializer
