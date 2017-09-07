from django.http import HttpResponse

from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, PermissionDenied
from rest_framework.response import Response

from . import serializers as serializer
from learning_base import custom_permissions
from .models import Course, CourseCategory, Try, CourseManager, Profile

from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from django.utils import timezone


class CategoryView(APIView):
    """
    Shows a category
    @author Claas Voelcker
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        Shows the categories
        """
        categories = CourseCategory.objects.all()
        data = serializer.CourseCategorySerializer(categories, many=True).data
        return Response(data,
                        status=status.HTTP_200_OK)

    def post(self, request, format=None):
        return Response({"ans": 'Method not allowed'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class MultiCourseView(APIView):
    """
    View to see all courses of a language. The post method provides a general
    interface with three filter settings.
    @author Claas Voelcker
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        Not implemented
        """
        return Response({"ans": 'Method not allowed'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format=None):
        """
        Returns a set of courses detailed by the query. It expects a request
        with the keys 'language', 'category', 'type'. The returning JSON
        corresponds to the values. All values can be empty strings, resulting
        in all courses being returned.
        """
        try:
            TYPES = ['mod', 'started']
            CATEGORIES = map(lambda x: str(x), CourseCategory.objects.all())
            LANGUAGES = map(lambda x: x[0], Course.LANGUAGES)
            data = request.data
            r_type = data['type']
            r_category = data['category']
            r_lan = data['language']

            # checks whether the query only contains acceptable keys
            if not ((r_type in TYPES or not r_type) and
                        (r_category in CATEGORIES or not r_category) and
                        (r_lan in LANGUAGES or not r_lan)):
                return Response({"ans": "Query not possible"},
                                status=status.HTTP_400_BAD_REQUEST)

            courses = Course.objects.all()
            courses = courses.filter(language=r_lan)
            if r_category != "":
                category = CourseCategory.objects.filter(
                    name=r_category).first()
                courses = courses.filter(category=category)
            if r_type == "mod":
                courses = courses.filter(responsible_mod=request.user)
            elif r_type == "started":
                courses = CourseManager.is_started(request.user)
            data = serializer.CourseSerializer(courses, many=True, context={
                'request': request}).data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"ans": "Query not possible" + str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class CourseEditView(APIView):
    """
    contains all the code related to edit a courses
    TODO: this is probably redundant code
    @author Leonhard Wiedmann
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (custom_permissions.IsModOrAdmin,)

    def get(self, request, course_id=None, format=None):
        """
        Returns all the information about a course with the answers and the
        solutions
        """
        if not course_id:
            return Response({"ans": 'Method not allowed'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

        try:
            course = Course.objects.filter(id=course_id).first()
            course_serializer = serializer.CourseEditSerializer(
                course,
                context={
                    'request': request})
            data = course_serializer.data
            return Response(data)

        except Exception as e:
            # TODO: Try if the conformate "ans" instead of "error"
            # works as good as this
            return Response({'error': str(e)},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request, course_id=None, format=None):
        return Response("test")


class CourseView(APIView):
    """
    Contains all code related to viewing and saving courses.
    @author Claas Voelcker
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (
        custom_permissions.IsModOrAdminOrReadOnly,)

    def get(self, request, course_id=None, format=None):
        """
        Returns a course if the course_id exists. The course, it's
        modules and questions are serialized.
        """
        if not course_id:
            return Response({"ans": 'Method not allowed'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            course = Course.objects.filter(id=course_id).first()
            course_serializer = serializer.CourseSerializer(course, context={
                'request': request})
            return Response(course_serializer.data,
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"ans": 'Course not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request, course_id=None, format=None):
        """
        Saves a course to the database. If the course id is provided,
        the method updates and existing course, otherwise, a new course
        is created.
        """
        data = request.data
        if data is None:
            return Response({"error": "Request does not contain data"},
                            status=status.HTTP_404_BAD_REQUEST)

        id = data.get('id')
        # This branch saves new courses or edites existing courses
        if (id is None) and Course.objects.filter(name=data['name']).exists():
            return Response({"ans": 'Course with that name exists'},
                            status=status.HTTP_409_CONFLICT)
        if id is None:
            data['responsible_mod'] = request.user
        else:
            responsible_mod = Course.objects.get(id=id).responsible_mod
            # decline access if user is wether admin nor responsible_mod
            if (request.user.profile.is_admin()
                or request.user == responsible_mod):
                data['responsible_mod'] = Course.objects.get(
                    id=id).responsible_mod
            else:
                raise PermissionDenied(detail="You're not allowed to edit this"
                                              + "course, since you're not the"
                                              + "responsible mod",
                                       code=None)

        course_serializer = serializer.CourseSerializer(data=data)
        if not course_serializer.is_valid():
            return Response({"error": course_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                course_serializer.create(data)
                return Response({"success": "Course saved"},
                                status=status.HTTP_201_CREATED)
            except ParseError as e:
                return Response({"error": str(e)},
                                status=status.HTTP_400_BAD_REQUEST)


class ModuleView(APIView):
    """
    Shows a module
    @author Claas Voelcker
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, course_id, module_id, format=None):
        """
        Shows the module
        """
        return Response({"ans": 'Method not allowed'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format=None):
        return Response({"ans": 'Method not allowed'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class QuestionView(APIView):
    """
    View to show questions and to evaluate them. This does not return the
    answers, which are given by a separate class.
    @author Claas Voelcker
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def can_access_question(self, user, question, module_id, question_id):
        module = question.module
        first_question = int(module_id) <= 0 and int(question_id) <= 0
        if first_question:
            return True
        elif (not first_question
              and question.get_previous_in_order()
              and Try.objects.filter(
                user=user,
                question=question.get_previous_in_order(),
                solved=True)):
            return True
        elif (not module.is_first_module()
              and module.get_previous_in_order()
              and Try.objects.filter(
                user=user,
                question=module.get_previous_in_order().question_set.all()[0],
                solved=True)):
            return True
        else:
            return False

    def get(self, request, course_id, module_id, question_id, format=None):
        """
        Get a question together with additional information about the module
        and position (last_module and last_question keys)
        """
        try:
            course = Course.objects.get(id=course_id)
            module = course.module_set.all()[int(module_id)]
            question = module.question_set.all()[int(question_id)]

            if question is None:
                return Response({"ans": "Question not found"},
                                status=status.HTTP_404_NOT_FOUND)
            if not self.can_access_question(request.user, question, module_id,
                                            question_id):
                return Response({"ans": "Previous question(s) haven't been "
                                        "answered correctly yet"},
                                status=status.HTTP_403_FORBIDDEN)
            data = serializer.QuestionSerializer(question,
                                                 context={'request': request})
            data = data.data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request, course_id, module_id, question_id, format=None):
        """
        Evaluates the answer to a question.
        @author Tobias Huber
        """
        try:
            course = Course.objects.get(id=course_id)
            module = course.module_set.all()[int(module_id)]
            question = module.question_set.all()[int(question_id)]
        except Exception as e:
            return Response({"ans": "Question not found"},
                            status=status.HTTP_404_NOT_FOUND)
        # deny access if there is a/are previous question(s) and it/they
        # haven't been answered correctly
        if not (self.can_access_question(request.user, question, module_id,
                                         question_id)):
            return Response({"ans":
                                 "Previous question(s) haven't been answered"
                                 " correctly yet"},
                            status=status.HTTP_403_FORBIDDEN)
        solved = question.evaluate(request.data["answers"])

        # only saves the points if the question hasn't been answered yet
        if solved and not question.try_set.filter(
                user=request.user, solved=True).exists():
            request.user.profile.ranking += question.get_points()
            request.user.profile.save()
        Try(user=request.user, question=question,
            answer=str(request.data["answers"]), solved=solved).save()
        response = {"evaluate": solved}
        if solved:
            nextType = ""
            if not question.is_last_question():
                nextType = "question"
            elif not module.is_last_module():
                nextType = "module"
            elif course.quizquestion_set.exists():
                nextType = "quiz"
            response['next'] = nextType
            if solved and question.feedback:
                response['custom_feedback'] = question.custom_feedback()
                response['feedback'] = question.feedback
        return Response(response)


class AnswerView(APIView):
    """
    Shows all possible answers to a question.
    @author Claas Voelcker
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, course_id, module_id, question_id, format=None):
        """
        Lists the answers for a question
        """
        course = Course.objects.get(id=course_id)
        module = course.module_set.all()[int(module_id)]
        question = module.question_set.all()[int(question_id)]
        answers = question.answer_set()
        data = serializer.AnswerSerializer(answers, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        return Response({"ans": 'Method not allowed'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class QuizView(APIView):
    """
    Shows the quiz question of the current course in get
    evaluates this quiz question in post
    @author Leonhard Wiedmann
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, course_id, quiz_id):
        """
        Shows the current quiz question if it exists.
        When this id does not exist throws error message
        """
        course = Course.objects.filter(id=course_id).first()

        # check if user did last question of the last module
        # if valid the course is completed
        module = course.module_set.all()[len(course.module_set.all()) - 1]
        question = module.question_set.all(
        )[len(module.question_set.all()) - 1]
        if not Try.objects.filter(question=question, solved=True).exists():
            return Response({"error": "complete the course first"},
                            status=status.HTTP_403_FORBIDDEN)

        if len(course.quizquestion_set.all()) > int(quiz_id):
            quiz = serializer.QuizSerializer(
                course.quizquestion_set.all()[int(quiz_id)])

            return Response(quiz.data)
        else:
            return Response({"error": "this quiz question does not exist"},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request, course_id, quiz_id, format=None):
        """
        Resolves this quiz question for the current user.
        """
        course = Course.objects.filter(id=course_id).first()
        if len(course.quizquestion_set.all()) > int(quiz_id):
            quiz = course.quizquestion_set.all()[int(quiz_id)]
            solved = quiz.evaluate(request.data)
            if solved and not quiz.try_set.filter(
                    user=request.user, solved=True).exists():
                request.user.profile.ranking += quiz.get_points()
                request.user.profile.save()
            Try(user=request.user, quiz_question=quiz,
                answer=str(request.data), solved=solved).save()
            return Response(
                {"last": len(
                    course.quizquestion_set.all()) == int(quiz_id) + 1}
            )
        else:
            return Response({"error": "this quiz question does not exist"},
                            status=status.HTTP_404_NOT_FOUND)


class UserView(APIView):
    """
    Shows a user profile
    @author Claas Voelcker
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user_id=False, format=None):
        """
        Shows the profile of any user if the requester is mod,
        or the profile of the requester

        TODO: If the behaviour that an admin is allowed to receive information
        about a specific user, will be used again,
        a custom_permission should be written.
        """
        user = request.user
        if user_id:
            if user.profile.is_admin():
                user = User.objects.filter(id=user_id).first()
                if not user:
                    return Response({"ans": 'User not found'},
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                raise PermissionDenied(detail=None, code=None)

        user = serializer.UserSerializer(user)
        return Response(user.data)

    def post(self, request, format=None):
        """
        Post is used to update the profile of the requesting user
        @author Tobias Huber
        """
        user = request.user
        data = request.data

        if "oldpassword" in data:
            if not request.user.check_password(request.data["oldpassword"]):
                return Response({"error": "given password is incorrect"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "password is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        user_serializer = serializer.UserSerializer(user, data=data,
                                                    partial=True)
        if user_serializer.is_valid():
            user_serializer = user_serializer.update(
                user,
                validated_data=request.data)
            return Response({"ans": 'Updated user ' + user.username},
                            status=status.HTTP_200_OK)
        else:
            return Response(user_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserRegisterView(APIView):
    """
    Shows a user profile
    @author Tobias Huber
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, user_id=False, format=None):
        """
        If the user_id field is specified, it updates user information.
        Otherwise it saves a new user.

        This behaviour isn't smart since this view doesn't require any
        authentication
        """
        if user_id:
            return Response({"ans": 'Please use the UserView to update data'},
                            status=status.HTTP_403_FORBIDDEN)
        else:
            user_serializer = serializer.UserSerializer(data=request.data)
            if user_serializer.is_valid():
                user_serializer.create(request.data)
                return Response({"ans": 'Created a new user'},
                                status=status.HTTP_201_CREATED)
            else:
                return Response(user_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)


class MultiUserView(APIView):
    """
    Shows an overview over all users
    @author Claas Voelcker
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (custom_permissions.IsAdmin,)

    def get(self, request):
        """
        Returns all users
        """
        users = User.objects.all()
        data = serializer.UserSerializer(users, many=True).data
        return Response(data)

    def post(self, request, format=None):
        """
        Not implemented
        """
        return Response({"ans": 'Method not allowed'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class StatisticsView(APIView):
    """
    A class displaying statistics information for a given user. It is used to
    access the try object.
    @author: Claas Voelcker
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user_id=None):
        user = request.user if not user_id else User.objects.get(id=user_id)
        tries = Try.objects.filter(user=user)
        data = serializer.TrySerializer(tries, many=True).data
        return Response(data)

    def post(self, request, format=None):
        import time
        import csv
        data = request.data
        user = request.user

        tries = Try.objects.all()

        groups = user.groups.values_list('name', flat=True)

        is_mod = 'moderator' in groups or 'admin' in groups

        # the simplest call is if the user just wants its statistic
        if 'id' in data and data['id'] == user.id:
            tries = tries.filter(user=user)

        # A moderator can get all statistics of his created courses
        # with 'get_courses' as in put the it will return all courses created
        # by this user
        elif is_mod and 'get_courses' in data:
            tries = tries.filter(
                question__module__course__responsible_mod=user)

        # admins can get all statistics of all users
        elif 'admin' in groups:
            if 'id' in data:
                tries.filter(user__id=data['id'])
        else:
            return Response({"error": "invalid userID"},
                            status=status.HTTP_401_UNAUTHORIZED)

        # return all statistics after prefiltering for this course
        if 'course' in data:
            tries = tries.filter(question__module__course__id=data['course'])

        # get the statistics for a specific time
        if ('date' in data
            and 'start' in data['date']
            and 'end' in data['date']):
            tries = tries.filter(
                date__range=[data['date']['start'], data['date']['end']])

        # filter just for solved tries
        if 'solved' in data:
            tries = tries.filter(solved=data['solved'])

        # filter for a specific category
        if 'category' in data:
            tries = tries.filter(
                question__module__course__category__name=data['category'])

        serializeData = serializer.TrySerializer(tries, many=True).data

        if 'format' in data and data['format'] == "csv":
            response = HttpResponse(content_type='text/csv')
            filename = time.strftime("%d/%m/%Y") + '-' + user.username + '.csv'
            content = 'attachment; filename="' + filename
            response['Content-Disposition'] = content
            writer = csv.writer(response)
            writer.writerow(['question', 'user', 'date', 'solved'])
            for row in serializeData:
                writer.writerow(
                    [row['question'], row['user'], row['date'], row['solved']])
            return response
        else:
            return Response(serializeData)


class RankingView(APIView):
    """
    A view for the ranking. The get method returns an ordered list of all users
    according to their rank.
    """
    #authentication_classes = (authentication.TokenAuthentication,)
    #permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        API request for ranking information
        :param request: can be empty
        :param format: request: can be empty
        :return: a json response with ranking information
        """
        profiles = Profile.objects.all().reverse()
        data = serializer.RankingSerializer(profiles).data
        return Response(data)

    def post(self, request, format=None):
        """
        Not implemented
        """
        return Response({"ans": 'Method not allowed'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class RequestView(APIView):
    # TODO: implement proper send_mail()
    """
    STILL IN DEVELOPMENT
    The RequestView class is used to submit a request for moderator rights.

    The request can be accessed via "clonecademy/user/request/"
    @author Tobias Huber
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        Returns True if request is allowed and False if request isn't allowed
        or the user is already mod.
        """
        allowed = (not request.user.profile.is_mod()
                   and request.user.profile.modrequest_allowed())
        return Response({'allowed': allowed},
                        status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Handels the moderator rights request. Expects a reason and extracts the
        user from the request header.
        """
        data = request.data
        user = request.user
        profile = user.profile
        if not user.profile.modrequest_allowed():
            return Response(
                {"ans": 'User is mod or has sent too many requests'},
                status=status.HTTP_403_FORBIDDEN)
        # TODO: fix if an localization issues arrise
        profile.last_modrequest = timezone.localdate()
        profile.save()
        send_mail(
            'Moderator rights requested by {}'.format(user.username),
            'The following user {} requested moderator rights for the \
CloneCademy platform. \n \
The given reason for this request: \n{}\n \
If you want to add this user to the moderator group, access the \
profile {} for the confirmation field.\n \
Have a nice day,\n your CloneCademy bot'.format(
                user.username, data["reason"],
                user.profile.get_link_to_profile()),
            'bot@clonecademy.de',
            [admin.email for
             admin in Group.objects.get(name="admin").user_set.all()]
        )
        return Response({"Request": "ok"}, status=status.HTTP_200_OK)


class UserRightsView(APIView):
    """
    Used to promote or demote a given user (by id)

    This View is used to grant or revoke specific rights (user|moderator|admin)
    The POST data must include the following fields
    {"right": "moderator"|"admin",
    "action": "promote"|"demote"}.
    Returns the request.data if validation failed.

    The user_id is to be provided in the url.

    TODO: try the generic.create APIView. Its behaviour isn't really different
    from the current. It just provides additional success-headers in a way
    I do not understand.
    """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (custom_permissions.IsAdmin,)

    def post(self, request, user_id, format=None):
        data = request.data
        right_choices = ['moderator', 'admin']
        action_choices = ['promote', 'demote']
        errors = {}

        # validation
        if not data["right"] or not (data["right"] in right_choices):
            errors["right"] = ("this field is required and must be one of "
                               + "the following options"
                               + ', '.join(right_choices))
        if not data["action"] or not (data["action"] in action_choices):
            errors["action"] = ("this field is required and must be one of "
                                + "the following options"
                                + ', '.join(action_choices))
        if not User.objects.filter(id=user_id).exists():
            errors["id"] = "a user with the id #" + user_id + " does not exist"
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        # actual behaviour
        user = User.objects.get(id=user_id)
        group = Group.objects.get(name=data["right"])
        action = data["action"]
        if (action == "promote"):
            user.groups.add(group)
        elif (action == "demote"):
            user.groups.remove(group)
        return Response(serializer.UserSerializer(user).data)

    def get(self, request, user_id, format=None):
        """
        This API is for debug only.
        It comes in quite handy with the browsable API
        """
        user = User.objects.get(id=user_id)
        return Response({"username": user.username,
                         "is_mod?":
                             user.groups.filter(name="moderator").exists(),
                         "is_admin?":
                             user.groups.filter(name="admin").exists()})
