class Course(models.Model):
    """
    One course is a group of questions which should be solved 
    together. These questions should have similar topics, 
    difficulty and should form a complete unit for learning.
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
        :author: Claas Voelcker
        :returns: length of the containing modules queryset
        """
        return len(Module.objects.filter(course=self))

