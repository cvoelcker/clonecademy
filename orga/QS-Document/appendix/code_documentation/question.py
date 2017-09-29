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

