from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from ast import literal_eval

from learning_base.serializers import *
from learning_base.question.serializer import *
from learning_base.question.models import Question
from learning_base.question.multiply_choice.models import MultipleChoiceQuestion
from learning_base.models import Course, CourseCategory
from rest_framework.response import Response

# Create your views here.

@api_view(['GET'])
def getCourses(request):
    courses = Course.objects.all().filter(is_visible=True)
    if len(courses) <= 0:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return Response(CourseSerializer(courses, many=True).data)

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

@api_view(['GET'])
def getCourseCategories(reqeust):
    categories = CourseCategory.objects.all()
    return Response(CourseCategorySerializer(categories, many=True).data)

@api_view(['POST'])
def save(request):
    data = request.data
    if data == None:
        return Response(status="invalid data")

    courseTitle = data['title']
    modules = data['modules']

    cat = None
    if data['categorie'] != None:
        cat = CourseCategory.objects.filter(id=data['categorie']).first()
    else:
        return Response(status="invalid data")

    course = Course(name = courseTitle,  is_visible = True)
    course.save()

    course.category.add(cat)

    moduleOrder = [-1] * len(modules)
    test = ""
    # first we extract the modules and save it
    for m in modules:
        module = Module(name = m['title'])
        module.save()
        order = [-1] * len(m['question'])

        #every module gets his questions here
        for q in m['question']:
            quest = Question()
            # check which question Type it is and save it
            if q['type'] == "MultiplyChoiceQuestion":
                quest = MultipleChoiceQuestion(question_body = q['question'])
                quest.save(q)

            # add the created question to our module
            module.questions.add(quest)
            test = quest.id
            order[q['order']] = quest.id

        module.question_order = str(order)
        module.save()
        moduleOrder[m['order']] = module.id

        course.module.add(module)

    course.module_order = str(moduleOrder)

    course.save()
    return Response(course.id)


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
