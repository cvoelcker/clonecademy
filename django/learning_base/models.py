from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from polymorphic.models import PolymorphicModel


# from user_model import models as ub_models


class Profile(models.Model):
    """
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    birth_date = models.DateField(
        blank=True,
        null=True,
    )

    last_modrequest = models.DateField(
        blank=True,
        null=True,
    )

    language = models.CharField(
        verbose_name='Language',
        max_length=2,
        default="en"
    )

    avatar = models.TextField(
        verbose_name="Avatar of the User",
        null=True,
        blank=True,
    )

    ranking = models.IntegerField(
        default=0
    )

    def get_age(self):
        today = timezone.today
        return today.year - self.birth_date.year - ((today.month, today.day) <
                                                    (self.birth_date.month,
                                                     self.birth_date.day))

    def __str__(self):
        return str(self.user)

    def get_link_to_profile(self):
        """
        Returns the link to the users profile page
        """
        # TODO: Implement correct user profile access string
        return "clonecademy.net/user/{}/".format(self.user.id)

    def modrequest_allowed(self):
        """
        Returns True if the user is allowed to request moderator rights
        """
        return (self.last_modrequest is None or (
                timezone.localdate() - self.last_modrequest).days >= 7) and \
            not self.is_mod()

    # TODO: Refactor these to a decorator
    def is_mod(self):
        """
        Returns True if the user is in the group moderators
        """
        return self.user.groups.filter(name="moderator").exists()

    def is_admin(self):
        """
        Returns True if the user is in the group admin
        """
        return self.user.groups.filter(name="admin").exists()


class CourseCategory(models.Model):
    """
    The type of a course, meaning the field in which the course belongs, e.g.
    biochemistry, cloning, technical details.
    """
    name = models.CharField(
        help_text="Name of the category (e.g. biochemistry)",
        max_length=144,
        unique=True,
    )

    def get_courses(self):
        return self.course_set

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    One course is a group of questions which build on each other and should be
    solved together. These questions should have similar topics, difficulty
    and should form a compete unit for learning.
    """

    class Meta:
        unique_together = ['category', 'name']

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

    GER = 'de'
    ENG = 'en'
    LANGUAGES = (
        (GER, 'German/Deutsch'),
        (ENG, 'English')
    )

    name = models.CharField(
        verbose_name='Course name',
        help_text="A short concise name for the course",
        max_length=144
    )

    category = models.ForeignKey(
        CourseCategory,
        null=True,
        blank=True
    )

    difficulty = models.IntegerField(
        verbose_name='Course difficulty',
        choices=DIFFICULTY,
        default=MODERATE
    )

    language = models.CharField(
        verbose_name='Course Language',
        max_length=2,
        choices=LANGUAGES,
        default=ENG
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

    description = models.CharField(
        max_length=144,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    def num_of_modules(self):
        """
        Returns the number of modules
        """
        return len(Module.objects.filter(course=self))


class Module(models.Model):
    """
    A Course is made out of several modules and a module contains the questions
    """

    class Meta():
        unique_together = ['order', 'course']
        ordering = ['order']

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

    order = models.IntegerField()

    description = models.CharField(
        max_length=144,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    def num_of_questions(self):
        """
        Returns the number of questions in the module
        """
        return len(self.question_set.all())

    def get_previous_in_order(self):
        """
        Gets the previous module in the ordering
        :return: the previous module in the same course
        """
        modules = self.course.module_set.all()
        if list(modules).index(self) <= 0:
            return False
        return modules[list(modules).index(self) - 1]

    def is_first_module(self):
        """
        checks whether the given module is the first in a course
        :return: True, iff this module has the lowest order in the course
        """
        modules = self.course.module_set
        return self == modules.first()

    def is_last_module(self):
        """
        Returns True if this is the final module in a course
        """
        modules = self.course.module_set
        return self == modules.last()


class Question(PolymorphicModel):
    """
    A question is the smallest unit of the learning process. A question has a
    task that can be solved by a user, a correct solution to evaluate the
    answer and a way to provide feedback to the user.
    """

    class Meta:
        unique_together = ['module', 'order']
        ordering = ['module', 'order']

    title = models.TextField(
        verbose_name='Question title',
        help_text="A short and concise name for the question",
        blank=True,
        null=True
    )

    text = models.TextField(
        verbose_name='Question text',
        help_text="This field can contain markdown syntax"
    )

    question = models.TextField(
        verbose_name='Question',
        help_text="This field can contain markdown syntax",
        blank=True,
        null=True
    )

    feedback = models.TextField(
        verbose_name="feedback",
        help_text="The feedback for the user after a sucessful answer",
        blank=True,
        null=True
    )

    order = models.IntegerField()

    module = models.ForeignKey(
        Module,
        verbose_name="Module",
        help_text="The corresponding module for the question",
        on_delete=models.CASCADE
    )

    def is_first_question(self):
        """
        Checks whether this is the first question in the module
        :return: whether this is the first question or not
        """
        questions = self.module.question_set
        return self == questions.first()

    def is_last_question(self):
        """
        Checks whether this is the last question in the module
        :return: whether this is the last question or not
        """
        questions = self.module.question_set
        return self == questions.last()

    def get_previous_in_order(self):
        """
        Returns the previous question in the course
        :return: the previous question in the same module
        """
        questions = self.module.question_set.all()
        if list(questions).index(self) <= 0:
            return False
        return questions[list(questions).index(self) - 1]

    def __str__(self):
        return self.title


class LearningGroup(models.Model):
    """
    A user group (currently not used)
    """
    name = models.CharField(
        help_text="The name of the user group",
        max_length=144)

    def __str__(self):
        return self.name


class Try(models.Model):
    """
    A try represents a submission of an answer. Each time an answer is
    submitted, a Try object is created in the database, detailing answer,
    whether it was answered correctly and the time of the submission.
    """
    user = models.ForeignKey(
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
        return "Solution_{}_{}_{}".format(
            self.question, self.solved, self.date)


class CourseManager(models.Manager):
    def is_started(user):
        courses = Course.objects.filter(
            module__question__try__user=user)
        return courses.distinct()
