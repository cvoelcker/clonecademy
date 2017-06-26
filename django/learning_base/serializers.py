from rest_framework import serializers
from .models import *
from .question.serializer import *
from ast import literal_eval


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ('name', "id",)


class ModuleSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ('name', 'learning_text', 'questions', "question_order",)

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

    def to_representation(self, obj):
        """
        This function makes the serialization and is needed for the custom order of the modules
        """
        value = {}
        value['name'] = obj.name
        value['course_difficulty'] = obj.course_difficulty
        value["id"] = obj.id
        value['category'] = CourseCategorySerializer(obj.category, many=True).data

        ordering = literal_eval(obj.module_order)
        modules = ModuleSerializer(obj.module, many=True, read_only=True).data

        return_modules = []
        for i in ordering:
            for m in modules:
                if i == m['id']:
                    return_modules.append(m)

        value["modules"] = return_modules
        return value
