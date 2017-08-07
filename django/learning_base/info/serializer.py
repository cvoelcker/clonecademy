from rest_framework import serializers
from rest_framework.exceptions import ParseError
from .models import *

class InformationTextSerializer(serializers.ModelSerializer):
    """
    The serializer for information text type questions.
    """
    
    class Meta():
        model = InformationText
        fields = ()
