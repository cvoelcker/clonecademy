from django.db import models
from learning_base.models import Question


class MultipleChoiceQuestion(Question):
    """
    A simple multiple choice question
    """
    def num_correct_answers(self):
        return len(MultipleChoiceAnswer.objects.filter(is_correct=True))

    def not_solvable(self):
        return self.num_correct_answers() == 0

    def evaluate(self, data):
        answers = map(lambda x: x.id, MultipleChoiceAnswer.objects.filter(question=self, is_correct=True))

        # if the the array length of the answers is not equal to the correct answers it cant be correct
        if len(data) != len(answers):
            return False

        # check if all correct answers exist in the array of user answers
        for ans in answers:
            if not (ans in data):
                return False
        return True

    def __str__(self):
        return self.body

    def answer_set(self):
        return self.multiplechoiceanswer_set.all()


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
        from learning_base.multiple_choice import serializer
        return serializer.MultipleChoiceAnswerSerializer
