from rest_framework import serializers
from learning_base.question.serializer import QuestionSerializer
from .models import *

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
