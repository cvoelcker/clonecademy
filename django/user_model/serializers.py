from rest_framework import serializers

from .models import *
from learning_base.models import Question
from learning_base.serializers import QuestionSerializer


class GroupSerializer(serializers.ModelSerializer):
    '''
    Model serializer for the Group model
    '''
    class Meta:
        model = LearningGroup
        fields = ('name', "id" )


class UserSerializer(serializers.ModelSerializer):
    '''
    Model serializer for the User model
    '''
    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'date_joined')

    def create(self, validated_data):
        print("\n\n\n\n\n{}\n\n\n\n\n\n\n\n\n".format(validated_data))
        return Profile.objects.create_both(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            age=validated_data["age"],
            group=validated_data["group"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )


class ProfileSerializer(serializers.ModelSerializer):
    '''
    Model serializer for the Profile model
    '''
    user = UserSerializer()
    group = GroupSerializer(required=False)

    class Meta:
        model = Profile
        fields = ('user', 'group', 'first_name', 'last_name', 'age', 'requested_mod')


# TODO: Kill this shit, it is not relevant anymore, it provides the same
#       functions as above
class ProfileListSerializer(serializers.ModelSerializer):
    '''
    Model serializer for the Profile model
    '''
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ('user',)


class TrySerializer(serializers.ModelSerializer):
    '''
    Model serializer for the Try model
    '''
    person = ProfileSerializer()
    question = QuestionSerializer()

    class Meta:
        model = Try
        fields = ('person', 'question', 'date', 'solved')


class StatisticsOverviewSerializer(serializers.BaseSerializer):
    '''
    Longer serializer for the statistics overview
    '''
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

# For reference:
#
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
