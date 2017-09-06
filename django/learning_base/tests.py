from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ParseError

from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from django.contrib.auth.models import User, Group
from learning_base import views, models, serializers
from learning_base.models import Profile
import learning_base.multiple_choice as MultipleChoice
import learning_base.info as InformationText


class DatabaseMixin():
    def setup_database(self):
        self.factory = APIRequestFactory()

        self.admin_group = Group.objects.create(name="admin")

        self.u1 = User(username='admin')
        self.u1.save()
        self.u1.groups.add(self.admin_group)
        self.u1_profile = Profile.objects.create(user=self.u1)
        self.u1.save()

        self.category = models.CourseCategory(name="test")
        self.category.save()

        self.c1_test_en = models.Course(name="test_1", category=self.category,
                                        difficulty=0, language='en',
                                        responsible_mod=self.u1,
                                        is_visible=True)
        self.c1_test_en.save()

        self.m1_test = models.Module(name="module_1", course=self.c1_test_en,
                                     order=1)
        self.m1_test.save()

        self.q1_test = MultipleChoice.models.MultipleChoiceQuestion(
            title="",
            text="a question",
            feedback="",
            order=1,
            module=self.m1_test)
        self.q1_test.save()

        self.a1_test = MultipleChoice.models.MultipleChoiceAnswer(
            question=self.q1_test,
            text="something",
            is_correct=False
        )
        self.a1_test.save()

        self.a2_test = MultipleChoice.models.MultipleChoiceAnswer(
            question=self.q1_test,
            text="something",
            is_correct=True)
        self.a2_test.save()

        self.q2_test = InformationText.models.InformationText(
            title="",
            text="an information text",
            feedback="",
            order=2,
            module=self.m1_test)
        self.q2_test.save()


class AnswerViewTest(DatabaseMixin, TestCase):
    def setUp(self):
        self.view = views.AnswerView.as_view()
        self.setup_database()

    def test_get(self):
        request = self.factory.get('/courses/1/1/1/answers')
        force_authenticate(request, self.u1)
        response = self.view(request, 1, 0, 0)

        answer_1_serialized = serializers.AnswerSerializer(self.a1_test).data
        answer_2_serialized = serializers.AnswerSerializer(self.a2_test).data

        self.assertEqual(response.data,
                         [answer_1_serialized, answer_2_serialized])


class MultiCourseViewTest(DatabaseMixin, TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.MultiCourseView.as_view()

        self.setup_database()

    def test_get(self):
        request = self.factory.get('/courses/')
        force_authenticate(request, self.u1)
        response = self.view(request)
        self.assertEqual(response.status_code, 405)

    def test_post(self):
        request_1 = self.factory.post('/courses/', {'type': '',
                                                    'language': 'de',
                                                    'category': ''})
        request_1.user = self.u1

        request_2 = self.factory.post('/courses/', {'type': '',
                                                    'language': 'en',
                                                    'category': ''})
        request_3 = self.factory.post('/courses/',
                                      {'stuff': 'kajiger'})

        force_authenticate(request_1, self.u1)
        force_authenticate(request_2, self.u1)
        force_authenticate(request_3, self.u1)

        c1_test_en_serialized = serializers.CourseSerializer(
            self.c1_test_en, context={'request': request_1}).data

        response_1 = self.view(request_1)
        response_2 = self.view(request_2)
        response_3 = self.view(request_3)

        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_1.data, [])

        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(response_2.data, [c1_test_en_serialized])

        self.assertEqual(response_3.status_code, 400)


class CourseViewTest(DatabaseMixin, TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.CourseView.as_view()

        self.setup_database()

    def test_get(self):
        request = self.factory.get('/courses/1')
        request.user = self.u1
        force_authenticate(request, self.u1)

        c1_test_en_serialized = serializers.CourseSerializer(
            self.c1_test_en, context={'request': request}).data

        response = self.view(request, course_id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, c1_test_en_serialized)

    def test_post(self):
        request = self.factory.post('/courses/save',
                                    {'name': 'test_2',
                                     'category': 'test',
                                     'difficulty': 2,
                                     'modules': [{'name': 'a module',
                                                  'learning_text': 'no way',
                                                  'order': 3,
                                                  'questions': [
                                                      {'title': 'a question',
                                                       'text': 'some text',
                                                       'feedback': '',
                                                       'type': 'multiple_choice',
                                                       'order': 1,
                                                       'answers': [
                                                           {'text': 'nope',
                                                            'is_correct': True},
                                                           {'text': 'nope',
                                                            'is_correct': False}]}]}],
                                     'language': 'en'}, format='json')
        force_authenticate(request, self.u1)
        response = self.view(request)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(models.Course.objects.filter(name='test_2').exists())

        request = self.factory.post('/courses/save',
                                    {'name': 'test_2',
                                     'category': 'test',
                                     'difficulty': 2,
                                     'modules': [{'name': 'a module',
                                                  'learning_text': 'no way',
                                                  'order': 3,
                                                  'questions': [
                                                      {'title': 'a question',
                                                       'text': 'some text',
                                                       'feedback': '',
                                                       'type': 'MultipleChoiceQuestion',
                                                       'order': 1,
                                                       'answers': [
                                                           {'text': 'nope',
                                                            'is_correct': False}]}]}],
                                     'language': 'en'}, format='json')
        force_authenticate(request, self.u1)
        response = self.view(request)
        self.assertEqual(response.status_code, 409)

        request = self.factory.post('/courses/save',
                                    {'name': 'test_3',
                                     'category': 'test',
                                     'difficulty': 2,
                                     'modules': [
                                         {'name': 'a module',
                                          'learning_text': 'no way',
                                          'order': 3,
                                          'questions': []},
                                         {'name': 'another module',
                                          'learning_text': 'appearing first',
                                          'order': 2,
                                          'questions': []}],
                                     'language': 'en'}, format='json')
        force_authenticate(request, self.u1)
        response = self.view(request)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(models.Course.objects.filter(name='test_3').exists())
        self.assertTrue(models.Module.objects.filter(name='a module').exists())
        self.assertTrue(
            models.Module.objects.filter(name='another module').exists())

        request = self.factory.post('/courses/save',
                                    {'name': 'test_4',
                                     'category': 'test',
                                     'difficulty': 2,
                                     'modules': [{'name': 'any module',
                                                  'learning_text': 'no way',
                                                  'order': 0,
                                                  'questions': [
                                                      {
                                                          'title': 'some question',
                                                          'text': 'any text',
                                                          'feedback': '',
                                                          'type': 'multiple_choice',
                                                          'order': 1,
                                                          'answers': [
                                                              {
                                                                  'text': 'this is not correct',
                                                                  'is_correct': False}]}]}],
                                     'language': 'en'}, format='json')
        force_authenticate(request, self.u1)
        response = self.view(request)
        self.assertEquals(response.status_code, 400)
        self.assertFalse(models.Course.objects.filter(name='test_4').exists())
        self.assertFalse(
            MultipleChoice.models.MultipleChoiceQuestion.objects.filter(
                title='any module').exists())

        request = self.factory.post('/courses/save',
                                    {'name': 'test_4',
                                     'category': 'test',
                                     'difficulty': 2,
                                     'modules': [
                                         {'name': 'a module',
                                          'learning_text': 'no way',
                                          'order': 3,
                                          'questions': [
                                              {'title': 'a question',
                                               'text': 'some text',
                                               'feedback': '',
                                               'type': 'multiple_choice',
                                               'order': 1,
                                               'answers': [
                                                   {'text': 'nope',
                                                    'is_correct': True}]
                                               }]}],
                                     'language': 'en'}, format='json')
        force_authenticate(request, self.u1)
        response = self.view(request)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(models.Course.objects.filter(name='test_4').exists())
        self.assertTrue(
            MultipleChoice.models.MultipleChoiceQuestion.objects.filter(
                title='a question').exists())

    def test_information_text(self):
        request = self.factory.post('/courses/save',
                                    {'name': 'test_4',
                                     'category': 'test',
                                     'difficulty': 2,
                                     'modules': [
                                         {'name': 'a module',
                                          'learning_text': 'no way',
                                          'order': 3,
                                          'questions': [
                                              {'title': 'a question',
                                               'text': 'some text',
                                               'feedback': '',
                                               'type': 'info_text',
                                               'order': 1,
                                               }]}],
                                     'language': 'en'}, format='json')
        force_authenticate(request, self.u1)
        response = self.view(request)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(models.Course.objects.filter(name='test_4').exists())
        self.assertTrue(
            InformationText.models.InformationText.objects.filter(
                title='a question').exists())


class CourseEditViewTest(DatabaseMixin, TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.CourseView.as_view()

        self.setup_database()

    def test_deleting_question(self):
        courseData = {
            'name': 'edit_1',
            'category': 'test',
            'difficulty': 2,
            'responsible_mod': 1,
            'responsible_mod': self.u1,
            'modules': [
                {
                    'name': 'a module',
                    'learning_text': 'no way',
                    'order': 3,
                    'questions': [
                        {
                            'title': 'a question',
                            'text': 'some text',
                            'feedback': '',
                            'type': 'multiple_choice',
                            'order': 1,
                            'answers': [
                                {
                                    'text': 'true',
                                    'is_correct': True
                                },
                                {
                                    'text': 'nope',
                                    'is_correct': False
                                }
                            ]
                        },
                        {
                            'title': 'this one will be removed',
                            'text': 'some text',
                            'feedback': '',
                            'type': 'multiple_choice',
                            'order': 2,
                            'answers': [
                                {
                                    'text': 'true',
                                    'is_correct': True
                                },
                                {
                                    'text': 'nope',
                                    'is_correct': False
                                }
                            ]
                        }
                    ]
                }
            ],
            'language': 'en'}

        course = serializers.CourseSerializer(data=courseData)
        if not course.is_valid():
            self.assertTrue(False)
        course.create(courseData)
        self.assertTrue(models.Course.objects.filter(name='edit_1').exists())

        request = self.factory.get('/courses/')
        request.user = self.u1
        edit = serializers.CourseEditSerializer(
            models.Course.objects.filter(name="edit_1").first()).data

        del edit['modules'][0]['questions'][1]

        import json
        data = json.loads(json.dumps(edit))

        data['modules'][0]['questions'][0]['answers'] = \
            data['modules'][0]['questions'][0]['question_body']['answers']

        del data['modules'][0]['questions'][0]['question_body']

        data['modules'][0]['questions'][0]['order'] = 0

        data['responsible_mod'] = self.u1
        course = serializers.CourseSerializer(data=data)
        if not course.is_valid():
            self.assertTrue(False)
        course.create(data)

        self.assertFalse(models.Question.objects.filter(
            title='this one will be removed').exists())

    def test_deleting_module(self):
        courseData = {
            'name': 'edit_2',
            'category': 'test',
            'difficulty': 2,
            'responsible_mod': 1,
            'responsible_mod': self.u1,
            'modules': [
                {
                    'name': 'a module',
                    'learning_text': 'no way',
                    'order': 3,
                    'questions': [
                        {
                            'title': 'a question',
                            'text': 'some text',
                            'feedback': '',
                            'type': 'multiple_choice',
                            'order': 1,
                            'answers': [
                                {
                                    'text': 'true',
                                    'is_correct': True
                                },
                                {
                                    'text': 'nope',
                                    'is_correct': False
                                }
                            ]
                        },
                    ]
                },
                {
                    'name': 'another module',
                    'learning_text': 'no way',
                    'order': 4,
                    'questions': [
                        {
                            'title': 'a question',
                            'text': 'some text',
                            'feedback': '',
                            'type': 'multiple_choice',
                            'order': 1,
                            'answers': [
                                {
                                    'text': 'true',
                                    'is_correct': True
                                },
                                {
                                    'text': 'nope',
                                    'is_correct': False
                                }
                            ]
                        },
                    ]
                }
            ],
            'language': 'en'}

        course = serializers.CourseSerializer(data=courseData)
        if not course.is_valid():
            self.assertTrue(False)
        course.create(courseData)
        self.assertTrue(models.Course.objects.filter(name='edit_2').exists())

        request = self.factory.get('/courses/')
        request.user = self.u1
        edit = serializers.CourseEditSerializer(
            models.Course.objects.filter(name="edit_2").first()).data

        del edit['modules'][1]

        import json
        data = json.loads(json.dumps(edit))

        data['modules'][0]['questions'][0]['answers'] = \
            data['modules'][0]['questions'][0]['question_body']['answers']

        del data['modules'][0]['questions'][0]['question_body']

        data['modules'][0]['questions'][0]['order'] = 0

        data['responsible_mod'] = self.u1
        course = serializers.CourseSerializer(data=data)
        if not course.is_valid():
            self.assertTrue(False)
        course.create(data)

        self.assertFalse(
            models.Module.objects.filter(name='another module').exists())


class RequestViewTest(DatabaseMixin, TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.RequestView.as_view()

        self.mod_group = Group(name="moderator")
        self.mod_group.save()

        self.u1 = User(username='user1')
        self.u1.save()
        self.u1_profile = models.Profile(user=self.u1)
        self.u1_profile.save()
        self.u2 = User.objects.create(username='mod')
        self.u2.groups.add(self.mod_group)
        self.u2.save()
        self.u2_profile = models.Profile(user=self.u2)
        self.u2_profile.save()
        self.u3 = User.objects.create(username="spamer")
        self.u3.save()
        self.u3_profile = models.Profile(user=self.u3)
        self.u3_profile.save()
        self.u3.profile.last_modrequest = timezone.localdate()

        Group(name="admin").save()

    def test_get(self):
        # Test for true positive
        request_1 = self.factory.get('/user/can_request_mod')
        force_authenticate(request_1, self.u1)
        response = self.view(request_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'allowed': True})

        # Test for true negative
        request_2 = self.factory.get('/user/can_request_mod')
        force_authenticate(request_2, self.u2)
        response = self.view(request_2)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(not response.data)

        # Test for true negative
        request_3 = self.factory.get('/user/can_request_mod')
        force_authenticate(request_3, self.u3)
        response = self.view(request_3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'allowed': False})

    def test_post(self):
        request_1 = self.factory.post("user/request_mod",
                                      {"reason": "you need me"}, format='json')
        force_authenticate(request_1, self.u1)
        response = self.view(request_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"Request": "ok"})
        self.assertFalse(self.u1.profile.modrequest_allowed())

        request_2 = self.factory.post("user/request_mod",
                                      {"reason": "you need me"}, format='json')
        force_authenticate(request_2, self.u2)
        response = self.view(request_2)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(self.mod_group in self.u2.groups.all())

        request_3 = self.factory.post("user/request_mod",
                                      {"reason": "you need me"}, format='json')
        force_authenticate(request_3, self.u3)
        response = self.view(request_3)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(self.mod_group in self.u1.groups.all())


class UserRightsViewTest(DatabaseMixin, TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.UserRightsView.as_view()

        self.mod_group = Group.objects.create(name="moderator")
        self.admin_group = Group.objects.create(name="admin")

        self.u1 = User.objects.create_user(username='user1')
        self.u1_profile = models.Profile.objects.create(user=self.u1)

        self.u2 = User.objects.create_user(username='mod')
        self.u2.groups.add(self.mod_group)
        self.u2.save()
        self.u2_profile = models.Profile.objects.create(user=self.u2)

        self.u3 = User.objects.create_user(username='admin')
        self.u3.groups.add(self.admin_group)
        self.u3.save()
        self.u3_profile = models.Profile.objects.create(user=self.u3)

        self.u4 = User.objects.create_user(username="spamer")
        self.u4_profile = models.Profile.objects.create(user=self.u4)
        self.u4.profile.last_modrequest = timezone.localdate()

        self.users = [self.u1, self.u2, self.u3, self.u4]
        # bad users are those who aren't allowed to promote users
        self.bad_users = [self.u1, self.u2, self.u4]

    def test_post(self):
        # check if 403 is correctly thrown
        requests = []
        responses = []
        i = 0
        for request_user in self.bad_users:
            requests.append(self.factory.post(
                "user/" + str(self.u1.id) + "/rights",
                {"right": "admin", "action": "promote"},
                format='json')
            )
            force_authenticate(requests[i], request_user)
            responses.append(self.view(requests[i]))
            self.assertEqual(responses[i].status_code, 403)
            self.assertFalse(self.u1.profile.is_admin())
            i += 1

        # try withdrawing admin rights from every kind of user as an admin
        # it should always work and the user to demote should not be
        # in the admin group afterwards
        for user_to_change in self.users:
            # try withdrawing modrights
            request2 = (self.factory.post(
                "user/" + str(user_to_change.id) + "/rights/",
                {"right": "moderator", "action": "demote"},
                format='json'
            ))
            force_authenticate(request2, self.u3)
            response2 = (self.view(request2, user_id=user_to_change.id))
            self.assertEqual(response2.status_code, 200)
            self.assertFalse(
                user_to_change.groups.filter(name="moderator").exists()
            )

            # try withdrawing admin rights
            request1 = (self.factory.post(
                "user/" + str(user_to_change.id) + "/rights/",
                {"right": "admin", "action": "demote"},
                format='json'
            ))
            force_authenticate(request1, self.u3)
            response1 = (self.view(request1, user_id=user_to_change.id))
            self.assertEqual(response1.status_code, 200)
            self.assertFalse(
                user_to_change.groups.filter(name="admin").exists()
            )

            # return adminrights to the admin user if they were
            # successfully withdrawn
            if (not self.u3_profile.is_admin()):
                self.u3.groups.add(self.admin_group)

            # try granting modrights
            request3 = (self.factory.post(
                "user/" + str(user_to_change.id) + "/rights/",
                {"right": "moderator", "action": "promote"},
                format='json'
            ))
            force_authenticate(request3, self.u3)
            response3 = (self.view(request3, user_id=user_to_change.id))
            self.assertEqual(response3.status_code, 200)
            self.assertTrue(
                user_to_change.groups.filter(name="moderator").exists()
            )

            # try granting admin rights
            request4 = (self.factory.post(
                "user/" + str(user_to_change.id) + "/rights/",
                {"right": "admin", "action": "promote"},
                format='json'
            ))
            force_authenticate(request4, self.u3)
            response4 = (self.view(request4, user_id=user_to_change.id))
            self.assertEqual(response4.status_code, 200)
            self.assertTrue(
                user_to_change.groups.filter(name="admin").exists()
            )


class QuizTest(DatabaseMixin, TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.QuestionView.as_view()
        self.setup_database()

        # self.u1 = User(username='user1')
        # self.u1.save()
        # self.u1_profile = models.Profile(user=self.u1)
        # self.u1_profile.save()

    def test_create_quiz(self):
        # creation is possible and quiz query is sorted
        courseData = {
            'name': 'quiz_1',
            'category': 'test',
            'difficulty': 2,
            'responsible_mod': 1,
            'responsible_mod': self.u1,
            'modules': [
                {
                    'name': 'a module',
                    'learning_text': 'no way',
                    'order': 3,
                    'questions': [
                        {
                            'title': 'a question',
                            'text': 'some text',
                            'feedback': '',
                            'type': 'multiple_choice',
                            'order': 1,
                            'answers': [
                                {
                                    'text': 'true',
                                    'is_correct': True
                                },
                                {
                                    'text': 'nope',
                                    'is_correct': False
                                }
                            ]
                        },
                    ]
                }
            ],
            "quiz": [
                {
                    "question": "first",
                    "image": "",
                    "answers": [
                        {
                            "text": "a sdfa sdfasd fasd fa",
                            "img": "",
                            "correct": True
                        },
                        {
                            "text": "as dfas dasd asfd adsfa sdf",
                            "img": "",
                            "correct": False
                        },
                        {
                            "text": "asdds afadsfadsf adsf ads fa dsf",
                            "img": "",
                            "correct": False
                        },
                        {
                            "text": "adf asdf asdfasdf",
                            "img": "",
                            "correct": False
                        }
                    ]
                },
                {
                    "question": "sadfasdfasdfas dasd fasd ",
                    "image": "",
                    "answers": [
                        {
                            "text": "sadfasdfasdfas dfasdf a",
                            "img": "",
                            "correct": False
                        },
                        {
                            "text": "asd fasdf asdf asd fasd f",
                            "img": "",
                            "correct": True
                        },
                        {
                            "text": "asdf asdf asdf asdf asd ",
                            "img": "",
                            "correct": False
                        },
                        {
                            "text": "asdf asdf asd",
                            "img": "",
                            "correct": False
                        }
                    ]
                },
                {
                    "question": "sadfasdfasdfas dasd fasd ",
                    "image": "",
                    "answers": [
                        {
                            "text": "sadfasdfasdfas dfasdf a",
                            "img": "",
                            "correct": False
                        },
                        {
                            "text": "asd fasdf asdf asd fasd f",
                            "img": "",
                            "correct": True
                        },
                        {
                            "text": "asdf asdf asdf asdf asd ",
                            "img": "",
                            "correct": False
                        },
                        {
                            "text": "asdf asdf asd",
                            "img": "",
                            "correct": False
                        }
                    ]
                },
                {
                    "question": "sadfasdfasdfas dasd fasd ",
                    "image": "",
                    "answers": [
                        {
                            "text": "sadfasdfasdfas dfasdf a",
                            "img": "",
                            "correct": False
                        },
                        {
                            "text": "asd fasdf asdf asd fasd f",
                            "img": "",
                            "correct": True
                        },
                        {
                            "text": "asdf asdf asdf asdf asd ",
                            "img": "",
                            "correct": False
                        },
                        {
                            "text": "asdf asdf asd",
                            "img": "",
                            "correct": False
                        }
                    ]
                },
                {
                    "question": "last",
                    "image": "",
                    "answers": [
                        {
                            "text": "sadfasdfasdfas dfasdf a",
                            "img": "",
                            "correct": False
                        },
                        {
                            "text": "asd fasdf asdf asd fasd f",
                            "img": "",
                            "correct": True
                        },
                        {
                            "text": "asdf asdf asdf asdf asd ",
                            "img": "",
                            "correct": False
                        },
                        {
                            "text": "asdf asdf asd",
                            "img": "",
                            "correct": False
                        }
                    ]
                }
            ],
            'language': 'en'}

        course = serializers.CourseSerializer(data=courseData)
        if not course.is_valid():
            self.assertTrue(False)
        course.create(courseData)
        course = models.Course.objects.filter(name='quiz_1')
        self.assertTrue(course.exists())
        course = course.first()
        self.assertEqual(len(course.quizquestion_set.all()), 5)
        self.assertEqual(course.quizquestion_set.all()[0].question, "first")
        self.assertEqual(course.quizquestion_set.all()[4].question, "last")

        # try accesing the quiz before answering the questions is not valid

        request = self.factory.get("courses/" + str(course.id) + "/quiz/0/",
                                   format="json")
        force_authenticate(request, self.u1)

        response = views.QuizView.as_view()(request, course_id=course.id,
                                            quiz_id=0)

        self.assertEqual(response.status_code, 400)

        # check if return value after every question in course is done is
        # correct
        question = MultipleChoice.models.MultipleChoiceAnswer.objects.filter(
            question__module__course__name="quiz_1", is_correct=True).first()
        correct_answer = self.factory.post(
            "courses/" + str(course.id) + "/0/0/",
            {"answers": [question.id]}, format='json')
        force_authenticate(correct_answer, self.u1)

        response = views.QuestionView.as_view()(correct_answer,
                                                course_id=course.id,
                                                module_id=0, question_id=0)
        self.assertEqual(response.data["next"], "quiz")

        # send post with false or correct answer will return 200 and send to
        # next quiz question

        answer_correct = models.QuizAnswer.objects.filter(correct=True, quiz=
        course.quizquestion_set.all()[0])

        correct_answer = self.factory.post(
            "courses/" + str(course.id) + "/quiz/0/",
            {"answers": [(lambda x: x.id)(x) for x in answer_correct]},
            format='json')
        force_authenticate(correct_answer, self.u1)

        response = views.QuestionView.as_view()(correct_answer,
                                                course_id=course.id,
                                                module_id=0, question_id=0)
        # return value of correct answer
        self.assertEqual(response.status_code, 200)

        answer_wrong = models.QuizAnswer.objects.filter(
            correct=False,
            quiz=course.quizquestion_set.all()[
                0])
        wrong_answer = self.factory.post(
            "courses/" + str(course.id) + "/quiz/0/",
            {"answers": [(lambda x: x.id)(x) for x in answer_wrong]},
            format='json')
        force_authenticate(wrong_answer, self.u1)

        response = views.QuestionView.as_view()(wrong_answer,
                                                course_id=course.id,
                                                module_id=0, question_id=0)

        # return value of wrong answer
        self.assertEqual(response.status_code, 200)

        # creation for unsolvable quiz resolves in error
        courseData = {
            'name': 'quiz_2',
            'category': 'test',
            'difficulty': 2,
            'responsible_mod': 1,
            'responsible_mod': self.u1,
            'modules': [
                {
                    'name': 'a module',
                    'learning_text': 'no way',
                    'order': 3,
                    'questions': [
                        {
                            'title': 'a question',
                            'text': 'some text',
                            'feedback': '',
                            'type': 'multiple_choice',
                            'order': 1,
                            'answers': [
                                {
                                    'text': 'true',
                                    'is_correct': True
                                },
                                {
                                    'text': 'nope',
                                    'is_correct': False
                                }
                            ]
                        },
                    ]
                },
                {
                    'name': 'another module',
                    'learning_text': 'no way',
                    'order': 4,
                    'questions': [
                        {
                            'title': 'a question',
                            'text': 'some text',
                            'feedback': '',
                            'type': 'multiple_choice',
                            'order': 1,
                            'answers': [
                                {
                                    'text': 'true',
                                    'is_correct': True
                                },
                                {
                                    'text': 'nope',
                                    'is_correct': False
                                }
                            ]
                        },
                    ]
                }
            ],
            "quiz": [
                {
                    "question": "first",
                    "image": "", "answers": [
                    {
                        "text": "a sdfa sdfasd fasd fa",
                        "img": "",
                        "correct": False
                    },
                    {
                        "text": "as dfas dasd asfd adsfa sdf",
                        "img": "",
                        "correct": False
                    },
                    {
                        "text": "asdds afadsfadsf adsf ads fa dsf",
                        "img": "",
                        "correct": False
                    },
                    {
                        "text": "adf asdf asdfasdf",
                        "img": "", "correct": False
                    }
                ]
                },
                {
                    "question": "sadfasdfasdfas dasd fasd ",
                    "image": "",
                    "answers": [
                        {
                            "text": "sadfasdfasdfas dfasdf a",
                            "img": "",
                            "correct": False
                        },
                        {
                            "text": "asd fasdf asdf asd fasd f",
                            "img": "",
                            "correct": True
                        },
                        {
                            "text": "asdf asdf asdf asdf asd ",
                            "img": "",
                            "correct": False
                        },
                        {
                            "text": "asdf asdf asd",
                            "img": "",
                            "correct": False
                        }
                    ]
                },
                {
                    "question": "sadfasdfasdfas dasd fasd ",
                    "image": "",
                    "answers": [
                        {
                            "text": "sadfasdfasdfas dfasdf a",
                            "img": "",
                            "correct": False
                        },
                        {
                            "text": "asd fasdf asdf asd fasd f",
                            "img": "",
                            "correct": True
                        },
                        {
                            "text": "asdf asdf asdf asdf asd ",
                            "img": "",
                            "correct": False
                        },
                        {
                            "text": "asdf asdf asd",
                            "img": "",
                            "correct": False
                        }
                    ]
                },
                {
                    "question": "sadfasdfasdfas dasd fasd ",
                    "image": "",
                    "answers": [
                        {
                            "text": "sadfasdfasdfas dfasdf a",
                            "img": "",
                            "correct": False
                        },
                        {
                            "text": "asd fasdf asdf asd fasd f",
                            "img": "",
                            "correct": True
                        },
                        {
                            "text": "asdf asdf asdf asdf asd ",
                            "img": "",
                            "correct": False
                        },
                        {
                            "text": "asdf asdf asd",
                            "img": "",
                            "correct": False
                        }
                    ]
                },
                {
                    "question": "last",
                    "image": "",
                    "answers": [
                        {
                            "text": "sadfasdfasdfas dfasdf a",
                            "img": "",
                            "correct": False
                        },
                        {
                            "text": "asd fasdf asdf asd fasd f",
                            "img": "",
                            "correct": True
                        },
                        {
                            "text": "asdf asdf asdf asdf asd ",
                            "img": "",
                            "correct": False
                        },
                        {
                            "text": "asdf asdf asd",
                            "img": "",
                            "correct": False
                        }
                    ]
                }
            ],
            'language': 'en'}

        quiz = serializers.CourseSerializer(data=courseData)
        if not quiz.is_valid():
            self.assertTrue(False)
        with self.assertRaises(ParseError):
            quiz.create(courseData)
        self.assertFalse(models.Course.objects.filter(name='quiz_2').exists())


class QuestionViewTest(DatabaseMixin, TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.QuestionView.as_view()

        self.setup_database()

    def test_get(self):
        # Test for true positive
        request_1 = self.factory.get('/course/1/1/1')
        force_authenticate(request_1, self.u1)
        response = self.view(request_1, course_id=1, module_id=0,
                             question_id=0)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data,
                         serializers.QuestionSerializer(self.q1_test, context={
                             'request': request_1}).data)

        # Test for true negative
        response = self.view(request_1, course_id=1, module_id=0,
                             question_id=128)
        self.assertEqual(response.status_code, 404)

        # Test for outer catch
        response = self.view(request_1, course_id=128, module_id=128,
                             question_id=128)
        self.assertEqual(response.status_code, 404)

        # Test for can't access
        response = self.view(request_1, course_id=1, module_id=0,
                             question_id=1)
        self.assertEqual(response.status_code, 403)

    def test_post(self):
        request_1 = self.factory.post('', {'answers': [0, 1]})
        request_1.user = self.u1
        force_authenticate(request_1, self.u1)
        response = self.view(request_1, course_id=1, module_id=0,
                             question_id=0)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"evaluate": False})

        can = views.QuestionView().can_access_question(self.u1, self.q2_test,
                                                       1, 1)
        self.assertFalse(can)

        # Test doesn't work because of weird behavior of testing API
        #
        # request_1 = self.factory.post('', {'answers': [2]})
        # request_1.user = self.u1
        # force_authenticate(request_1, self.u1)
        # response = self.view(request_1, course_id=1, module_id=0,
        #                      question_id=0)

        # can = views.QuestionView().can_access_question(self.u1, self.q2_test)
        # self.assertTrue(can)

    def test_can_access_question(self):
        can = views.QuestionView().can_access_question(self.u1, self.q1_test,
                                                       0, 0)
        self.assertTrue(can)

        can = views.QuestionView().can_access_question(self.u1, self.q2_test,
                                                       2, 1)
        self.assertFalse(can)
