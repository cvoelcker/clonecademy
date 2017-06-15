from rest_framework import serializers
from .models import *

class MultipleChoiceAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceAnswer
        fields = ('text', 'id')


# It would be great to have a solution to not copy the serializer for preview
class MultipleChoiceQuestionPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceQuestion
        fields = ('question_body', "id", )


# TODO: Represent inheritance over models in the serializer
class MultipleChoiceQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceQuestion
        fields = ('question_body', 'answers', "id", )

    answers = MultipleChoiceAnswersSerializer(many = True, read_only=True)
