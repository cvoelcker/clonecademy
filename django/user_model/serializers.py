from rest_framework import serializers
from .models import *

class TriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Try
        fields = ('person', 'question', 'date', 'tries', 'solved')
