from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view

from learning_base.serializers import *
from learning_base.models import Course
from learning_base.question.multiply_choice.models import *
from rest_framework.response import Response

# Create your views here.

@api_view(['GET'])
def getCourses(request):
    courses = Course.objects.all().filter(is_visible=True)
    if len(courses) <= 0:
        return Response(status=status.HTTP_404_NOT_FOUND)
    values = []
    for c in courses:
        values.append(CourseSerializer(c).data)
    return Response(values)

@api_view(['GET'])
def singleCourse(request, course):
    course = Course.objects.filter(id=course)
    if len(course) <= 0:
        return Response(status=status.HTTP_404_NOT_FOUND)
    values = {"course": CourseSerializer(course[0]).data, "module": []}

    questions = course[0].module.order_by("order")
    for q in questions:
        module = ModulePreviewSerializer(q).data
        module['class'] = q.__class__.__name__
        values['module'].append(module)
    return Response(values)

@api_view(['GET', 'POST'])
def callModule(request, module, course):
    module = Module.objects.filter(id=module)
    if len(module) <= 0:
        return Response(status=status.HTTP_404_NOT_FOUND)
    module = module.first()

    if request.method == "GET":
        return Response(ModuleSerializer(module).data)
    if request.method == "POST":
        return Response(module.evaluate(request.data))
