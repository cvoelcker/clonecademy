"""
This module contains all directly accessed API functions
"""
from math import floor

from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from django.utils import timezone

from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, PermissionDenied
from rest_framework.response import Response

from . import custom_permissions
from . import serializers
from .models import Course, CourseCategory, Try, Profile, started_courses

from django.utils.crypto import get_random_string


class CategoryView(APIView):
    """
    Shows, creates, updates and deletes a category
    @author Claas Voelcker, Tobias Huber
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (custom_permissions.IsAdminOrReadOnly,)

    def get(self, request, format=None):
        """
        Shows the categories
        @author Claas Voelcker
        """
        categories = CourseCategory.objects.all()
        data = serializers.CourseCategorySerializer(categories, many=True).data
        return Response(data,
                        status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        everything else but displaying
        @author Tobias Huber
        """
        data = request.data
        # check if instance shall be deleted
        if "delete" in data and data["delete"] == "true":
            if "id" in data:
                instance = CourseCategory.get(id=data["id"])
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"ans": "a category with the given id"
                                    + " does not exist"},
                            status=status.HTTP_404_NOT_FOUND)

        # check if an id is given, signaling to update the corresponding cat.
        if "id" in data:
            category_id = data["id"]
            if CourseCategory.objects.filter(id=category_id).exists():
                category = CourseCategory.objects.get(id=category_id)
                serializer = serializers.CourseCategorySerializer(
                    category, data=data, partial=True, )
            else:
                return Response(
                    {"ans": "a category with the id " + str(category_id)
                            + " does not exist"},
                    status=status.HTTP_404_NOT_FOUND)
        else:
            # else just create a plain serializer
            serializer = serializers.CourseCategorySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


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
            types = ['mod', 'started']
            categories = [str(x) for x in CourseCategory.objects.all()]
            languages = [x[0] for x in Course.LANGUAGES]
            data = request.data
            r_type = data['type']
            r_category = data['category']
            r_lan = data['language']

            # checks whether the query only contains acceptable keys
            if not ((r_type in types or not r_type)
                    and (r_category in categories or not r_category)
                    and (r_lan in languages or not r_lan)):
                return Response({"ans": "Query not possible"},
                                status=status.HTTP_400_BAD_REQUEST)

            courses = Course.objects.all()
            courses = courses.filter(language=r_lan)

            # filter invisible courses if neccessary
            if not (request.user.profile.is_mod()
                    or request.user.profile.is_admin()):
                courses = courses.filter(is_visible=True)

            if r_category != "":
                category = CourseCategory.objects.filter(
                    name=r_category).first()
                courses = courses.filter(category=category)
            if r_type == "mod":
                courses = courses.filter(responsible_mod=request.user)
            elif r_type == "started":
                courses = started_courses(request.user)
            data = serializers.CourseSerializer(courses, many=True, context={
                'request': request}).data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as errors:
            return Response({"ans": "Query not possible" + str(errors)},
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
            course_serializer = serializers.CourseEditSerializer(
                course,
                context={
                    'request': request})
            data = course_serializer.data
            return Response(data)

        except Exception as errors:
            # TODO: Try if the conformate "ans" instead of "error"
            # works as good as this
            return Response({'error': str(errors)},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request, course_id=None, format=None):
        """
        Not implemented
        """
        return Response({"ans": 'Method not allowed'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


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
            course_serializer = serializers.CourseSerializer(course, context={
                'request': request})
            return Response(course_serializer.data,
                            status=status.HTTP_200_OK)
        except Exception:
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
                            status=status.HTTP_400_BAD_REQUEST)

        course_id = data.get('id')
        # This branch saves new courses or edites existing courses
        if (course_id is None) and Course.objects.filter(
                name=data['name']).exists():
            return Response({"ans": 'Course with that name exists'},
                            status=status.HTTP_409_CONFLICT)
        if course_id is None:
            data['responsible_mod'] = request.user
        else:
            responsible_mod = Course.objects.get(id=course_id).responsible_mod
            # decline access if user is wether admin nor responsible_mod
            if (request.user.profile.is_admin()
                or request.user == responsible_mod):
                data['responsible_mod'] = Course.objects.get(
                    id=course_id).responsible_mod
            else:
                raise PermissionDenied(detail="You're not allowed to edit this"
                                              + "course, since you're not the"
                                              + "responsible mod",
                                       code=None)

        course_serializer = serializers.CourseSerializer(data=data)
        if not course_serializer.is_valid():
            return Response({"error": course_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                course_serializer.create(data)
                return Response({"success": "Course saved"},
                                status=status.HTTP_201_CREATED)
            except ParseError as error:
                return Response({"error": str(error)},
                                status=status.HTTP_400_BAD_REQUEST)


class ToggleCourseVisibilityView(APIView):
    """
    changes the visibility of a course

    alternatively sets the visibility to the provided state
    {
        "is_visible": (optional) True|False
    }

    @author Tobias Huber
    """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (custom_permissions.IsAdmin,)

    def post(self, request, course_id, format=None):
        if course_id is None:
            return Response({"ans": "course_id must be provided"},
                            status=status.HTTP_400_BAD_REQUEST)
        elif not Course.objects.filter(id=course_id).exists():
            return Response({"ans": "course not found. id: " + course_id},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            course = Course.objects.get(id=course_id)
            if "is_visible" in request.data:
                course.is_visible = request.data["is_visible"]
            else:
                course.is_visible = not course.is_visible
            course.save()
            return Response({"is_visible": course.is_visible},
                            status=status.HTTP_200_OK)


class ModuleView(APIView):
    """
    Shows a module
    @author Claas Voelcker
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, course_id, module_id, format=None):
        """
        Not implemented
        """
        return Response({"ans": 'Method not allowed'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format=None):
        """
        Not implemented
        """
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

    @staticmethod
    def can_access_question(user, question, module_id, question_id):
        """
        Checks if the question is accessable by the user (all questions before
        need to be answered correctly)
        :param user:
        :param question:
        :param module_id:
        :param question_id:
        :return:
        """
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
        return False

    def get(self, request, course_id, module_id, question_id, format=None):
        """
        Get a question together with additional information about the module
        and position (last_module and last_question keys)
        """
        try:
            course = Course.objects.get(id=course_id)
            course_module = course.module_set.all()[int(module_id)]
            question = course_module.question_set.all()[int(question_id)]

            if question is None:
                return Response({"ans": "Question not found"},
                                status=status.HTTP_404_NOT_FOUND)
            if not self.can_access_question(request.user, question, module_id,
                                            question_id):
                return Response({"ans": "Previous question(s) haven't been "
                                        "answered correctly yet"},
                                status=status.HTTP_403_FORBIDDEN)
            data = serializers.QuestionSerializer(question,
                                                  context={'request': request})
            data = data.data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": str(error)},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request, course_id, module_id, question_id, format=None):
        """
        Evaluates the answer to a question.
        @author Tobias Huber
        """
        try:
            course = Course.objects.get(id=course_id)
            course_module = course.module_set.all()[int(module_id)]
            question = course_module.question_set.all()[int(question_id)]
        except Exception:
            return Response({"ans": "Question not found"},
                            status=status.HTTP_404_NOT_FOUND)
        # deny access if there is a/are previous question(s) and it/they
        # haven't been answered correctly
        if not (self.can_access_question(request.user, question, module_id,
                                         question_id)):
            return Response(
                {"ans": "Previous question(s) haven't been answered"
                        + " correctly yet"},
                status=status.HTTP_403_FORBIDDEN
            )

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
            next_type = ""
            if not question.is_last_question():
                next_type = "question"
            elif not course_module.is_last_module():
                next_type = "module"
            elif course.quizquestion_set.exists():
                next_type = "quiz"
            response['next'] = next_type
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
        data = [serializers.get_answer_serializer(answer) for answer in
                answers]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Not implemented
        :param request:
        :param format:
        :return:
        """
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

    def get(self, request, course_id):
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

        quiz = course.quizquestion_set.all()
        if len(quiz) in range(5, 21):
            quiz = serializers.QuizSerializer(quiz, many=True)

            return Response(quiz.data)
        return Response({"error": "this quiz is invalid"},
                        status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, course_id, format=None):
        """
        Resolves this quiz question for the current user.
        """
        course = Course.objects.filter(id=course_id).first()
        quiz = course.quizquestion_set.all()

        if len(quiz) <= 0:
            return Response({"error": "this quiz does not exist"},
                            status=status.HTTP_404_NOT_FOUND)

        if len(quiz) != len(request.data):
            return Response({"error": "the quiz has " + str(
                len(quiz)) + " question and your evaluation has " + str(
                len(request.data)), "test": request.data},
                            status=status.HTTP_400_BAD_REQUEST)

        response = []
        newly_solved = 0
        old_solved = 0
        for i, quiz_entry in enumerate(quiz):
            answerSolved = request.data[i]
            for answer in request.data:
                if 'id' in answer and quiz_entry.id is answer['id']:
                    answer.pop('id')
                    answerSolved = answer
                    break;
            solved = quiz_entry.evaluate(answerSolved)
            if solved and not quiz_entry.try_set.filter(
                    user=request.user, solved=True).exists():
                newly_solved += 1
                request.user.profile.ranking += quiz_entry.get_points()
            elif quiz_entry.try_set.filter(user=request.user,
                                           solved=True).exists():
                old_solved += 1
            Try(user=request.user, quiz_question=quiz_entry,
                answer=str(request.data), solved=solved).save()

            response.append({"name": quiz[i].question, "solved": solved})
        old_extra = floor(old_solved / 5)
        new_extra = floor((newly_solved + old_solved) / 5)
        request.user.profile.ranking += (new_extra - old_extra) * 2
        request.user.profile.save()

        return Response(response, status=status.HTTP_200_OK)


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

        user = serializers.UserSerializer(user)
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

        user_serializer = serializers.UserSerializer(user, data=data,
                                                     partial=True)
        if user_serializer.is_valid():
            user_serializer = user_serializer.update(
                user,
                validated_data=request.data)
            return Response({"ans": 'Updated user ' + user.username},
                            status=status.HTTP_200_OK)
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
        user_serializer = serializers.UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.create(request.data)
            return Response({"ans": 'Created a new user'},
                            status=status.HTTP_201_CREATED)
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
        data = serializers.UserSerializer(users, many=True).data
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
        """
        shows the statistics of the given user
        """
        user = request.user if not user_id else User.objects.get(id=user_id)
        tries = Try.objects.filter(user=user)
        data = serializers.TrySerializer(tries, many=True).data
        return Response(data)

    def post(self, request, format=None):
        """
        implements filtering logic for the statistics
        :param request:
        :param format:
        :return:
        """
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
        elif is_mod and 'course' in data and not 'admin' in groups:
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

            if 'list_questions' in data:
                course = Course.objects.filter(id=data['course']).first()
                value = []
                index = 0
                for module in course.module_set.all():
                    value.append([])
                    for question in module.question_set.all():
                        value[index].append({"name": question.title,
                                             "solved": len(
                                                 question.try_set.filter(
                                                     solved=True).all()),
                                             "not solved": len(
                                                 question.try_set.filter(
                                                     solved=False).all())})
                    index += 1
                return Response(value)

        # get the statistics for a specific time
        if ('date' in data
            and 'start' in data['date']
            and 'end' in data['date']):
            start = data['date']['start']
            end = data['date']['end']
            tries = tries.filter(
                date__range=[start, end])

        # filter just for solved tries
        if 'solved' in data:
            tries = tries.filter(solved=data['solved'])

        # filter for a specific category
        if 'category' in data:
            tries = tries.filter(
                question__module__course__category__name=data['category'])

        # if this variable is set the view will return a array of dicts which are {name: string, color: string, counter: number}
        if 'categories__with__counter' in data:
            categories = CourseCategory.objects.all()
            value = []
            for cat in categories:
                value.append(
                    {
                        'name': cat.name,
                        'color': cat.color,
                        'counter': len(tries.filter(
                            question__module__course__category=cat))
                    })
            return Response(value)

        serialize_data = None

        if 'filter' in data:
            value = {}
            for trie in tries:
                if not str(getattr(trie, data['filter'])) in value:
                    value[str(getattr(trie, data['filter']))] = 1
                else:
                    value[str(getattr(trie, data['filter']))] += 1
            return Response(value)

        # this part orders the list for the "order" value in the request
        if 'order' in data:
            tries = tries.order_by(data['order'])

        if 'serialize' in data:
            serialize_data = serializers.TrySerializer(tries, many=True,
                                                       context={
                                                           'serialize': data[
                                                               'serialize']}).data
        else:
            serialize_data = serializers.TrySerializer(tries, many=True).data

        if 'format' in data and data['format'] == "csv":
            response = HttpResponse(content_type='text/csv')
            filename = time.strftime("%d/%m/%Y") + '-' + user.username + '.csv'
            content = 'attachment; filename="' + filename
            response['Content-Disposition'] = content
            writer = csv.writer(response)
            writer.writerow(['question', 'user', 'date', 'solved'])
            for row in serialize_data:
                profile = Profile.objects.get(user__username=row['user'])
                profile_hash = profile.get_hash()
                writer.writerow(
                    [row['question'],
                     profile_hash,
                     row['date'],
                     row['solved']])
            return response
        return Response(serialize_data)


class RankingView(APIView):
    """
    A view for the ranking. The get method returns an ordered list of all users
    according to their rank.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        API request for ranking information
        :param request: can be empty
        :param format: request: can be empty
        :return: a json response with ranking information
        """
        profiles = Profile.objects.all().reverse()
        data = serializers.RankingSerializer(profiles).data
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
        """
        changes the group membership of the user
        """
        data = request.data
        right_choices = ['moderator', 'admin']
        action_choices = ['promote', 'demote']
        errors = {}

        # validation
        if not data["right"] or not data["right"] in right_choices:
            errors["right"] = ("this field is required and must be one of "
                               + "the following options"
                               + ', '.join(right_choices))
        if not data["action"] or not data["action"] in action_choices:
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
        if action == "promote":
            user.groups.add(group)
        elif action == "demote":
            user.groups.remove(group)
        return Response(serializers.UserSerializer(user).data)

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


class PwResetView(APIView):
    """
    Resets the password of a user and sends the new one to the email adress
    of the user

    {
        "email": the email of the user
    }
    """

    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format=None):
        data = request.data
        if ("email" not in data):
            return Response({"ans": "you must provide an email"},
                            status=status.HTTP_400_BAD_REQUEST)
        elif (not User.objects.filter(email=data["email"]).exists()):
            return Response({"ans": "no user with email: " + data["email"]},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            user = User.objects.get(email=data["email"])
            # generate a randome password with the random implementation of
            # django.utils.crypto
            new_password = get_random_string(length=16)

            send_mail(
                'Password Reset on clonecademy.net',
                'Hello {},\n \
                You have requested a new password on clonecademy.net \n \
                Your new password is: \n {} \n \n \
                Please change it imediately! \n \
                Have a nice day,\n your CloneCademy bot'.format(
                    user.username, new_password
                ),
                'bot@clonecademy.de',
                [user.email]
            )
            user.set_password(new_password)
            return Response(status=status.HTTP_200_OK)
