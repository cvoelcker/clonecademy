from django.db import models
from polymorphic.models import PolymorphicModel
from django.contrib.contenttypes.models import ContentType
from user_model import models as ub_models

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


class Course(models.Model):
    """
    One course is a group of questions which build on each other and should be solved
    together. These questions should have similar topics, difficulty and should form
    a compete unit for learning.
    """
    QUESTION_NAME_LENGTH = 144

    EASY = 0
    MODERATE = 1
    DIFFICULT = 2
    EXPERT = 3
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

    category = models.ForeignKey(
        CourseCategory,
        null=True,
        blank = True
    )

    course_difficulty = models.IntegerField(
        verbose_name='Course difficulty',
        choices=DIFFICULTY,
        default=MODERATE
    )

    responsible_mod = models.ForeignKey(
        ub_models.Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_visible = models.BooleanField(
        verbose_name='Is the course visible',
        default=False
    )

    def __str__(self):
        return self.name


class Module(models.Model):
    """
    A Course is made out of many modules and a module and in a Module can be n questions
    """
    class Meta():
        unique_together = ['module_order', 'course']
        ordering = ['module_order']

    name = models.CharField(
        help_text="A short concise name for the module",
        verbose_name='Module name',
        max_length=144
    )

    learning_text = models.TextField(
        help_text="The learning Text for the module",
        verbose_name="Learning text"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    module_order = models.IntegerField()

    def __str__(self):
        return self.name

    def delete(self):
        for q in self.questions:
            q.delete()
        super(Module, self).delete()


class Question(PolymorphicModel):
    """
    A question is the smallest unit of the learning process. A question has a task that
    can be solved by a user, a correct solution to evaluate the answer and a way to
    provide feedback to the user.
    """
    class Meta():
        unique_together = ['module', 'question_order']
        ordering = ['module', 'question_order']

    question_title = models.TextField(
        verbose_name='Question title',
        help_text="A short and concise name for the question"
    )

    question_body = models.TextField(
        verbose_name='Question text',
        help_text="This field can contain markdown syntax"
    )

    feedback = models.TextField(
        verbose_name="feedback",
        help_text="The feedback for the user after a sucessful answer"
    )

    question_order = models.IntegerField()

    module = models.ForeignKey(
        Module,
        verbose_name="feedback",
        help_text="The corresponding module for the question",
        on_delete=models.CASCADE
    )

    def feedback_is_set(self):
        return len(feedback) != 0

    def __str__(self):
        return self.question_title
