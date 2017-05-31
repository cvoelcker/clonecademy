from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User

from .serializers import StatisticsViewSerializer
from .models import Try

from rest_framework.decorators import api_view

from rest_framework.response import Response

# Create your views here.

class TriesViewSet(viewsets.ReadOnlyModelViewSet):
    """

    """
    queryset = Try.objects.all()
    serializer_class = StatisticsViewSerializer

    def get_queryset(self):
        _user = self.request.user
        user = _user.profile
        return self.queryset.filter(person=user)

@api_view(['GET'])
def getUserInfo(request):
    value = []
    for group in request.user.get_all_permissions():
        if "learning_base" in group:
            value.append(group)
    return Response(value)
