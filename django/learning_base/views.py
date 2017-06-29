from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from learning_base.serializers import *
from learning_base.multiple_choice.models import MultipleChoiceQuestion
from learning_base.models import Course, CourseCategory, Module, valid_mod_request, get_link_to_profile

from rest_framework.response import Response
from django.core.mail import send_mail

# Create your views here.

class CourseView():
    pass

class ModuleView():
    pass

class QuestionView():
    pass

class UserView():
    pass
    
class RequestView(APIView):
    """
    STILL IN DEVELOPMENT
    The RequestView class is used to submit a request for moderator rights.

    The request can be accessed via "clonecademy/user/request/"
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    '''
    example function
    '''
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)

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

    course = course.first()
    data = CourseSerializer(course).data
    solved = []

    for m in Module.objects.filter(course=course):
        for q in Question.objects.filter(module=m):
            if Try.objects.filter(question=q).filter(solved=True).exists():
                solved.append(q.id)
    data['solved'] = solved
    return Response(data)


def get_module_by_order(course, index):
    return Module.objects.filter(id=index, course=course).first()

@api_view(['GET'])
def callModule(request, courseID, moduleIndex):
    course = Course.objects.filter(id=courseID).first()
    index = int(moduleIndex)

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
    index = int(moduleIndex)

    module = get_module_by_order(course, index);

    if not module:
        return Response(status=status.HTTP_404_NOT_FOUND)

    index = int(questionIndex)

    if index < 0:
        return Response(status=status.HTTP_404_NOT_FOUND)
    question = Question.objects.filter(id=int(questionIndex)).first()

    if request.method == "GET":
        value = QuestionSerializer(question, read_only=True).data
        value['title'] = module.name
        # to see if the module is over
        value['lastQuestion'] = int(questionIndex) == module.num_of_questions()
        # to check if the course is over
        value['lastModule'] = int(moduleIndex) == course.num_of_modules()
        return Response(value)
    elif request.method == "POST":
        solved = question.evaluate(request.data)
        Try(person=request.user.profile, question=question, answer=str(request.data), solved=solved).save()
        response = {"evaluate": solved}
        if solved and question.feedback_is_set:
            response['feedback'] = question.feedback
        return Response(response)


@api_view(['GET'])
def getStatisticsOverview(request):
    '''
    Returns the statistics overview for a user
    '''
    json = StatisticsOverviewSerializer(request.user)
    return Response(json.data)


@api_view(['GET'])
def getUsers(request, get_list):
    '''
    Returns a list of alluser profile names
    '''
    user = User.objects.all()
    user = UserSerializer(user, many=get_list).data
    return Response(serializer)


@api_view(['GET'])
def getUserDetails(request, userID):
    '''
    Returns the user profile info
    '''
    user = User.objects.filter(id=userID).first()
    user = UserSerializer(user)
    return Response(user.data)


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
    '''
    This handels the request for a new user account. All data is validated, and if
    every consistency check passes, a new user and  new profile is created.
    '''
    # User serialization out of json request data
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.create(request.data)
        return Response(user)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
Mod Request API
"""

@api_view(['GET'])
def canRequestMod(request):
    user = request.user
    return Response(valid_mod_request(user))

@api_view(['POST'])
def requestModStatus(request):
    '''
    TODO: Should be GET method in ClassBasedView - remember problem with auth/perm!
    Handels the moderator rights request. Expects a reason and extracts the user
    from the request header.
    '''
    data = request.data
    user = request.user
    if valid_mod_request(user=user):
        return Response('User is mod or has sent to many requests',status=402)
    #TODO: fix if an localization issues arrise
    
    data['user'] = user.id
    data['date'] = str(timezone.localdate())

    new_request = ModRequestSerializer(data=data)
    
    if new_request.is_valid():
        new_request.create(new_request.data)
    else:
        print("\n\n\n\n\n\n\n{}\n{}\n\n\n\n\n\n\n".format(data, new_request.errors))
        return Response('Invalid request', status=500)

    send_mail(
        'Moderator rights requested by {}'.format(user.username),
        'The following user {} requested moderator rights for the CloneCademy platform. \n \
        The given reason for this request: \n{}\n \
        If you want to add this user to the moderator group, access the profile {}\
        for the confirmation field.\n \
     UserSerializer   Have a nice day, your CloneCademy bot'.format(
            user.username, data["reason"], get_link_to_profile(user)),
        'bot@clonecademy.de',
        ['test@test.net']
    )
    return Response({"Request": "ok"})  

def getCurrentUser(request):
    return getUserDetails(request, request.user.id)
