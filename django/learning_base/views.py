from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import authentication, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from learning_base.serializers import CourseSerializer
from learning_base.models import Course

# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    """

    """
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
