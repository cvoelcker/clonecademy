from rest_framework import serializers
from django.contrib.auth.models import User

def user_by_id_exists(value):
    if not User.objects.get(id=value).exists():
        raise serializers.ValidationError('A user with the given id'+value+'does not exist')
