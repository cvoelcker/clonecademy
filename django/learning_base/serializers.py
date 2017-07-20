from rest_framework import serializers
from rest_framework.exceptions import ParseError
from .models import *
from learning_base.multiple_choice.models import *
from learning_base.drag_and_drop.models import *
from learning_base.multiple_choice.serializer import *
from learning_base.drag_and_drop.serializer import *


class AnswerSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        serializer = obj.get_serializer()
        return serializer(obj).data


class QuestionSerializer(serializers.ModelSerializer):
    '''
    The serializer responsible for the Question object
    @author: Claas Voelcker
    '''

    class Meta:
        '''
        Meta information (which fields are serialized for the representation)
        '''
        model = Question
        fields = ('title', 'body', 'feedback',)

    def to_representation(self, obj):
        '''
        Appends additional information to the model.
        Input:
            obj: The object that should be serialized (Question)
        Output:
            value: a valid json object containing all required fields
        '''

        module = obj.module
        value = super(QuestionSerializer, self).to_representation(obj)
        value['type'] = obj.__class__.__name__
        value['last_question'] = obj.is_last_question()
        value['last_module'] = module.is_last_module()
        value['learning_text'] = module.learning_text
        serializer = obj.get_serializer()
        value['question_body'] = serializer(obj).data
        user = self.context['request'].user
        value['solved'] = obj.try_set.filter(solved=True)
        value['solved'] = value['solved'].filter(user=user)
        value['solved'] = value['solved'].exists()

        return value

    def create(self, validated_data):
        question_type = validated_data.pop('type')

        if question_type == 'multiple_choice':
            MultipleChoiceQuestionSerializer().create(validated_data)
        elif question_type == 'drag_and_drop':
            pass
        else:
            raise ParseError(
                detail='{} is not a valid question type'.format(
                    question_type))


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ('name', "id",)


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
        '''
        This method is used to save modules and their respective questions
        '''
        questions = validated_data.pop('questions')
        module = Module(**validated_data)
        module.course = validated_data['course']
        module.save()
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
        fields = ('name', 'difficulty', 'id', 'language', 'category')

    def to_representation(self, obj):
        """
        This function serializes the courses.
        """

        value = super(CourseSerializer, self).to_representation(obj)

        all_modules = obj.module_set.all()
        modules = ModuleSerializer(all_modules, many=True, read_only=True, context=self.context).data

        value['modules'] = modules

        num_questions = 0
        num_answered = 0
        for module in modules:
            for question in module['questions']:
                if question['solved']: num_answered += 1
                num_questions += 1
        value['num_answered'] = num_answered
        value['num_questions'] = num_questions
        return value

    def create(self, validated_data):
        '''
        This method is used to save courses together with all modules and
        questions.
        '''
        modules = validated_data.pop('modules')
        category = validated_data.pop('category')
        category = CourseCategory.objects.get(name=category)
        validated_data['category'] = category
        course = Course(**validated_data)
        course.save()
        try:
            for module in modules:
                module_serializer = ModuleSerializer(data=module)
                if not module_serializer.is_valid():
                    raise ParseError(
                        detail="Error in module serialization", code=None)
                else:
                    module['course'] = course
                    module_serializer.create(module)
            return True
        except Exception as e:
            course.delete()
            raise ParseError(detail=e.detail, code=None)


class GroupSerializer(serializers.ModelSerializer):
    '''
    Model serializer for the Group model
    '''

    class Meta:
        model = LearningGroup
        fields = ('name', "id")


class UserSerializer(serializers.ModelSerializer):
    '''
    Model serializer for the User model
    '''

    groups = serializers.StringRelatedField(many=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'date_joined', 'groups', 'first_name', 'last_name')

    def validate(self, data):
        """
        validate given passwords
        """
        if self.context.request.method=="POST":
            if "oldpassword" in data:
                if not request.user.check_password(request.data["oldpassword"]):
                    raise serializers.ValidationError("incorrect password @key oldpassword")
            else:
                if "password" in data:
                    raise serializers.ValidationError("when changing password the old password must be given with the key oldpassword")
        return data

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        validated_data.pop('groups')
        # TODO add language to profile
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
        #instance.username = validated_data["username"]
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
    '''
    Model serializer for the Try model
    '''
    user = serializers.StringRelatedField()
    question = serializers.StringRelatedField()

    class Meta:
        model = Try
        fields = ('user', 'question', 'date', 'solved')


class StatisticsOverviewSerializer(serializers.BaseSerializer):
    '''
    Longer serializer for the statistics overview
    '''

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
