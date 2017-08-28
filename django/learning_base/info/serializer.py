from rest_framework import serializers
from .models import *


class InformationTextSerializer(serializers.ModelSerializer):
    """
    The serializer for information text type questions.
    """

    class Meta:
        model = InformationText
        fields = ('text_field', 'image')

    def create(self, validated_data):
        question = InformationText(**validated_data)
        question.module = validated_data['module']
        question.save()
        return True


class InformationYoutubeSerializer(serializers.ModelSerializer):
    """
    The serializer for information text type questions.
    """

    class Meta:
        model = InformationYoutube
        fields = ('text_field', 'url')

    def create(self, validated_data):
        question = InformationYoutube(**validated_data)
        question.module = validated_data['module']
        question.save()
        return True
