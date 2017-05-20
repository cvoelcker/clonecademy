from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import authentication, permissions

from learning_base.serializers import CourseSerializer
from learning_base.models import Course
from django.http import JsonResponse

# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = Course.objects.all().filter(is_visible=True)
    serializer_class = CourseSerializer


# class get(request):
#     dataTransform=json.loads(request.body.decode("utf-8"))
#     name = dataTransform['name']
#     return name #json.dumps(dataTransform)
