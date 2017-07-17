from rest_framework import serializers
from rest_framework.exceptions import ParseError
from .models import *


class MultipleChoiceAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceAnswer
        fields = ('text', 'id')

    def create(self, validated_data):
        answer = MultipleChoiceAnswer(**validated_data)
        answer.question = validated_data['question']
        answer.save()


class MultipleChoiceQuestionPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceQuestion
        fields = ('body', "id",)


class MultipleChoiceQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceQuestion
        fields = ('id',)

    def to_representation(self, obj):
        values = super(MultipleChoiceQuestionSerializer, self).to_representation(obj)
        answers = obj.answer_set()
        values['answers'] = MultipleChoiceAnswerSerializer(answers, many=True).data
        return values

    def create(self, validated_data):
        answers = validated_data.pop('answers')
        question = MultipleChoiceQuestion(**validated_data)
        question.module = validated_data['module']
        question.save()
        for answer in answers:
            answer['question'] = question
            answer_serializer = MultipleChoiceAnswerSerializer(data=answer)
            if not answer_serializer.is_valid():
                raise ParseError(detail="Error in answer serialization", code=None)
            else:
                answer_serializer.create(answer)
        if question.not_solvable():
            question.delete()
            raise ParseError(detail="Unsolvable question {}".format(question.title), code=None)
        else:
            return True
