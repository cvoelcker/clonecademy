"""
module containing all serializers
"""

from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.exceptions import ParseError

from .info.serializer import InformationYoutubeSerializer, \
    InformationTextSerializer
from .multiple_choice.serializer import \
    MultipleChoiceQuestionSerializer
from .models import Question, CourseCategory, Module, Course, QuizQuestion, \
    QuizAnswer, LearningGroup, Try, Profile


def get_answer_serializer(obj):
    """
    dispatch function that chooses the correct serializer
    :param obj: the answers object to be serialiaized
    :return: a json serialization
    """
    serializer = obj.get_serializer()
    return serializer(obj).data


class QuestionSerializer(serializers.ModelSerializer):
    """
    The serializer responsible for the Question object
    :author: Claas Voelcker
    """

    class Meta:
        """
        Meta information (which fields are serialized for the representation)
        """
        model = Question
        fields = ('title', 'text', 'feedback',)

    def to_representation(self, obj):
        """
        Appends additional information to the model.
        :param: obj: The object that should be serialized (Question)
        :return: value: a valid json object containing all required fields
        """
        course_module = obj.module
        value = super(QuestionSerializer, self).to_representation(obj)
        value['type'] = obj.__class__.__name__
        user = self.context['request'].user

        # calculate the current progress of the user in a array of arrays
        # the outer array is the module and the inner
        # is the title of the quesiton
        # e.g [['question 1', 'question, 2'], ['quesiton 3']]
        value['progress'] = []
        answered_question_before = True
        for course_module in obj.module.course.module_set.all():
            module_set = []
            for question in course_module.question_set.all():
                if answered_question_before and question.try_set.filter(
                        solved=True, user=user).exists():
                    module_set.append({'solved': True, 'title': question.title})

                else:
                    answered_question_before = False
                    module_set.append({'solved': False, 'title': question.title})
            value['progress'].append(module_set)

        value['last_question'] = obj.is_last_question()
        value['last_module'] = course_module.is_last_module()
        value['learning_text'] = course_module.learning_text
        serializer = obj.get_serializer()
        value['question_body'] = serializer(obj).data

        value['solved'] = obj.try_set.filter(solved=True, user=user).exists()

        return value

    def create(self, validated_data):
        """
        Serializer that governs the dispatch to specific class serializers
        :param validated_data: the data to be serialized
        :return: serialized representation
        """
        question_type = validated_data.pop('type')
        if question_type == 'multiple_choice':
            MultipleChoiceQuestionSerializer().create(validated_data)
        elif question_type == 'info_text':
            InformationTextSerializer().create(validated_data)
        elif question_type == 'info_text_youtube':
            InformationYoutubeSerializer().create(validated_data)
        else:
            raise ParseError(
                detail='{} is not a valid question type'.format(
                    question_type))


class QuestionEditSerializer(serializers.ModelSerializer):
    """
    The serializer to get all information to edit a question
    :author: Leonhard Wiedmann
    """
    class Meta:
        model = Question
        fields = ('title', 'text', 'id', 'feedback')

    def to_representation(self, obj):
        """
        to json representation serialization
        :param obj: the object to be serialized
        :return: a serialized representation
        """
        value = super(QuestionEditSerializer, self).to_representation(obj)
        value['type'] = obj.__class__.__name__
        serializer = obj.get_edit_serializer()
        value['question_body'] = serializer(obj).data
        return value


class CourseCategorySerializer(serializers.ModelSerializer):
    """
    A serializer for course categories
    :author: Claas Voelcker
    """
    class Meta:
        model = CourseCategory
        fields = ('name', 'color', 'id',)

    color = serializers.RegexField(r'^#[a-fA-F0-9]{6}', max_length=7,
                                   min_length=7, allow_blank=False)


class ModuleEditSerializer(serializers.ModelSerializer):
    """
    A serializer to get module editing data
    :auhor: Leonhard Wiedmann
    """
    class Meta:
        model = Module
        fields = ('name', 'id', 'learning_text', 'order')

    def to_representation(self, obj):
        """
        responsible for returning a valid json response
        :param obj: the object to be serialized
        :return: a valid json representation
        """
        value = super(ModuleEditSerializer, self).to_representation(obj)

        questions = obj.question_set.all()
        value['questions'] = QuestionEditSerializer(questions, many=True).data
        return value


class ModuleSerializer(serializers.ModelSerializer):
    """
    The serializer for modules
    :author: Leonhard Wiedmann
    """
    class Meta:
        model = Module
        fields = ('name', 'learning_text', 'id')

    def to_representation(self, obj):
        """
        This function makes the serialization and is needed to correctly
        display nested objects.
        :param obj: a
        :return:
        """

        value = super(ModuleSerializer, self).to_representation(obj)

        questions = Question.objects.filter(module=obj)
        questions = QuestionSerializer(
            questions, many=True, read_only=True, context=self.context).data

        value['questions'] = questions
        return value

    def create(self, validated_data):
        """
        This method is used to save modules and their respective questions
        """
        questions = validated_data.pop('questions')

        if questions is None or len(questions) is 0:
            raise ParseError(detail='empty module is not allowed', code=None)

        module = Module(**validated_data)
        module.course = validated_data['course']
        module.save()

        question_id = []
        # create a array with the ids for all questions of this module
        for quest in questions:
            if 'id' in quest:
                question_id.append(quest['id'])

        # check if this is a edit or creation of a new module
        if question_id:
            # get all questions for the current module
            query_questions = Question.objects.filter(
                module_id=validated_data['id'])
            # iterate over the questions and if the questions does not exist in
            # the edited module it will be removed
            for question in query_questions:
                if question.id not in question_id:
                    question.delete()

        for question in questions:
            question['module'] = module
            question_serializer = QuestionSerializer(data=question)
            if not question_serializer.is_valid():
                raise ParseError(
                    detail='Error in question serialization', code=None)
            else:
                question_serializer.create(question)


class CourseSerializer(serializers.ModelSerializer):
    """
    A serializer to view courses
    """
    category = serializers.StringRelatedField()
    is_visible = serializers.BooleanField(required=False,
                                          default=False)

    class Meta:
        model = Course
        fields = ('name', 'difficulty', 'id', 'language', 'category',
                  'is_visible', 'description')

    def to_representation(self, obj):
        """
        This function serializes the courses.
        :param obj: the object to be serialized
        :return: a json serialization
        """

        value = super(CourseSerializer, self).to_representation(obj)

        all_modules = obj.module_set.all()
        modules = ModuleSerializer(all_modules, many=True, read_only=True,
                                   context=self.context).data

        value['modules'] = modules

        num_questions = 0
        num_answered = 0
        count_question = 0
        count_module = 0
        for module in modules:
            count_module += 1
            for question in module['questions']:
                count_question += 1
                if question['solved']:
                    num_answered += 1
                else:
                    value['next_question'] = count_question
                    value['current_module'] = count_module
                num_questions += 1
        value['num_answered'] = num_answered
        value['num_questions'] = num_questions
        value['responsible_mod'] = obj.responsible_mod.id
        return value

    def create(self, validated_data):
        """
        This method is used to save courses together with all modules and
        questions.
        :param validated_data: valid data for the Course object
        """
        modules = validated_data.pop('modules')
        quiz_data = []
        if 'quiz' in validated_data:
            quiz_data = validated_data.pop('quiz')

        # check if course is empty and raise error if so
        if not modules:
            raise ParseError(detail='Course needs to have at least one module',
                             code=None)
        category = validated_data.pop('category')
        category = CourseCategory.objects.get(name=category)
        validated_data['category'] = category
        course = Course(**validated_data)
        course.save()

        # add quiz to a course
        if quiz_data and len(quiz_data) >= 5:
            try:
                if 5 <= len(quiz_data) <= 20:
                    quiz_id = [q['id'] for q in quiz_data if 'id' in q.keys()]
                    for quiz in course.quizquestion_set.all():
                        if quiz.id not in quiz_id:
                            quiz.delete()
                    for quiz in quiz_data:
                        quiz_serializer = QuizSerializer(data=quiz)
                        if not quiz_serializer.is_valid():
                            raise ParseError(
                                detail=str(quiz_serializer.errors),
                                code=None)
                        else:
                            quiz['course'] = course
                            quiz_serializer.create(quiz)
            except ParseError as error:
                if 'id' not in validated_data:
                    course.delete()
                raise ParseError(detail=error.detail, code=None)
        else:
            for quiz in course.quizquestion_set.all():
                quiz.delete()

        # create a array with the ids for all module ids of this course
        module_id = []
        for course_module in modules:
            if 'id' in course_module:
                module_id.append(course_module['id'])

        # check if this is a edit or creation of a new course
        if module_id:
            # get all modules for the current course
            module_query = Module.objects.filter(
                course_id=validated_data['id'])
            # iterate over the modules and if the modules does not exist in the
            # edited course it will be removed
            for course_module in module_query:
                if course_module.id not in module_id:
                    course_module.delete()

        try:
            if len(modules) <= 0:
                raise ParseError(detail='no Empty course allowed', code=None)
            for module in modules:
                module_serializer = ModuleSerializer(data=module)
                if not module_serializer.is_valid():
                    raise ParseError(
                        detail='Error in module serialization', code=None)
                else:
                    module['course'] = course
                    module_serializer.create(module)
            return True
        except ParseError as error:
            if 'id' not in validated_data:
                course.delete()
            raise ParseError(detail=error.detail, code=None)


class CourseEditSerializer(serializers.ModelSerializer):
    """
    A serializer that returns all data needed to edit the course
    :author: Leonhard Wiedmann
    """
    category = serializers.StringRelatedField()

    class Meta:
        model = Course
        fields = (
            'name', 'id', 'category', 'difficulty', 'language',
            'responsible_mod',
            'is_visible', 'description')

    def to_representation(self, obj):
        """
        method responsible for serializing a Curse object for editing purposes
        :param obj: the object to be serialized
        :return: a json representation of the object
        """
        value = super(CourseEditSerializer, self).to_representation(obj)
        all_modules = obj.module_set.all()
        modules = ModuleEditSerializer(all_modules, many=True).data
        value['modules'] = modules

        all_quiz = obj.quizquestion_set.all()
        quiz = QuizSerializer(all_quiz, many=True, context={'edit': True}).data
        value['quiz'] = quiz

        return value


class QuizSerializer(serializers.ModelSerializer):
    """
    Quiz Serializer for a single quiz question
    :author: Leonhard Wiedmann
    """

    class Meta:
        model = QuizQuestion
        fields = ('question', 'image', 'id',)

    def create(self, validated_data):
        """
        method creating a Quiz object form a json input
        :param validated_data: validated json data for the object
        """
        if 'answers' not in validated_data:
            raise ParseError(detail='The quiz has no answers',
                             code=None)
        answers = validated_data.pop('answers')
        quiz = QuizQuestion(**validated_data)
        quiz.save()
        try:
            if len(answers) != 4:
                raise ParseError(detail='Quiz must have 4 answers', code=None)
            for ans in answers:
                quiz_answer_serializer = QuizAnswerSerializer(data=ans)
                if not quiz_answer_serializer.is_valid():
                    raise ParseError(detail=str(quiz_answer_serializer.errors),
                                     code=None)
                else:
                    ans['quiz'] = quiz
                    quiz_answer_serializer.create(ans)
            if not quiz.is_solvable():
                raise ParseError(detail='This quiz is not solvable', code=None)
        except ParseError as error:
            quiz.delete()
            raise ParseError(detail=error.detail, code=None)

    def to_representation(self, obj):
        """
        representation of a Quiz object
        :author: Claas Voelcker
        :param obj: the user object to be serialized
        :return: a json representation of the object
        """
        value = super(QuizSerializer, self).to_representation(obj)
        value['answers'] = QuizAnswerSerializer(obj.answer_set(), many=True,
                                                context=self.context).data
        return value


class QuizAnswerSerializer(serializers.ModelSerializer):
    """
    Quiz Answer Serializer
    :author: Leonhard Wiedmann
    """

    class Meta:
        model = QuizAnswer
        fields = ('text', 'img', 'id')

    def create(self, validated_data):
        """
        method creating a QuizAnswer object form a json input
        :param validated_data: validated json data for the object
        """
        quiz_answer = QuizAnswer(**validated_data)
        quiz_answer.save()

    def to_representation(self, obj):
        """
        representation of a Quiz object
        :author: Claas Voelcker
        :param obj: the user object to be serialized
        :return: a json representation of the object
        """
        value = super(QuizAnswerSerializer, self).to_representation(obj)
        if 'edit' in self.context and self.context['edit']:
            value['correct'] = obj.correct
        return value


class GroupSerializer(serializers.ModelSerializer):
    """
    Model serializer for the Group model
    :author: Claas Voelcker
    """

    class Meta:
        model = LearningGroup
        fields = ('name', 'id')


class UserSerializer(serializers.ModelSerializer):
    """
    Model serializer for the User model
    :author: Claas Voelcker
    """

    groups = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'id', 'date_joined', 'groups', 'first_name',
            'last_name')

    def to_representation(self, obj):
        """
        representation of a user object
        :author: Leonhard Wiedmann
        :param obj: the user object to be serialized
        :return: a json representation of the object
        """
        value = super(UserSerializer, self).to_representation(obj)

        if 'language' not in value:
            value['language'] = 'en'
        profile = Profile.objects.filter(user=obj).first()
        value['language'] = profile.language

        value['avatar'] = profile.avatar
        value['ranking'] = profile.ranking
        return value

    def create(self, validated_data):
        """
        method creating a User object form a json input
        :author: Leonhard Wiedmann
        :param validated_data: validated json data for the object
        """
        profile_data = validated_data.pop('profile')
        validated_data.pop('groups')
        if 'language' not in validated_data:
            validated_data['language'] = 'en'
        profile_data['language'] = validated_data.pop('language')
        if 'avatar' in validated_data:
            profile_data['avatar'] = validated_data.pop('avatar')
        # if 'language' in profile_data:
        #    profile_data['language'] = validated_data.pop('language')
        user = User.objects.create_user(**validated_data)
        profile = Profile(user=user, **profile_data)
        profile.save()

    def update(self, instance, validated_data):
        """
        Updates a given user instance
        Note: Only updates fields changeable by user
        :author: Tobias Huber
        :param validated_data: validated data for the input
        """
        instance.email = validated_data['email']
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        # profile.language = validated_data['language']
        if 'avatar' in validated_data:
            profile = instance.profile
            profile.avatar = validated_data['avatar']
            profile.save()
        instance.save()


class TrySerializer(serializers.ModelSerializer):
    """
    Model serializer for the Try model
    :author: Claas Voelcker
    """
    user = serializers.StringRelatedField()
    question = serializers.StringRelatedField()
    date = serializers.DateTimeField(format='%d/%m/%Y')

    class Meta:
        model = Try
        fields = ('user', 'question', 'date', 'solved')

    def to_representation(self, obj):
        """
        converts try objects to a serialized version
        :param obj: the object to be serialized
        :return: a json serialization
        """
        data = super(TrySerializer, self).to_representation(obj)

        if 'serialize' in self.context:
            for serial in self.context['serialize']:
                value = obj
                for child in serial.split('__'):
                    if value is None:
                        break
                    value = getattr(value, child)
                data[serial] = value
        return data


class RankingSerializer(serializers.BaseSerializer):
    """
    A serializer for all rankings
    :author: Claas Voelcker
    """

    def to_representation(self, instance):
        """
        a serialization of profile rankings
        :param instance: an ordered profile list
        :return: a dictionary with ranking information
        """
        value = []
        for profile in instance:
            value.append({
                'name': profile.user.username,
                'id': profile.id,
                'ranking': profile.ranking
            })
        return value
