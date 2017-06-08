from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User

from .serializers import *
from .models import Try, Profile

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes

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
def getUserDetails(request, userID):
    profils = Profile.objects.filter(id=userID).first()
    serializer = ProfileSerializer(profils).data
    return Response(serializer)

@api_view(['GET'])
def getUserInfo(request):
    value = []
    for group in request.user.get_all_permissions():
        if "learning_base" in group:
            value.append(group)
    return Response(value)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def createNewUser(request):


    # User serialization out of json request data
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user_serializer.save()
        return Response(status=status.HTTP_200_OK)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # profile serialization out of json request data
    profile_serializer = ProfileSerializer(data=request.data)
    if profile_serializer.is_valid():
        profile_serializer.save()
        return Response(status=status.HTTP_200_OK)
    return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #TODO: refactor name and surname to first and last name
    # add optional info
    #if("name" in data):
        #newUser.first_name = data["name"]

    #if("surname" in data):
        #newUser.last_name = data["surname"]

    return Response("Register did work")


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



