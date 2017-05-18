from rest_framework import serializers
from .models import *

class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields('name')


class CourseSerializer(serializer.ModelSerializer):
    class Meta:
        model = Course
        fields('name', 'Course_difficulty', 'is_visible')


class Question(serializer.Serializer):
    class Meta:
        model = Question
        fields('name', 'order', 'question_body', 'course')


class MultipleChoiceQuestionSerializer(Question):
    class Meta:
        model = MultipleChoiceQuestion
        fields()
