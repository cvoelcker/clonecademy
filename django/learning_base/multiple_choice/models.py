from django.db import models
from learning_base.models import Question


class MultipleChoiceQuestion(Question):
    """
    A simple multiple choice question
    """

    def __str__(self):
        return self.question_body

    def numCorrectAnswers(self):
        return self.answers.filter(is_correct=True).count()

    def notSolvable(self):
        return self.numCorrectAnswers() == 0

    def evaluate(self, data):
        answers = map(lambda x: x.id, self.answers.filter(is_correct=True))

        # if the the array length of the answers is not equal to the correct answers it cant be correct
        if len(data) != len(answers):
            return False

        # check if all correct answers exist in the array of user answers
        for ans in answers:
            if not (ans in data):
                return False
        return True

    def delete(self):
        for ans in self.answers:
            ans.delete()
        super(MultipleChoiceQuestion, self).delete()

    def save(self, q):
        if 'question' not in q or 'answers' not in q:
            return False
        question_body=q['question']

        super(Question, self).save()

        for a in q['answers']:
            if 'correct' not in a or 'text' not in a:
                return False
            ans = MultipleChoiceAnswer(text=a['text'], is_correct = a['correct'])
            ans.save()
            self.answers.add(ans)
        return True


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
