from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User

from .serializers import StatisticsOverviewSerializer, ProfileListSerializer
from .models import Try, Profile

from rest_framework.decorators import api_view
from rest_framework.response import Response

#For debug only!
from django.http import HttpResponse

# Create your views here.


@api_view(['GET'])
def getStatisticsOverview(request):
    json = StatisticsOverviewSerializer(request.user).data
    return Response(json)

@api_view(['GET'])
def getStatisticsDetail(request):
    pass

@api_view(['GET'])
def getAllUsers(request):
    profiles = Profile.objects.all()
    serializer = ProfileListSerializer(profiles, many=True).data
    #TODO it will return [{user: {username, id, email}}]
    # but it would be good to return [{username, id, email}]
    serializer = map(lambda x: x['user'], serializer)
    return Response(serializer)

@api_view(['GET'])
def getUserInfo(request):
    value = []
    for group in request.user.get_all_permissions():
        if "learning_base" in group:
            value.append(group)
    return Response(value)

@api_view(['POST'])
def createNewUser(request):
    data = request.data

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

@api_view(['POST'])
def requestModStatus(request):
    '''
    Handels the moderator rights request. Expects a username and a
    '''
    try:
        data = request.data
        user = User.objects.filter(username=data["username"])[0]
        user = user.profile
        if user.is_mod or user.requested_mod:
            return Response(status=400)
        user.requested_mod = True
        user.save()

        mail_admins(
            'Moderator rights requested by {}'.format(data["username"]),
            'The following user {} requested moderator rights for the CloneCademy platform. \n \
            The given reason for this request: \n{}\n \
            If you want to add this user to the moderator group, access the profile {}\
            for the confirmation field.\n \
            Have a nice day, your CloneCademy bot'.format(
                data["username"], data["reason"], user.get_link_to_profile()),
        )
    except:
        return Response(status=400)
