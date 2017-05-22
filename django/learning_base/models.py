from django.db import models
from polymorphic.models import PolymorphicModel
from django.contrib.contenttypes.models import ContentType

class CourseCategory(models.Model):
    """
    The type of a course, meaning the field in which the course belongs, e.g.
    biochemistry, cloning, technical details.
    """
    name = models.CharField(
        help_text="Name of the category (e.g. biochemistry)",
        max_length=144
    )

    def getCourses(self):
        return self.course_set

    def __str__(self):
        return self.name

class Module(PolymorphicModel):
    """
    A Course is made out of many modules and a module is the Base class for everything else.
    In a module can be questions  or chapters.
    """

    class Meta():
        ordering = ('order',)

    name = models.CharField(
        help_text="A short concise name for the module",
        verbose_name='Question name',
        max_length=144
    )
    order = models.IntegerField(
        verbose_name='Question Order',
        help_text="Determines the place of the module",
        default=0
    )


    def __str__(self):
        return self.name

class Course(models.Model):
    """
    One course is a group of questions which build on each other and should be solved
    together. These questions should have similar topics, difficulty and should form
    a compete unit for learning.
    """
    QUESTION_NAME_LENGTH = 144

    EASY = 'EA'
    MODERATE = 'MO'
    DIFFICULT = 'DI'
    EXPERT = 'EX'
    DIFFICULTY = (
        (EASY, 'Easy (high school students)'),
        (MODERATE, 'Moderate (college entry)'),
        (DIFFICULT, 'Difficult (college students'),
        (EXPERT, 'Expert (college graduates)')
    )

    name = models.CharField(
        verbose_name='Course name',
        help_text="A short concise name for the course",
        unique=True,
        max_length=144
    )
    #Course_type = models.ManyToManyField(CourseCategory)

    # QUESTION: Other representation better? How to guarantee constraints
    course_difficulty = models.CharField(
        verbose_name='Course difficulty',
        max_length=2,
        choices=DIFFICULTY,
        default=MODERATE
    )
    is_visible = models.BooleanField(
        verbose_name='Is the course visible',
        default=False
    )

    module = models.ManyToManyField(Module)

    category = models.ManyToManyField(CourseCategory)

    def visible(self):
        return self.is_visible

    def getQuestions(self):
        return self.question_set

    def __str__(self):
        return self.name

class Question(Module):
    """
    A question is the smallest unit of the learning process. A question has a task that
    can be solved by a user, a correct solution to evaluate the answer and a way to
    provide feedback to the user.
    """
    question_body = models.TextField(
        verbose_name='Question text',
        help_text="This field can contain markdown syntax"
    )

    def __str__(self):
        return self.name


class MultipleChoiceAnswer(models.Model):
    """
    A possible answer to a multiple choice question
    """
    class Meta:
        ordering = ('?', )

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

    def getAnswers(self):
        return self.answers

    def numCorrectAnswers(self):
        return self.getAnswers().filter(is_correct=True).count()

    def notSolvable(self):
        return self.numCorrectAnswers() == 0

    def __str__(self):
        return self.name
