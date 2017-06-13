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

from user_model.models import Try


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
        return Response(status=400)

    # every course needs a title, the modules and a categorie
    # here we check that thes variables are set
    if "title" not in data or 'modules' not in data or 'categorie' not in data:
        return Response(status=400)

    courseTitle = data['title']
    modules = data['modules']

    cat = CourseCategory.objects.filter(id=data['categorie']).first()

    course = Course(name = courseTitle,  is_visible = True)
    course.save()

    course.category.add(cat)

    # we prepare the array to save the order
    moduleOrder = [-1] * len(modules)

    # first we extract the modules and save it
    for m in modules:
        # every modules needs at least a title, question and a order in which it appears in the course
        # if these variables are not give delete the coures from the database
        if 'title' not in m or 'question' not in m or 'order' not in m:
            course.wipe_out()
            return Response(status=401)
        module = Module(name = m['title'], learning_text = m['learningText'])
        module.save()
        order = [-1] * len(m['question'])

        #every module gets his questions here
        for q in m['question']:
            # every question needs at least a question text a type and order
            # if these variables are not given delete the course with all its modules
            if 'type' not in q or 'question' not in q or 'order' not in q:
                course.wipe_out()
                return Response(status=402)

            # TODO it qould be nice to create the question component with
            # question_body and feedback and pass it to the child object
            quest = Question()
            # check which question Type it is and save it
            if q['type'] == "MultiplyChoiceQuestion":
                quest = MultipleChoiceQuestion(question_body = q['question'])
                if 'feedbackBool' in q and q['feedbackBool'] and 'feedback' in q:
                    quest.feedback = q['feedback']
                    quest.feedback_is_set = q['feedbackBool']
                if not quest.save(q):
                    course.wipe_out()
                    return Response(status=403)

            # add the created question to our module
            module.questions.add(quest)

            order[q['order']] = quest.id

        module.question_order = str(order)
        module.save()
        moduleOrder[m['order']] = module.id

        course.module.add(module)

    course.module_order = str(moduleOrder)

    course.save()
    return Response(True)


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
        solved = question.evaluate(request.data)
        Try(person=request.user.profile, question=question, answer=str(request.data), solved=solved).save()
        response = {"evaluate": solved}
        if solved and question.feedback_is_set:
            response['feedback'] = question.feedback
        return Response(response)
