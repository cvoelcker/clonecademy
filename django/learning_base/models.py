"""
This module contains all database models not provided by django
itself.
:author: Claas Voelcker
"""

from hashlib import sha512
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from polymorphic.models import PolymorphicModel

from .default_picture import default_picture

class Settings(models.Model):
    """
    The settings for the website.
    :author: Leonhard Wiedmann
    """

    name = models.CharField(
        verbose_name='Title of the Homepage',
        max_length=40,
        default='CloneCademy'
    )

    image = models.TextField(
        verbose_name='Main image of the Homepage',
        default=''
    )

    email = models.EmailField(
        verbose_name='Email to send system informations',
        default=''
    )

    img = models.ImageField(
        blank=True,
        upload_to="media/base"
    )

class Profile(models.Model):
    """
    A user profile that stores additional information about a user
    :author: Claas Voelcker
    """

    class Meta:
        ordering = ('ranking',)

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
        default=default_picture,
        null=True,
        blank=True,
    )

    ranking = models.IntegerField(
        default=0
    )

    def get_link_to_profile(self):
        """
        :return: the link to the users profile page
        """
        return "clonecademy.net/admin/profiles/{}/".format(self.user.id)

    def modrequest_allowed(self):
        """
        :return: True if the user is allowed to request moderator rights
        """
        return (not self.is_mod()
                and (self.last_modrequest is None
                     or (timezone.now() - self.last_modrequest).days >= 7))

    def is_mod(self):
        """
        :return: True if the user is in the group moderators
        """
        return self.user.groups.filter(name="moderator").exists()

    def is_admin(self):
        """
        Returns True if the user is in the group admin
        :return: whether the user belong to the admin group
        """
        return self.user.groups.filter(name="admin").exists()

    def get_hash(self):
        """
        calculates a hash to get anonymous user data
        :return: the first 10 digits of the hash
        """
        return sha512(str.encode(self.user.username)).hexdigest()[:10]

    def __str__(self):
        return str(self.user)


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

    color = models.CharField(
        help_text="Color that is used in the category context",
        max_length=7,
        default="#000000"
    )

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    One course is a group of questions which build on each other and should be
    solved together. These questions should have similar topics, difficulty
    and should form a compete unit for learning.
    :author: Claas Voelcker
    """

    class Meta:
        unique_together = ['category', 'name']

    # difficulty selection and mapping to human readable names
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

    # language selection and mapping
    GER = 'de'
    ENG = 'en'
    LANGUAGES = (
        (GER, 'German/Deutsch'),
        (ENG, 'English')
    )

    # the name of the course
    name = models.CharField(
        verbose_name='Course name',
        help_text="A short concise name for the course",
        max_length=144
    )

    # foreign key mapping to the CourseCategory object
    category = models.ForeignKey(
        CourseCategory,
        null=True,
        blank=True
    )

    # choice field mapped to dictionary above
    difficulty = models.IntegerField(
        verbose_name='Course difficulty',
        choices=DIFFICULTY,
        default=MODERATE
    )

    # choice field mapped to dictionary above
    language = models.CharField(
        verbose_name='Course Language',
        max_length=2,
        choices=LANGUAGES,
        default=ENG
    )

    # foreign key mapping to the user who can edit the course
    responsible_mod = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # should the course be serialized for normal users
    is_visible = models.BooleanField(
        verbose_name='Is the course visible',
        default=False
    )

    # a short description of the course
    description = models.CharField(
        max_length=144,
        null=True,
        blank=True,
        default=""
    )

    def __str__(self):
        return self.name

    def num_of_modules(self):
        """
        Returns the number of modules
        """
        return len(Module.objects.filter(course=self))

    def delete(self):
        for module in self.module_set.all():
            for question in module.question_set.all():
                question.delete()
            module.delete()
        super(Course, self).delete()

class Module(models.Model):
    """
    A Course is made out of several modules and a module contains the questions
    """

    class Meta:
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

    :author: Claas Voelcker
    """

    class Meta:
        unique_together = ['module', 'order']
        ordering = ['module', 'order']

    # a title for the question
    title = models.TextField(
        verbose_name='Question title',
        help_text="A short and concise name for the question",
        blank=True,
        null=True
    )

    # the question text, that provides additional information to the user
    text = models.TextField(
        verbose_name='Question text',
        help_text="This field can contain markdown syntax"
    )

    # the specific question
    question = models.TextField(
        verbose_name='Question',
        help_text="This field can contain markdown syntax",
        blank=True,
        null=True
    )

    # a custom feedback that can be displayed
    feedback = models.TextField(
        verbose_name="feedback",
        help_text="The feedback for the user after a sucessful answer",
        blank=True,
        null=True
    )

    # the ordering attribute of the question (needs to be explicitly saved)
    order = models.IntegerField()

    # foreign key mapping to the module that contains this question
    module = models.ForeignKey(
        Module,
        verbose_name="Module",
        help_text="The corresponding module for the question",
        on_delete=models.CASCADE
    )

    def is_first_question(self):
        """
        Checks whether this is the first question in the module

        :author: Claas Voelcker
        :return: whether this is the first question or not
        """
        questions = self.module.question_set
        return self == questions.first()

    def is_last_question(self):
        """
        Checks whether this is the last question in the module

        :author: Claas Voelcker
        :return: whether this is the last question or not
        """
        questions = self.module.question_set
        return self == questions.last()

    def get_previous_in_order(self):
        """
        Returns the previous question in the course
        :author: Claas Voelcker
        :return: the previous question in the same module
        """
        questions = self.module.question_set.all()
        if list(questions).index(self) <= 0:
            return False
        return questions[list(questions).index(self) - 1]

    def get_points(self):
        """
        Returns the number of ranking points for the question.
        This method needs to be overridden by subclasses and
        remains unimplemented here.
        :author: Claas Voelcker
        :return: the points
        :raise: not implemented error
        """
        raise NotImplementedError

    def __str__(self):
        return self.title


class QuizQuestion(models.Model):
    """
    single Quiz Question with possible multiple answers
    @author Leonhard Wiedmann
    """
    question = models.TextField(
        verbose_name="quizQuestion",
        help_text="The Question of this quiz question.",
        default=""
    )

    image = models.TextField(
        help_text="The image which is shown in this quiz",
        default="",
        blank=True
    )

    course = models.ForeignKey(
        Course,
        help_text="The Course of this question",
        on_delete=models.CASCADE
    )

    def evaluate(self, data):
        """
        Checks whether the quiz question is answered correctly
        :return: True iff all and only the correct answers are
                 provided
        """
        answers = self.answer_set()
        for ans in answers:
            if ans.correct:
                for i in data['answers']:
                    if 'id' in i and (i['id'] == ans.id and not i['chosen']):
                        return False
            if not ans.correct:
                for i in data:
                    if 'id' in i and (i['id'] == ans.id and i['chosen']):
                        return False
        return True

    def answer_set(self):
        """
        shortcut for all answers to a question
        :return: all answers to the quizquestion
        """
        return self.quizanswer_set.all()

    def is_solvable(self):
        """
        x
        :return:
        """
        for ans in self.answer_set():
            if ans.correct:
                return True
        return False

    def get_points(self):
        """
        returns the points for answering this question type
        :return: 0 points
        """
        return 0


class QuizAnswer(models.Model):
    """
    Quiz answer with image and the value for correct answer
    @author Leonhard Wiedmann
    """
    text = models.TextField(
        help_text="The answer text"
    )

    img = models.TextField(
        help_text="The image for this answer",
        default="",
        blank=True
    )

    correct = models.BooleanField(
        help_text="If this answer is correct",
        default=False
    )

    quiz = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)


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
    :author: Claas Voelcker
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

    quiz_question = models.ForeignKey(
        QuizQuestion,
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

    def __str__(self):
        return "Solution_{}_{}_{}".format(
            self.question, self.solved, self.date)


def started_courses(user):
    """
    returns all courses started by a user
    :param user: the user that is currently accessing the database
    :return: all courses where the user has answered at least one course
    """
    courses = Course.objects.filter(
        module__question__try__user=user)
    return courses.distinct()
