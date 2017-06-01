from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User

from .serializers import StatisticsViewSerializer
from .models import Try

from rest_framework.decorators import api_view
from rest_framework.response import Response

#For debug only!
from django.http import HttpResponse

# Create your views here.


@api_view(['GET'])
def getStatisticsOverview(request):
    _user = request.user.profile
    queryset = Try.objects.filter(person=_user)
    value = []
    for objects in queryset:

        _json = StatisticsViewSerializer(objects)
        value.append(_json.data)
    return Response(value)


@api_view(['GET'])
def getUserInfo(request):
    value = []
    for group in request.user.get_all_permissions():
        if "learning_base" in group:
            value.append(group)
    return Response(value)

@api_view(['POST'])
def createNewUser(request):
    data = request.data;

    if "username" not in data or "email" not in data or "password" not in data:
        return Response(status = 400)

    newUser = User.objects.create_user(data["username"], data["email"], data["password"]);

    #add optional info
    #TODO: refactor name and surname to first and last name
    #if("name" in data):
     #   newUser.first_name = data["name"]

    #if("surname" in data):
     #   newUser.last_name = data["surname"]

    #newUser.save();

    #return HttpResponse("Register did work")