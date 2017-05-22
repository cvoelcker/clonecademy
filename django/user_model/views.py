from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User

from .serializers import TriesSerializer
from .models import Try

# Create your views here.

class TriesViewSet(viewsets.ReadOnlyModelViewSet):
    """

    """
    queryset = Try.objects.all()
    serializer_class = TriesSerializer

    def get_queryset(self):
        _user = self.request.user
        user = _user.profile
        return self.queryset.filter(person=user)
