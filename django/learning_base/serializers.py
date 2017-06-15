from rest_framework import serializers
from .models import *
from ast import literal_eval
from learning_base.multiply_choice.models import *
from learning_base.multiply_choice.serializer import *

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', )

    def to_representation(self, obj):
        if isinstance(obj, MultipleChoiceQuestion):
            value = MultipleChoiceQuestionSerializer(obj, context = self.context).to_representation(obj)
        # to serialize add new serializ classes for module types here
        else:
            return super(QuestionSerializer, self).to_representation(obj)

        value['class'] = obj.__class__.__name__
        return value

class QuestionPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', )

    def to_representation(self, obj):
        if isinstance(obj, MultipleChoiceQuestion):
            value = MultipleChoiceQuestionPreviewSerializer(obj, context = self.context).to_representation(obj)
        # to serialize add new serializ classes for module types here
        else:
            return super(QuestionPreviewSerializer, self).to_representation(obj)

        value['class'] = obj.__class__.__name__
        return value


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ('name', "id",)


class ModuleSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ('name', 'learning_text', 'questions', "question_order",)

    #TODO: Can this be refactored and the ordering be done in the frontend?
    #      The serializer is needlessly complicated
    #      The ordering field in Question Meta should do this
    def to_representation(self, obj):
        """
        This function makes the serialization and is needed for the custom order of the question
        """
        value = dict()
        value['name'] = obj.name
        value['max_module'] = len(obj.questions.all())
        value["id"] = obj.id
        value['learning_text'] = obj.learning_text

        ordering = literal_eval(obj.question_order)
        questions = QuestionPreviewSerializer(obj.questions, many=True, read_only=True).data

        return_questions = []
        for i in ordering:
            for question in questions:
                if i == question['id']:
                    return_questions.append(question)

        value["question"] = return_questions
        return value


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'course_difficulty', 'id')

    #TODO: Can this be refactored and the ordering be done in the frontend?
    #      The serializer is needlessly complicated
    #      The ordering field in Module Meta should do this
    def to_representation(self, obj):
        """
        This function makes the serialization and is needed for the custom order of the modules
        """
        value = {}
        value['name'] = obj.name
        value['course_difficulty'] = obj.course_difficulty
        value["id"] = obj.id

        modules = ModuleSerializer(obj.module, many=True, read_only=True).data

        return_modules = []
        for i in ordering:
            for m in modules:
                if i == m['id']:
                    return_modules.append(m)

        value["modules"] = return_modules
        return value
