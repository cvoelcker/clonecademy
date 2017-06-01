from django.db import models
from learning_base.question.models import Question
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

class Module(models.Model):
    """
    A Course is made out of many modules and a module and in a Module can be n questions
    """

    class Meta():
        ordering = ('name',)

    name = models.CharField(
        help_text="A short concise name for the module",
        verbose_name='Module name',
        max_length=144
    )

    question_order = models.CharField(
        help_text="the ordering of the questions in array format. It must to start with [ and end with ]",
        verbose_name="Question ordering array",
        max_length=144,
        null=True
    )

    questions = models.ManyToManyField(
        Question,
        null=True
    )

    def evaluate(data):
        return False

    def __str__(self):
        return self.name

    def delete(self):
        for q in self.questions:
            q.delete()
        super(Module, self).delete()

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

    module_order = models.CharField(
        help_text="The ordering of the modules in array format. It must to start with [ and end with ]",
        verbose_name="Question ordering array",
        max_length=144,
        null=True
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

    module = models.ManyToManyField(
        Module,
        null=True
    )

    category = models.ManyToManyField(
        CourseCategory,
        null=True
    )

    def wipe_out(self):
        for m in self.module.all():
            m.delete()
        super(Course, self).delete()

    def visible(self):
        return self.is_visible

    def getQuestions(self):
        return self.question_set

    def __str__(self):
        return self.name
