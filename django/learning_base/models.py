from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.contrib.auth.models import User
from django.utils import timezone
from polymorphic.models import PolymorphicModel
# from user_model import models as ub_models


def get_link_to_profile(user):
    '''
    Returns the link to the users profile page
    '''
    #TODO: Implement correct user profile access string
    return "clonecademy.com/this/users/profile"


def valid_mod_request(user):
    request = ModRequest.objects.filter(user=user)
    return request.exists() and (request.first().date - timezone.localdate()).days < -7


def is_mod(user):
    return user.groups.filter(name="moderator").exists()

def is_admin(user):
    return user.groups.filter(name="admin").exists()


class ModRequest(models.Model):
    '''
    Represents a moderation request and saves the corresponding user and time to
    evaluate new requests.
    '''
    class Meta():
        ordering = ["date",]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False
    )

    date = models.DateField(
        blank=False,
        default=timezone.now
    )


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    birth_date = models.DateField(
        blank=True,
        null = True,
    )

    def get_age(self):
        today = timezone.today
        return today.year - self.birth_date.year - ((today.month, today.day) < \
            (self.birth_date.month, self.birth_date.day))


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
        User,
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

    def num_of_modules(self):
        return len(Module.objects.filter(course=self))


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

    def num_of_questions(self):
        return len(Question.objects.filter(module=self))


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
        verbose_name="Module",
        help_text="The corresponding module for the question",
        on_delete=models.CASCADE
    )

    def feedback_is_set(self):
        return len(feedback) != 0

    def __str__(self):
        return self.question_title


class LearningGroup(models.Model):
    """
    A user group (currently not used)
    """
    name = models.CharField(help_text="The name of the user group", max_length=144)

    def __str__(self):
        return self.name


class Try(models.Model):
    '''
    A try represents a submission of an answer. Each time an answer is submitted, a Try
    object is created in the database, detailing answer, wether it was answered
    correctly and the time of the submission.
    '''
    person = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )

    question = models.ForeignKey(
        Question,
        null=True,
        on_delete=models.SET_NULL,
    )

    answer = models.TextField(
        verbose_name="The given answer",
        help_text="The answers as pure string",
        null=True
    )

    date = models.DateTimeField(
        default=timezone.now,
        null=True
    )

    solved = models.BooleanField(
        default=False
    )

    def __unicode__(self):
        return "Solution_{}_{}_{}".format(self.question, self.solved, self.date)
