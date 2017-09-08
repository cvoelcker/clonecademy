from rest_framework import serializers
from rest_framework.exceptions import ParseError

from .info.serializer import InformationYoutubeSerializer, \
    InformationTextSerializer
from .multiple_choice.serializer import \
    MultipleChoiceQuestionSerializer
from .models import Question, CourseCategory, Module, Course, QuizQuestion, \
    QuizAnswer, LearningGroup, Try, Profile

from django.contrib.auth.models import User


class AnswerSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        serializer = obj.get_serializer()
        return serializer(obj).data


class QuestionSerializer(serializers.ModelSerializer):
    """
    The serializer responsible for the Question object
    @author: Claas Voelcker
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
        Input:
            obj: The object that should be serialized (Question)
        Output:
            value: a valid json object containing all required fields
        """
        module = obj.module
        value = super(QuestionSerializer, self).to_representation(obj)
        value['type'] = obj.__class__.__name__
        user = self.context['request'].user

        # calculate the current progress of the user in a array of arrays
        # the outer array is the module and the inner
        # is the title of the quesiton
        # e.g [['question 1', 'question, 2'], ['quesiton 3']]
        value['progress'] = []
        answered_question_before = True
        for module in obj.module.course.module_set.all():
            m = []
            for question in module.question_set.all():
                if answered_question_before and question.try_set.filter(
                        solved=True, user=user).exists():
                    m.append({"solved": True, "title": question.title})

                else:
                    answered_question_before = False
                    m.append({"solved": False, "title": question.title})
            value['progress'].append(m)

        value['last_question'] = obj.is_last_question()
        value['last_module'] = module.is_last_module()
        value['learning_text'] = module.learning_text
        serializer = obj.get_serializer()
        value['question_body'] = serializer(obj).data

        value['solved'] = obj.try_set.filter(solved=True, user=user).exists()

        return value

    def create(self, validated_data):
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
    class Meta:
        model = Question
        fields = ("title", "text", 'id', "feedback")

    def to_representation(self, obj):
        value = super(QuestionEditSerializer, self).to_representation(obj)
        value['type'] = obj.__class__.__name__
        serializer = obj.get_edit_serializer()
        value['question_body'] = serializer(obj).data
        return value


class CourseCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseCategory
        fields = ('name', "color", "id",)

    color = serializers.RegexField(r'^#[a-fA-F0-9]{6}', max_length=7,
                                   min_length=7, allow_blank=False)


class ModuleEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('name', "id", "learning_text", "order")

    def to_representation(self, obj):
        value = super(ModuleEditSerializer, self).to_representation(obj)

        questions = obj.question_set.all()
        value['questions'] = QuestionEditSerializer(questions, many=True).data
        return value


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('name', 'learning_text', 'id')

    def to_representation(self, obj):
        """
        This function makes the serialization and is needed to correctly
        display nested objects.
        """

        value = super(ModuleSerializer, self).to_representation(obj)

        questions = Question.objects.filter(module=obj)
        questions = QuestionSerializer(
            questions, many=True, read_only=True, context=self.context).data

        value["questions"] = questions
        return value

    def create(self, validated_data):
        """
        This method is used to save modules and their respective questions
        """
        questions = validated_data.pop('questions')

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
            for q in query_questions:
                if q.id not in question_id:
                    q.delete()

        for question in questions:
            question['module'] = module
            question_serializer = QuestionSerializer(data=question)
            if not question_serializer.is_valid():
                raise ParseError(
                    detail="Error in question serialization", code=None)
            else:
                question_serializer.create(question)


class CourseSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Course
        fields = ('name', 'difficulty', 'id', 'language', 'category',
                  'description')

    def to_representation(self, obj):
        """
        This function serializes the courses.
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
        """
        modules = validated_data.pop('modules')
        quiz = False
        if 'quiz' in validated_data:
            quiz = validated_data.pop('quiz')

        # check if course is empty and raise error if so
        if len(modules) <= 0:
            raise ParseError(detail="Course needs to have at least one module",
                             code=None)
        category = validated_data.pop('category')
        category = CourseCategory.objects.get(name=category)
        validated_data['category'] = category
        course = Course(**validated_data)
        course.save()

        # add quiz to a course
        if quiz is not False:
            try:
                if len(quiz) >= 5 and len(quiz) <= 20:
                    # delete quiz
                    quiz_id = []
                    for q in quiz:
                        if 'id' in q:
                            quiz_id.append(q['id'])
                    if quiz_id:
                        for q in course.quizquestion_set.all():
                            if q.id not in quiz_id:
                                q.delete()

                    for q in quiz:

                        quiz_serializer = QuizSerializer(data=q)
                        if not quiz_serializer.is_valid():
                            raise ParseError(
                                detail=str(quiz_serializer.errors),
                                code=None)
                        else:
                            q['course'] = course
                            quiz_serializer.create(q)
            except ParseError as e:
                if 'id' not in validated_data:
                    course.delete()
                raise ParseError(detail=e.detail, code=None)

        # create a array with the ids for all module ids of this course
        module_id = []
        for m in modules:
            if 'id' in m:
                module_id.append(m['id'])

        # check if this is a edit or creation of a new course
        if module_id:
            # get all modules for the current course
            module_query = Module.objects.filter(
                course_id=validated_data['id'])
            # iterate over the modules and if the modules does not exist in the
            # edited course it will be removed
            for m in module_query:
                if m.id not in module_id:
                    m.delete()

        try:
            if len(modules) <= 0:
                raise ParseError(detail="no Empty course allowed", code=None)
            for module in modules:
                module_serializer = ModuleSerializer(data=module)
                if not module_serializer.is_valid():
                    raise ParseError(
                        detail="Error in module serialization", code=None)
                else:
                    module['course'] = course
                    module_serializer.create(module)
            return True
        except ParseError as e:
            if 'id' not in validated_data:
                course.delete()
            raise ParseError(detail=e.detail, code=None)


class CourseEditSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Course
        fields = (
            "name", "id", "category", "difficulty", "language",
            "responsible_mod",
            "is_visible", "description")

    def to_representation(self, obj):
        value = super(CourseEditSerializer, self).to_representation(obj)
        all_modules = obj.module_set.all()
        modules = ModuleEditSerializer(all_modules, many=True).data
        value['modules'] = modules

        all_quiz = obj.quizquestion_set.all()
        quiz = QuizSerializer(all_quiz, many=True, context={"edit": True}).data
        value['quiz'] = quiz

        return value


class QuizSerializer(serializers.ModelSerializer):
    """
    Quiz Serializer for a single quiz question
    @author Leonhard Wiedmann
    """

    class Meta:
        model = QuizQuestion
        fields = ('question', 'image', 'id',)

    def create(self, validated_data):
        if 'answers' not in validated_data:
            return False
        answers = validated_data.pop('answers')
        quiz = QuizQuestion(**validated_data)
        quiz.save()
        try:
            if len(answers) != 4:
                raise ParseError(detail="Quiz must have 4 answers", code=None)
            for ans in answers:
                quiz_answer_serializer = QuizAnswerSerializer(data=ans)
                if not quiz_answer_serializer.is_valid():
                    raise ParseError(detail=str(quiz_answer_serializer.errors),
                                     code=None)
                else:
                    ans['quiz'] = quiz
                    quiz_answer_serializer.create(ans)
            if not quiz.is_solvable():
                raise ParseError(detail="This quiz is not solvable", code=None)
        except ParseError as e:
            quiz.delete()
            raise ParseError(detail=e.detail, code=None)

    def to_representation(self, obj):
        value = super(QuizSerializer, self).to_representation(obj)
        value['answers'] = QuizAnswerSerializer(obj.answer_set(), many=True,
                                                context=self.context).data
        return value


class QuizAnswerSerializer(serializers.ModelSerializer):
    """
    Quiz Answer Serializer
    @author Leonhard Wiedmann
    """

    class Meta:
        model = QuizAnswer
        fields = ('text', 'img', 'id')

    def create(self, validated_data):
        quiz_answer = QuizAnswer(**validated_data)
        quiz_answer.save()

    def to_representation(self, obj):
        value = super(QuizAnswerSerializer, self).to_representation(obj)
        if 'edit' in self.context and self.context['edit']:
            value['correct'] = obj.correct
        return value


class GroupSerializer(serializers.ModelSerializer):
    """
    Model serializer for the Group model
    """

    class Meta:
        model = LearningGroup
        fields = ('name', "id")


class UserSerializer(serializers.ModelSerializer):
    """
    Model serializer for the User model
    """

    groups = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'id', 'date_joined', 'groups', 'first_name',
            'last_name')

    def to_representation(self, obj):
        value = super(UserSerializer, self).to_representation(obj)

        if 'language' not in value:
            value['language'] = "en"
        p = Profile.objects.filter(user=obj).first()
        value['language'] = p.language
        value['ranking'] = p.ranking
        return value

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        validated_data.pop('groups')
        # TODO add language to profile
        if 'language' in profile_data:
            profile_data['language'] = validated_data.pop('language')
        user = User.objects.create_user(**validated_data)
        profile = Profile(user=user, **profile_data)
        profile.save()
        return True

    def update(self, instance, validated_data):
        """
        Updates a given user instance
        Note: Only updates fields changeable by user
        @author Tobias Huber
        Thoughts: Add birth_date when neccessary
        """
        # instance.username = validated_data["username"]
        instance.email = validated_data["email"]
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        profile = instance.profile
        profile.language = validated_data["language"]
        profile.save()
        instance.save()
        return True


class TrySerializer(serializers.ModelSerializer):
    """
    Model serializer for the Try model
    """
    user = serializers.StringRelatedField()
    question = serializers.StringRelatedField()

    class Meta:
        model = Try
        fields = ('user', 'question', 'date', 'solved')


class StatisticsOverviewSerializer(serializers.BaseSerializer):
    """
    Longer serializer for the statistics overview
    """

    def to_representation(self, user):
        all_questions = list()
        for question in Question.objects.all():
            question_string = str(question)
            question_entry = dict()
            try_set = Try.objects.filter(question=question, user=user)
            for _try in try_set:
                if not question_entry:
                    question_entry = {
                        'question': question_string,
                        'solved': _try.solved,
                        'tries': 1
                    }
                else:
                    question_entry['tries'] += 1
                    question_entry['solved'] = question_entry['solved'] \
                        or _try.solved
            if question_entry:
                all_questions.append(question_entry)
        return all_questions


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
