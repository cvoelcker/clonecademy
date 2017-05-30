from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from ast import literal_eval

from learning_base.serializers import *
from learning_base.question.serializer import *
from learning_base.question.models import Question
from learning_base.models import Course
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
def singleCourse(request, courseID):
    course = Course.objects.filter(id=courseID)
    if len(course) <= 0:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return Response(CourseSerializer(course[0]).data)


def get_module_by_order(course, index):
    # get the map of the ordered modules
    ordering_module = literal_eval(course.module_order)

    if index < 0 or index > len(ordering_module):
        return False

    #module = module.first()
    return course.module.filter(id=ordering_module[index]).first()

@api_view(['GET'])
def callModule(request, courseID, moduleIndex):
    course = Course.objects.filter(id=courseID).first()
    index = int(moduleIndex) - 1

    module = get_module_by_order(course, index);

    if module == False:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        value = ModuleSerializer(module).data
        return Response(value)



@api_view(['GET', "POST"])
def callQuestion(request, courseID, moduleIndex, questionIndex):
    course = Course.objects.filter(id=courseID).first()
    index = int(moduleIndex) - 1

    module = get_module_by_order(course, index);

    if module == False:
        return Response(status=status.HTTP_404_NOT_FOUND)

    index = int(questionIndex) - 1
    ordering = literal_eval(module.question_order)

    if index < 0 or index > len(ordering):
        return Response(status=status.HTTP_404_NOT_FOUND)
    question = Question.objects.filter(id=ordering[int(questionIndex) - 1])[0]

    if request.method == "GET":
        value = QuestionSerializer(question,  read_only=True).data
        value['title'] = module.name
        # to see if the module is over
        value['lastQuestion'] = int(questionIndex) == len(ordering)
        # to check if the course is over
        value['lastModule'] = int(moduleIndex) == len(course.module.all())
        return Response(value)
    elif request.method == "POST":
        return Response(question.evaluate(request.data))
