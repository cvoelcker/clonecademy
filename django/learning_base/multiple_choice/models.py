from django.db import models
from learning_base.models import Question


class MultipleChoiceQuestion(Question):
    """
    A simple multiple choice question
    """
    __name__ = "multiple_choice"

    question_image = models.CharField(
        max_length=255,
        verbose_name = "The Image for the question",
        blank = True,
    )

    answer_image = models.CharField(
        max_length=255,
        verbose_name = "The Image for the question",
        blank = True,
    )

    def num_correct_answers(self):
        return len(MultipleChoiceAnswer.objects.filter(is_correct=True))

    def not_solvable(self):
        return self.num_correct_answers() == 0

    def evaluate(self, data):
        """
        data: Map of answers
        returns True if and only if the array of provided answers are exactly
        the correct answers
        @author Tobias Huber
        """

        "get all correct answers, map them to their id and make a (mathematical) set out of it"
        answers = set([x.id for x in self.multiplechoiceanswer_set.filter(is_correct=True)])
        return answers == set(data)

    def __str__(self):
        return self.body

    def answer_set(self):
        return self.multiplechoiceanswer_set.all()

    def get_serializer(self):
        from learning_base.multiple_choice import serializer
        return serializer.MultipleChoiceQuestionSerializer

    def get_edit_serializer(self):
        from learning_base.multiple_choice import serializer
        return serializer.MultipleChoiceQuestionEditSerializer

class MultipleChoiceAnswer(models.Model):
    """
    A possible answer to a multiple choice question
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

    def __str__(self):
        return self.text

    def get_serializer(self):
        from learning_base.MultipleChoiceQuestion import serializer
        return serializer.MultipleChoiceAnswerSerializer

    def get_edit_serializer(self):
        from learning_base.MultipleChoiceQuestion import serializer
        return serializer.MultipleChoiceAnswerEditSerializer
