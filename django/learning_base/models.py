from django.db import models

class CourseCategory(models.Model):
    """
    The type of a Course, meaning the field in which the Course belongs, e.g.
    biochemistry, cloning, technical details.
    """
    name = models.CharField(help_text="Name of the category (e.g. biochemistry)", max_length=144)


class Course(models.Model):
    """
    One Course is a group of questions which build on each other and should be solved
    together. These questions should have similar topics, difficulty and should form
    a compete unit for learning.
    """
    QUESTION_NAME_LENGTH = 144

    EASY = 'EA'
    MODERATE = 'MO'
    DIFFICULT = 'DI'
    EXPERT = 'MA'
    DIFFICULTY = (
        (EASY, 'Easy (high school students)'),
        (MODERATE, 'Moderate (college entry)'),
        (DIFFICULT, 'Difficult (college students'),
        (EXPERT, 'Expert (college graduates)'),
    )
    name = models.CharField(help_text="A short concise name for the course", unique=True, max_length=144)
    #Course_type = models.ManyToManyField(CourseCategory)
    Course_difficulty = models.CharField(
        max_length=2,
        choices=DIFFICULTY,
        default=MODERATE
    )


class Question(models.Model):
    """
    A question is the smallest unit of the learning process. A question has a task that
    can be solved by a user, a correct solution to evaluate the answer and a way to
    provide feedback to the user.
    """
    name = models.CharField(help_text="A short concise name for the question", max_length=144)
    #TODO: Find better representation
    ranking = models.IntegerField(help_text="Determines the place of the question")
    question_body = models.TextField(help_text="This field can contain markdown syntax")
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    class Meta():
        unique_together = (("course", "ranking"),)

class MultipleChoiceQuestion(Question):
    def numCorrectAnswers(self):
        return self.multiplechoiceanswer_set.filter(is_correct=True).count()
    def notSolvable(self):
        return self.numCorrectAnswers() == 0

class MultipleCoiceAnswer(models.Model):
    """
    A possible answer to a multiple choice question
    """
    text = models.TextField(help_text="The answers text")
    is_correct = models.BooleanField(default=False)

    question = models.ForeignKey('MultipleChoiceQuestion', on_delete=models.CASCADE)
