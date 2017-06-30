from datetime import datetime

from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.core.mail import mail_admins, send_mail

from .serializers import *
from .models import Try, Profile

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes

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
    user = User.objects.filter(id=userID).first()
    profiles = Profile.objects.filter(user=user).first()
    serializer = ProfileSerializer(profiles).data
    #serializer = map(lambda x: x['user'], serializer)
    return Response(serializer['user'])

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
        user = user_serializer.create(request.data)
        return Response(True)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def requestModStatus(request):
    '''
    Handels the moderator rights request. Expects a reason and extracts the user
    from the request header.

    This class does not use a serializer, as the json is only one element wide and.
    '''
    data = request.data
    user = request.user
    profile = user.profile
    if profile.is_mod or profile.requested_mod:
        return Response('User is mod or has sent to many requests',status=400)
    #TODO: fix if an localization issues arrise
    profile.requested_mod = datetime.now()
    profile.save()
    send_mail(
        'Moderator rights requested by {}'.format(user.username),
        'The following user {} requested moderator rights for the CloneCademy platform. \n \
        The given reason for this request: \n{}\n \
        If you want to add this user to the moderator group, access the profile {}\
        for the confirmation field.\n \
        Have a nice day, your CloneCademy bot'.format(
            user.username, data["reason"], profile.get_link_to_profile()),
        'bot@clonecademy.de',
        ['test@test.net']
    )
    return Response("Request send")

@api_view(['GET'])
def canRequestMod(request):
    profile = request.user.profile
    can_request = ProfileSerializer(profile)
    return Response(can_request.data)

@api_view(['GET'])
def getCurrentUser(request):
    return Response(UserGroups(request.user).data)
