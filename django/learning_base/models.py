"""
x
"""

from hashlib import sha512
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from polymorphic.models import PolymorphicModel


class Profile(models.Model):
    """
    A user profile that stores additional information about a user
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
        default="data:image/png;base64,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",
        null=True,
        blank=True,
    )

    ranking = models.IntegerField(
        default=0
    )

    def get_age(self):
        """
        Caculates the current age of the user
        :return: the age of the user relative to the current server date
        """
        today = timezone.now()
        return today.year - self.birth_date.year - ((today.month, today.day) <
                                                    (self.birth_date.month,
                                                     self.birth_date.day))

    def get_link_to_profile(self):
        """
        Returns the link to the users profile page
        """
        return "clonecademy.net/admin/profiles/{}/".format(self.user.id)

    def modrequest_allowed(self):
        """
        Returns True if the user is allowed to request moderator rights
        """
        return ((self.last_modrequest is None
                 or (timezone.localdate() - self.last_modrequest).days >= 7)
                and not self.is_mod())

    def is_mod(self):
        """
        Returns True if the user is in the group moderators
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

    def get_points(self):
        """
        x
        :return:
        """
        raise NotImplementedError


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
        x
        :return:
        """
        answers = self.answer_set()
        for ans in answers:
            if ans.correct:
                if not data[str(ans.id)]:
                    return False
            if not ans.correct:
                if data[str(ans.id)]:
                    return False
        return True

    def answer_set(self):
        """
        x
        :return:
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

    @staticmethod
    def get_points():
        """
        returns the points for answering this question type
        :return: 2 points
        """
        return 2


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
    :param user:
    :return:
    """
    courses = Course.objects.filter(
        module__question__try__user=user)
    return courses.distinct()
