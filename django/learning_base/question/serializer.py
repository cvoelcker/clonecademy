from rest_framework import serializers
from learning_base.question.models import Question
from learning_base.question.multiply_choice.models import *
from learning_base.question.multiply_choice.serializer import *

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
