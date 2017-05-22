from rest_framework import serializers
from .models import *

class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ('name')


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'course_difficulty', 'id')

class ModulePreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('name', "id")

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        module = Module
        fields = ('name', )

    def to_representation(self, obj):
        if isinstance(obj, MultipleChoiceQuestion):
            value = MultipleChoiceQuestionSerializer(obj, context = self.context).to_representation(obj)
        # to serialize add new serializ classes for module types here
        else:
            return super(ModuleSerializer, obj).to_representation(obj)

        value['class'] = obj.__class__.__name__
        return value

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('name', 'order', 'question_body',)

class QuestionPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('name', 'id')


class MultipleChoiceAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceAnswer
        fields = ('text', 'id')


# TODO: Represent inheritance over models in the serializer
class MultipleChoiceQuestionSerializer(QuestionSerializer):
    answers = MultipleChoiceAnswersSerializer(many = True, read_only=True)

    class Meta:
        model = MultipleChoiceQuestion
        fields = ('name', 'question_body', 'answers',)
