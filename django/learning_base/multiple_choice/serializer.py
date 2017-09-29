"""
serializers for MultipleChoice question types
"""

from rest_framework import serializers
from rest_framework.exceptions import ParseError
from .models import MultipleChoiceAnswer, MultipleChoiceQuestion


class MultipleChoiceAnswerSerializer(serializers.ModelSerializer):
    """
    Serializer for MultipleChoice answers
    :author: Leonhard Wiedmann
    """
    class Meta:
        model = MultipleChoiceAnswer
        fields = ('text', 'id', 'img')

    def create(self, validated_data):
        """
        creation method for new db entries
        :author: Leonhard Wiedmann
        :param: validated_data valid data for the creation
        """
        answer = MultipleChoiceAnswer(**validated_data)
        answer.question = validated_data['question']
        answer.save()


class MultipleChoiceQuestionPreviewSerializer(serializers.ModelSerializer):
    """
    Serializer for MultipleChoice question preview
    :author: Leonhard Wiedmann
    """
    class Meta:
        model = MultipleChoiceQuestion
        fields = ('body', "id",)


class MultipleChoiceAnswerEditSerializer(serializers.ModelSerializer):
    """
    Serializer for MultipleChoice answer editing
    :author: Leonhard Wiedmann
    """
    class Meta:
        model = MultipleChoiceAnswer
        fields = ("text", "id", "is_correct", "img")


class MultipleChoiceQuestionEditSerializer(serializers.ModelSerializer):
    """
    Serializer for MultipleChoice question editing
    :author: Leon Wiedmann
    """
    class Meta:
        model = MultipleChoiceQuestion
        fields = ("id", 'question_image', 'feedback_image')

    def to_representation(self, obj):
        """
        responsible for json serialization of objects
        :author: Leonhard Wiedmann
        :param obj: the object that should be serialized
        :return: a json representation of the object
        """
        values = super(MultipleChoiceQuestionEditSerializer,
                       self).to_representation(obj)
        answers = obj.answer_set()
        values['answers'] = MultipleChoiceAnswerEditSerializer(answers,
                                                               many=True).data
        return values


class MultipleChoiceQuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for MultipleChoice questions editing
    :author: Leon Wiedmann
    """
    class Meta:
        model = MultipleChoiceQuestion
        fields = ('id', 'question_image')

    def to_representation(self, obj):
        """
        responsible for json serialization of objects
        :author: Leonhard Wiedmann
        :param obj: the object that should be serialized
        :return: a json representation of the object
        """
        values = super(MultipleChoiceQuestionSerializer,
                       self).to_representation(obj)
        answers = obj.answer_set()
        values['answers'] = MultipleChoiceAnswerSerializer(answers,
                                                           many=True).data
        return values

    def create(self, validated_data):
        """
        creating new database entries while editing
        :author: Leonhard Wiedmann
        :param validated_data: valid data
        """
        answers = validated_data.pop('answers')
        question = MultipleChoiceQuestion(**validated_data)
        question.module = validated_data['module']
        question.save()

        for answer in answers:
            answer['question'] = question
            answer_serializer = MultipleChoiceAnswerSerializer(data=answer)
            if not answer_serializer.is_valid():
                raise ParseError(detail=answer_serializer.errors, code=None)
            else:
                answer_serializer.create(answer)
        if question.not_solvable():
            question.delete()
            raise ParseError(
                detail="Unsolvable question {}".format(question.title),
                code=None)
