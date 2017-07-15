from rest_framework import serializers
from rest_framework.exceptions import ParseError
from .models import *
from learning_base.multiple_choice.models import *
from learning_base.drag_and_drop.models import *
from learning_base.multiple_choice.serializer import *
from learning_base.drag_and_drop.serializer import *

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
        value['last'] = obj.last_question()
        value['module'] = module.__str__()
        value['last_module'] = module.last_module()
        value['learning_text'] = module.learning_text
        value['course'] = module.course.__str__()
        if isinstance(obj, DragAndDropQuestion):
            value['question_body'] = DragAndDropQuestionSerializer(obj).data
        return value

    def create(validated_data):
        question_type = validated_data.pop['type']
        module_id = validated_data.pop['module_id']
        module = Module.objects.filter(id=module_id)

        if question_type == 'multiple_choice':
            pass
        if question_type == 'drag_and_drop':
            pass
        else:
            raise ParseError(detail='{} is not a valid question type'.format(question_type))


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ('name', "id",)


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('name', 'learning_text')

    def create(self, validated_data):
        print("still_alive")
        print(validated_data)

    def to_representation(self, obj):
        """
        This function makes the serialization and is needed for the custom order of the question
        """
        value = dict()
        value['name'] = obj.name
        value["id"] = obj.id
        value['learning_text'] = obj.learning_text

        questions = Question.objects.filter(module=obj)
        questions = QuestionSerializer(questions, many=True, read_only=True).data

        value["questions"] = questions
        return value

    def create(self, validated_data):
        '''
        This method is used to save modules and their respective questions
        '''
        questions = validated_data.pop('questions')
        course_id = validated_data.pop('course_id')
        course = Course.objects.filter(id=course_id)
        module = Module(**validated_data)
        module.course = course
        module.save()
        question_serializer = QuestionSerializer(data=modules)
        if not question_serializer.is_valid():
            raise ParseError(detail="Error in question serialization", code=None)
        else:
            question_serializer.save()


class CourseSerializer(serializers.ModelSerializer):
    module = ModuleSerializer()
    class Meta:
        model = Course
        fields = ('name', 'difficulty', 'id')

    def to_representation(self, obj):
        """
        This function serializes the courses.
        """
        value = {}
        value['name'] = obj.name
        value['difficulty'] = obj.difficulty
        value["id"] = obj.id

        all_modules = Module.objects.filter(course=obj)
        modules = ModuleSerializer(all_modules, many=True, read_only=True).data

        value["modules"] = modules
        return value

    def create(self, validated_data):
        '''
        This method is used to save courses together with all modules and questions
        '''
        modules = validated_data.pop('modules')
        course = Course(**validated_data)
        course.save()
        modules['course_id'] = course.id
        module_serializer = ModuleSerializer(data=modules)
        if not module_serializer.is_valid():
            raise ParseError(detail="Error in module serialization", code=None)
        else:
            module_serializer.save()


class GroupSerializer(serializers.ModelSerializer):
    '''
    Model serializer for the Group model
    '''
    class Meta:
        model = LearningGroup
        fields = ('name', "id" )


class UserSerializer(serializers.ModelSerializer):
    '''
    Model serializer for the User model
    '''
    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'date_joined')
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User(**validated_data)
        user.save()
        profile = Profile(user=user, **profile_data)
        profile.save()
        return True

class ModRequestSerializer(serializers.ModelSerializer):
    class Meta():
        model = ModRequest
        fields = ('user', 'date')

    def create(self, validated_data):
        user = validated_data.pop('user')
        user = User.objects.filter(id=user).first()
        new_request = ModRequest(user=user, date=timezone.localdate())
        new_request.save()
        return True


class TrySerializer(serializers.ModelSerializer):
    '''
    Model serializer for the Try model
    '''
    person = UserSerializer()
    question = QuestionSerializer()

    class Meta:
        model = Try
        fields = ('person', 'question', 'date', 'solved')


class StatisticsOverviewSerializer(serializers.BaseSerializer):
    '''
    Longer serializer for the statistics overview
    '''
    def to_representation(self, user):
        all_questions = list()
        for question in Question.objects.all():
            question_string = str(question)
            question_entry = dict()
            try_set = Try.objects.filter(question=question, person=user)
            for _try in try_set:
                if not question_entry:
                    question_entry = {
                        'question': question_string,
                        'solved': _try.solved,
                        'tries': 1
                    }
                else:
                    question_entry['tries'] += 1
                    question_entry['solved'] = question_entry['solved'] or _try.solved
            if question_entry:
                all_questions.append(question_entry)
        return all_questions
