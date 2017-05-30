from rest_framework import serializers

from .models import *
from learning_base.question.serializers import QuestionPreviewSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class ProfileSerializer(serializer.ModelSerializer):
    user = UserSerializer()
    group = GroupSerializer()

    class Meta:
        model = Profile
        fields = ('user', 'group', 'date_registered')

class StatisticsDetailedViewSerializer(serializers.ModelSerializer):
    person = StringRelatedField()
    question = StringRelatedField()
    class Meta:
        model = Try
        fields = ('person', 'question', 'date', 'solved')

class StatisticsViewSerializer(serializers.Serializer):
    question = serializers.StringRelatedField()


#class CommentSerializer(serializers.Serializer):
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
