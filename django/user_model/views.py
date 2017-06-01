from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User

from .serializers import StatisticsOverviewSerializer
from .models import Try

from rest_framework.decorators import api_view

from rest_framework.response import Response

# Create your views here.


@api_view(['GET'])
def getStatisticsOverview(request):
    _user = request.user.profile
    _queryset = Try.objects.filter(person=_user)
    _json = StatisticsOverviewSerializer(_queryset, many=True)
    return Response(_json.data)

@api_view(['GET'])
def getStatisticsDetail(request):
    pass


@api_view(['GET'])
def getUserInfo(request):
    value = []
    for group in request.user.get_all_permissions():
        if "learning_base" in group:
            value.append(group)
    return Response(value)
