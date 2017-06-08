from rest_framework import serializers

from .models import *
from learning_base.question.models import Question
from learning_base.serializers import QuestionSerializer


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningGroup
        fields = ('name', "id" )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', "id")


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    group = GroupSerializer()

    def to_representation(self, obj):
        serializer = UserSerializer(obj.user).data
        serializer['group'] = GroupSerializer(obj.group).data
        serializer['date_registered'] = obj.date_registered
        return serializer

    class Meta:
        model = Profile
        fields = ('user', 'group', 'date_registered', 'first_name', 'last_name', 'age')

class ProfileListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ('user', )

class StatisticsDetailedViewSerializer(serializers.ModelSerializer):
    person = ProfileSerializer()
    question = QuestionSerializer()

    class Meta:
        model = Try
        fields = ('person', 'question', 'date', 'solved')


class StatisticsOverviewSerializer(serializers.BaseSerializer):

    def to_representation(self, user):
        all_questions = list()
        for question in Question.objects.all():
            question_string = str(question)
            question_entry = dict()
            try_set = Try.objects.filter(question=question, person=user.profile)
            for _try in try_set:
                if not question_entry:
                    question_entry = {
                        'question': question_string,
                        'solved': _try.solved,
                        'tries': 1
                    }
                else:
                    question_entry['tries'] += 1
                    question_entry['solved'] = question_entry['solved'] or _try.solved
            if question_entry:
                all_questions.append(question_entry)
        return all_questions

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
