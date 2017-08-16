from django.http import HttpResponse

from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError


import learning_base.serializers as serializer
from learning_base.models import Course, CourseCategory, Try, Profile

from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group

from django.utils import timezone


class CategoryView(APIView):
    '''
    Shows a category
    @author Claas Voelcker
    '''
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        '''
        Shows the categories
        '''
        categories = CourseCategory.objects.all()
        data = serializer.CourseCategorySerializer(categories, many=True).data
        return Response(data,
                        status=status.HTTP_200_OK)

    def post(self, request, format=None):
        return Response('Method not allowed',
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class MultiCourseView(APIView):
    '''
    View to see all courses of a language. The post method provides a general
    interface with three filter settings.
    @author Claas Voelcker
    '''
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        '''
        Not implemented
        '''
        return Response('Method not allowed',
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format=None):
        '''
        Returns a set of courses detailed by the query. It expects a request
        with the keys 'language', 'category', 'type'. The returning JSON
        corresponds to the values. All values can be empty strings, resulting
        in all courses being returned.
        '''
        try:
            TYPES = ['mod', 'started']
            CATEGORIES = map(lambda x: str(x), CourseCategory.objects.all())
            LANGUAGES = map(lambda x: x[0], Course.LANGUAGES)
            data = request.data
            r_type = data['type']
            r_category = data['category']
            r_lan = data['language']

            # checks whether the query only contains acceptable keys
            if not ((r_type in TYPES or not r_type)
                    and (r_category in CATEGORIES or not r_category)
                    and (r_lan in LANGUAGES or not r_lan)):
                return Response("Query not possible",
                                status=status.HTTP_400_BAD_REQUEST)

            courses = Course.objects.all()
            courses = courses.filter(language=r_lan)
            if r_category != "":
                category = CourseCategory.objects.filter(
                    name=r_category).first()
                courses = courses.filter(category=category)
            if r_type == "mod":
                courses.filter(responsible_mod=request.user)
            elif r_type == "started":
                courses = courses.filter(module__question__try__person=user)
            data = serializer.CourseSerializer(courses, many=True, context={
                'request': request}).data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response("Query not possible",
                            status=status.HTTP_400_BAD_REQUEST)


class CourseEditView(APIView):
    '''
    contains all the code related to edit a courses
    @author Leonhard Wiedmann
    '''
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, course_id=None, format=None):
        '''
        Returns all the information about a course with the answers and the
        solutions
        '''
        if not course_id:
            return Response('Method not allowed',
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

        try:
            course = Course.objects.filter(id=course_id).first()
            course_serializer = serializer.CourseEditSerializer(
                course,
                context={
                    'request': request})
            data = course_serializer.data;
            return Response(data)

        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request, course_id=None, format=None):
        return Response("test")


class CourseView(APIView):
    '''
    Contains all code related to viewing and saving courses.
    @author Claas Voelcker
    '''
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, course_id=None, format=None):
        '''
        Returns a course if the course_id exists. The cours, it's
        modules and questions are serialized.
        '''
        if not course_id:
            return Response('Method not allowed',
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            course = Course.objects.filter(id=course_id).first()
            course_serializer = serializer.CourseSerializer(course, context={
                'request': request})
            data = course_serializer.data
            return Response(course_serializer.data,
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response('Course not found',
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request, course_id=None, format=None):
        '''
        Saves a course to the database. If the course id is provided,
        the method updates and existing course, otherwise, a new course
        is created.
        '''
        data = request.data
        if data is None:
            return Response({"error": "Request does not contain data"},
                            status=status.HTTP_404_BAD_REQUEST)

        id = data.get('id')
        # This branch saves new courses or edites existing courses
        if (id is None) and Course.objects.filter(name=data['name']).exists():
            return Response('Course with that name exists',
                            status=status.HTTP_409_CONFLICT)
        if id is None:
            data['responsible_mod'] = request.user
        else:
            data['responsible_mod'] = Course.objects.filter(id=id).first().responsible_mod

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
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class ModuleView(APIView):
    '''
    Shows a module
    @author Claas Voelcker
    '''
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, course_id, module_id, format=None):
        '''
        Shows the module
        '''
        return Response('Method not allowed',
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format=None):
        return Response('Method not allowed',
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class QuestionView(APIView):
    '''
    View to show questions and to evaluate them. This does not return the
    answers, which are given by a seperate class.
    @author Claas Voelcker
    '''
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def can_access_question(self, user, question):
        return (
                   question.is_first_question and
                   question.module.is_first_module) or user.try_set.filter(
            question__order=question.order - 1, solved=True).exists()

    def get(self, request, course_id, module_id, question_id, format=None):
        '''
        Get a question together with additional information about the module
        and position (last_module and last_question keys)
        '''
        try:
            course = Course.objects.get(id=course_id)
            module = course.module_set.all()[int(module_id)]
            question = module.question_set.all()[int(question_id)]

            if question is None:
                return Response("Question not found",
                                status=status.HTTP_404_NOT_FOUND)
            if not self.can_access_question(request.user, question):
                return Response(
                    "Previous question(s) haven't been answered correctly yet",
                    status=status.HTTP_403_FORBIDDEN)

            data = serializer.QuestionSerializer(question,
                                                 context={'request': request})
            data = data.data
            return Response(data,
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response("Question not found",
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request, course_id, module_id, question_id, format=None):
        '''
        Evaluates the answer to a question.
        @author Tobias Huber
        '''
        try:
            course = Course.objects.get(id=course_id)
            module = course.module_set.all()[int(module_id)]
            question = module.question_set.all()[int(question_id)]
        except Exception as e:
            return Response("Question not found",
                            status=status.HTTP_404_NOT_FOUND)
        # deny access if there is a/are previous question(s) and it/they
        # haven't been answered correctly
        if not (self.can_access_question(request.user, question)):
            return Response(
                "Previous question(s) haven't been answered correctly yet",
                status=status.HTTP_403_FORBIDDEN)

        solved = question.evaluate(request.data["answers"])
        Try(user=request.user, question=question,
            answer=str(request.data["answers"]), solved=solved).save()
        response = {"evaluate": solved}
        if solved and question.feedback_is_set:
            response['custom_feedback'] = question.custom_feedback()
            response['feedback'] = question.feedback
        return Response(response)


class AnswerView(APIView):
    '''
    Shows all possible answers to a question.
    @author Claas Voelcker
    '''
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, course_id, module_id, question_id, format=None):
        '''
        Lists the answers for a question
        '''
        course = Course.objects.get(id=course_id)
        module = course.module_set.all()[int(module_id)]
        question = module.question_set.all()[int(question_id)]
        answers = question.answer_set()
        data = serializer.AnswerSerializer(answers, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        return Response('Method not allowed',
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserView(APIView):
    '''
    Shows a user profile
    @author Claas Voelcker
    '''
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user_id=False, format=None):
        '''
        Shows the profile of any user if the requester is mod,
        or the profile of the requester

        TODO: Refactor this user.profile.is_mod() out of it
        AFAIK is this not the right behaviour
        but rather overriding REST functions is -TH
        #TODO: probably should be check_permissions(self, request)
        '''
        user = request.user
        if user_id:
            if user.profile.is_mod():
                user = User.objects.filter(id=user_id).first()
                if not user:
                    return Response('User not found',
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                return Response('Access denied',
                                status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.UserSerializer(user)
        return Response(user.data)

    def post(self, request, format=None):
        '''
        Post is used to update the profile of a given user
        (Guess: patch is the actual method we want to go for)
        @author Tobias Huber
        '''
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
    '''
    Shows a user profile
    @author Claas Voelcker
    '''
    authentication_classes = []
    permission_classes = []

    def post(self, request, user_id=None, format=None):
        '''
        If the user_id field is specified, it updates user information.
        Otherwise it saves a new user.

        This behaviour isn't smart since this view doesn't require any
        authentication
        '''
        if user_id:
            return Response('Please use the UserView to update data',
                            status=status.HTTP_403_FORBIDDEN)
        else:
            user_serializer = serializer.UserSerializer(data=request.data)
            if user_serializer.is_valid():
                user = user_serializer.create(request.data)
                return Response('Created a new user',
                                status=status.HTTP_201_CREATED)
            else:
                return Response(user_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)


class MultiUserView(APIView):
    '''
    Shows an overview over all users
    @author Claas Voelcker
    '''
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        '''
        Returns all users
        '''
        if not request.user.profile.is_mod():
            return Response('Access denied',
                            status=status.HTTP_401_UNAUTHORIZED)
        users = User.objects.all()
        data = serializer.UserSerializer(users, many=True).data
        return Response(data)

    def post(self, request, format=None):
        '''
        Not implemented
        '''
        return Response('Method not allowed',
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class StatisticsView(APIView):
    '''
    A class displaying statistics information for a given user. It is used to
    access the try object.
    @author: Claas Voelcker
    '''
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user_id=None):
        user = request.user if not user_id else User.objects.get(id=user_id)
        tries = Try.objects.filter(user=user)
        data = serializer.TrySerializer(tries, many=True).data
        return Response(data)

    def post(self, request, format=None):
        return Response('Method not allowed',
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class StatisticsDownloadView(APIView):
    '''
    A class returning the statistics information in the given format. It is used to
    access the try object.
    @author: Leonhard Wiedmann
    '''
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user_id=None):
        return Response({"error": 'Method not allowed'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format=None):
        import time, csv
        data = request.data
        user = request.user

        response = HttpResponse(content_type='text/csv')
        response[
            'Content-Disposition'] = 'attachment; filename="' + time.strftime(
            "%d/%m/%Y") + '-' + user.username + '.csv"'
        tries = Try.objects.all()

        groups = user.groups.values_list('name', flat=True)

        # admins can get all statistics of all users
        # if 'admin' in groups and 'user_id' in data:
        #     tries.filter(user__id=data['user_id'])

        # A moderator can get all tries of his created courses
        if 'moderator' in groups and 'course' in data:
            course = Course.objects.filter(responsible_mod=user,
                                           id=data['course'])
            if not course.exists():
                return Response({'error': 'invalid Course ID'},
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)
            tries = tries.filter(question__module__course=course.first())
        else:
            tries = tries.filter(user=user)

        if 'date' in data and 'start' in data['date'] and 'end' in data[
            'date']:
            tries = tries.filter(
                date__range=[data['date']['start'], data['date']['end']])

        # filter just for solved tries
        if 'solved' in data:
            tries = tries.filter(solved=data['solved'])

        # filter for a specific category
        if 'category' in data:
            tries = tries.filter(
                question__module__course__category__name=data['category'])

        data = serializer.TrySerializer(tries, many=True).data
        writer = csv.writer(response)
        writer.writerow(['question', 'date', 'solved'])
        for row in data:
            writer.writerow([row['question'], row['date'], row['solved']])
        return response


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
        '''
        Returns True if request is allowed and False if request isn't allowed
        or the user is already mod.
        '''
        allowed = not request.user.profile.is_mod() and request.user.profile.modrequest_allowed()
        return Response({'allowed': allowed},
                        status=status.HTTP_200_OK)

    def post(self, request, format=None):
        '''
        TODO: Fix problem with auth/perm!
        Handels the moderator rights request. Expects a reason and extracts the
        user from the request header.
        '''
        data = request.data
        user = request.user
        profile = user.profile
        if not user.profile.modrequest_allowed():
            return Response('User is mod or has sent too many requests',
                            status=status.HTTP_403_FORBIDDEN)
        # TODO: fix if an localization issues arrise
        profile.last_modrequest = timezone.localdate()

        send_mail(
            'Moderator rights requested by {}'.format(user.username),
            'The following user {} requested moderator rights for the \
            CloneCademy platform. \n \
            The given reason for this request: \n{}\n \
            If you want to add this user to the moderator group, access the \
            profile {} for the confirmation field.\n \
            Have a nice day, your CloneCademy bot'.format(
                user.username, data["reason"],
                user.profile.get_link_to_profile()),
            'bot@clonecademy.de',
            [admin.email for
                admin in Group.objects.get(name="admin").user_set.all()]
        )
        return Response({"Request": "ok"}, status=status.HTTP_200_OK)


class GrantModRightsView(APIView):
    """
    This View is used to grant a user modrights
    @author Tobias Huber
    """

    # authentication_classes=(authentication.TokenAuthentication,);
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, user_id, format=None):
        '''
        Returns True if given user with a given user_id is a moderator
        '''
        return Response(Profile.objects.get(user__id=user_id).is_mod(),
                        status=status.HTTP_200_OK)

    def post(self, request, user_id, format=None):
        '''
        Grants a user with a given user id mod rights.
        User id is taken from the url
        '''
        to_be_promoted = User.objects.get(id=user_id)
        if to_be_promoted.profile.is_mod():
            # TODO Find out if it is useful to send a 200 when a user
            # was already mod
            return Response(
                "the user \" " + to_be_promoted.username +
                "\" is already a moderator",
                status=status.HTTP_200_OK)
        mod_group = Group.objects.get(name='moderator')
        to_be_promoted.groups.add(mod_group)

        # may be replaced by tests
        if not to_be_promoted.profile.is_mod():
            return Response(
                "Something went wrong with promoting" + to_be_promoted.username,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response("successfully promoted " + to_be_promoted.username,
                        status=status.HTTP_200_OK)
