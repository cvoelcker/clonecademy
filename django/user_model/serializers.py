from rest_framework import serializers

from .models import *

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
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
    person = serializers.StringRelatedField()
    question = serializers.StringRelatedField()
    class Meta:
        model = Try
        fields = ('person', 'question', 'date', 'solved')


class StatisticsViewSerializer(serializers.ModelSerializer):
    question = serializers.StringRelatedField()
    class Meta:
        model = Try
        fields = ('question', 'solved', 'tries')


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
