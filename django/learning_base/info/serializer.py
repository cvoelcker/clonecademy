from rest_framework import serializers
from .models import *


class InformationTextSerializer(serializers.ModelSerializer):
    """
    The serializer for information text type questions.
    """

    class Meta():
        model = InformationText
        fields = ('text_field',)
