from rest_framework import serializers

from .models import *
from learning_base.question.models import Question
from learning_base.serializers import QuestionSerializer


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningGroup
        fields = ('name')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    group = GroupSerializer()

    class Meta:
        model = Profile
        fields = ('user', 'group', 'date_registered')


class StatisticsDetailedViewSerializer(serializers.ModelSerializer):
    person = ProfileSerializer()
    question = QuestionSerializer()

    class Meta:
        model = Try
        fields = ('person', 'question', 'date', 'solved')


class StatisticsOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Try
        fields = ('person', 'question', 'date', 'solved')

    person = ProfileSerializer()
    question = QuestionSerializer()
    date = serializers.DateTimeField()
    solved = serializers.BooleanField()

    def to_representation(self, user):
        _all_questions = dict()
        for _question in Question.objects.all():
            _try_set = Try.objects.filter(question=_question, person=user.profile)
            for _try in _try_set:
                if not _all_questions[_question]:
                    _all_questions[_question] = {
                        'question': _try.question,
                        'person': _try.person,
                        'solved': _try.solved,
                        'tries': 1
                    }
                else:
                    _all_questions[_question]['tries'] += 1
                    _all_questions[_question]['solved'] = _all_questions[_question]['solved'] or _try.solved
        return _all_questions

# class CommentSerializer(serializers.Serializer):
#    email = serializers.EmailField()
#    content = serializers.CharField(max_length=200)
#    created = serializers.DateTimeField()
#
#    def create(self, validated_data):
#        return Comment(**validated_data)
#
#    def update(self, instance, validated_data):
#        instance.email = validated_data.get('email', instance.email)
#        instance.content = validated_data.get('content', instance.content)
#        instance.created = validated_data.get('created', instance.created)
#        return instance
