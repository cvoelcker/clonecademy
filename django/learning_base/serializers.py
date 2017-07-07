from rest_framework import serializers
from .models import *
from ast import literal_eval
from learning_base.multiple_choice.models import *
from learning_base.drag_and_drop.models import *
from learning_base.multiple_choice.serializer import *
from learning_base.drag_and_drop.serializer import *

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('title', 'body', 'feedback',)

    def to_representation(self, obj):
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


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ('name', "id",)


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('name', 'learning_text')

    def to_representation(self, obj):
        """
        This function makes the serialization and is needed for the custom order of the question
        """
        value = dict()
        value['name'] = obj.name
        value["id"] = obj.id
        value['learning_text'] = obj.learning_text

        questions = Question.objects.filter(module=obj)
        questions = QuestionPreviewSerializer(questions, many=True, read_only=True).data

        value["questions"] = questions
        return value


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'difficulty', 'id')

    #TODO: Can this be refactored and the ordering be done in the frontend?
    #      The serializer is needlessly complicated
    #      The ordering field in Module Meta should do this
    def to_representation(self, obj):
        """
        This function makes the serialization and is needed for the custom order of the modules
        """
        value = {}
        value['name'] = obj.name
        value['difficulty'] = obj.difficulty
        value["id"] = obj.id

        all_modules = Module.objects.filter(course=obj)
        modules = ModuleSerializer(all_modules, many=True, read_only=True).data

        value["modules"] = modules
        return value


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


class ModRequestSerializer(serializers.ModelSerializer):
    class Meta():
        model = ModRequest
        fields = ('user', 'date')

    def create(self, validated_data):
        print(validated_data)
        user = validated_data.pop('user')
        print("Still alive")
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
