from django.db import models
from learning_base.question.models import Question

class MultipleChoiceAnswer(models.Model):
    """
    A possible answer to a multiple choice question
    """


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


class MultipleChoiceQuestion(Question):
    """
    A simple multiple choice question
    """

    answers = models.ManyToManyField(MultipleChoiceAnswer)

    def __str__(self):
        return self.question_body

    def numCorrectAnswers(self):
        return self.answers.filter(is_correct=True).count()

    def notSolvable(self):
        return self.numCorrectAnswers() == 0

    def evaluate(self, data):
        answers = self.answers.filter(is_correct=True)

        # if the the array length of the answers is not equeal to the correct answers it cant be correct
        if len(data) != len(answers):
            return False

        # check if all correct answers exist in the array of usre answers
        for ans in answers:
            if not (ans.id in data):
                return False
        return True

    def save(self, q):
        question_body=q['question']

        super(Question, self).save()
        
        for a in q['answers']:
            ans = MultipleChoiceAnswer(text=a['text'], is_correct = a['correct'])
            ans.save()
            self.answers.add(ans)
