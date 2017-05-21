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

class CoursePreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'course_difficulty')

class ModulePreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('name', )

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('name', 'order', 'question_body')

class QuestionPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('name', 'id')

# TODO: Represent inheritance over models in the serializer
class MultipleChoiceQuestionSerializer(QuestionSerializer):
    class Meta:
        model = MultipleChoiceQuestion
        fields = ('name', 'question_body')

class MultipleChoiceAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceAnswer
        fields = ('text', )
