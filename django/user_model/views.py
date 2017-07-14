from datetime import datetime

from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from django.core.mail import mail_admins, send_mail

from .serializers import *
from .models import Try, Profile, is_mod, is_admin

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
    profiles = Profile.objects.filter(id=userID).first()
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
        return Response(user)
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
    profile = request.user.profile
    return Response(ProfileSerializer(profile).data)

@api_view(['POST'])
#@permission_classes((IsAdminUser, )) for some reason the compiler couldn't find the permission class
def grantModStatus(request, userID):
    '''
    '''
    to_be_promoted = User.objects.get(id=userID)
    if is_mod(to_be_promoted):
    #    return Response("the user \" "+ to_be_promoted.username +"\" is already a moderator", status=status.HTTP_200_OK)
        return Response("the user \" "+ to_be_promoted.username +"\" is already a moderator", status=status.HTTP_304_NOT_MODIFIED)
    mod_group = Group.objects.get(name='moderator')
    to_be_promoted.groups.add(mod_group)
    if is_mod(to_be_promoted):
        return Response("successfully promoted " + to_be_promoted.username, status=status.HTTP_200_OK)
    return Response("something went terribly wrong with promoting" + to_be_promoted.username, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def grantModStatusByName(request):
    '''
    '''
    to_be_promoted = User.objects.get(username=request.data["username"])
    return grantModStatus(request, to_be_promoted.id)
