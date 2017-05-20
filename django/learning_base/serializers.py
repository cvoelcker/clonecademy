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


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('name', 'order', 'question_body', 'course')


# TODO: Represent inheritance over models in the serializer
class MultipleChoiceQuestionSerializer(QuestionSerializer):
    class Meta:
        model = MultipleChoiceQuestion
        fields = fields = ('name', 'order', 'question_body')
