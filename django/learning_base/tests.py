from django.test import TestCase
from django.utils import timezone

from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from django.contrib.auth.models import User, Group
from learning_base import views, models, serializers
import learning_base.multiple_choice as MultipleChoiceQuestion
import learning_base.info as InformationText

class DatabaseMixin():
    def setup_database(self):
        self.factory = APIRequestFactory()

        self.u1 = User(username='admin')
        self.u1.save()

        self.category = models.CourseCategory(name="test")
        self.category.save()

        self.c1_test_en = models.Course(name="test_1", category=self.category,
                                        difficulty=0, language='en',
                                        responsible_mod=self.u1,
                                        is_visible=True)
        self.c1_test_en.save()

        self.m1_test = models.Module(name="modue_1", course=self.c1_test_en,
                                     order=1)
        self.m1_test.save()

        self.q1_test = MultipleChoiceQuestion.models.MultipleChoiceQuestion(
            title="",
            body="a question",
            feedback="",
            order=1,
            module=self.m1_test)
        self.q1_test.save()
        self.q2_test = InformationText.models.InformationText(
            title="",
            body="an information text",
            feedback="",
            order=2,
            module=self.m1_test)
        self.q2_test.save()

        Group(name="admin").save()



class AnswerViewTest(DatabaseMixin, TestCase):
    def setUp(self):
        self.view = views.AnswerView.as_view()
        self.setup_database()

    def test_get(self):
        request = self.factory.get('/courses/1/1/1/answers')
        force_authenticate(request, self.u1)
        response = self.view(request, 1, 0, 0)

        self.assertEqual(response.data, [])

        answer_1 = MultipleChoiceQuestion.models.MultipleChoiceAnswer(
            question=self.q1_test,
            text="something",
            is_correct=False)
        answer_1.save()
        answer_2 = MultipleChoiceQuestion.models.MultipleChoiceAnswer(
            question=self.q1_test,
            text="something",
            is_correct=False)
        answer_2.save()
        answer_1_serialized = serializers.AnswerSerializer(answer_1).data
        answer_2_serialized = serializers.AnswerSerializer(answer_2).data
        response = self.view(request, 1, 0, 0)

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
                                           'body': 'some text',
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
                                           'body': 'some text',
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
                                          {'title': 'some question',
                                           'body': 'any text',
                                           'feedback': '',
                                           'type': 'multiple_choice',
                                           'order': 1,
                                           'answers': [
                                               {'text': 'this is not correct',
                                                'is_correct': False}]}]}],
                                     'language': 'en'}, format='json')
        force_authenticate(request, self.u1)
        response = self.view(request)
        self.assertEquals(response.status_code, 400)
        self.assertFalse(models.Course.objects.filter(name='test_4').exists())
        self.assertFalse(
            MultipleChoiceQuestion.models.MultipleChoiceQuestion.objects.filter(
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
                                               'body': 'some text',
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
            MultipleChoiceQuestion.models.MultipleChoiceQuestion.objects.filter(
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
                                               'body': 'some text',
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
                        'questions':[
                            {
                            'title': 'a question',
                            'body': 'some text',
                            'feedback': '',
                            'type': 'multiple_choice',
                            'order': 1,
                            'answers':[
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
                            'body': 'some text',
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
        edit = serializers.CourseEditSerializer(models.Course.objects.filter(name="edit_1").first()).data

        del edit['modules'][0]['questions'][1]

        import json
        data = json.loads(json.dumps(edit))

        data['modules'][0]['questions'][0]['answers'] = data['modules'][0]['questions'][0]['question_body']['answers']

        del data['modules'][0]['questions'][0]['question_body']

        data['modules'][0]['questions'][0]['order'] = 0

        data['responsible_mod'] = self.u1
        course = serializers.CourseSerializer(data=data)
        if not course.is_valid():
            self.assertTrue(False)
        course.create(data)

        self.assertFalse(models.Question.objects.filter(title='this one will be removed').exists())


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
                        'questions':[
                            {
                            'title': 'a question',
                            'body': 'some text',
                            'feedback': '',
                            'type': 'multiple_choice',
                            'order': 1,
                            'answers':[
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
                        'questions':[
                            {
                            'title': 'a question',
                            'body': 'some text',
                            'feedback': '',
                            'type': 'multiple_choice',
                            'order': 1,
                            'answers':[
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
        edit = serializers.CourseEditSerializer(models.Course.objects.filter(name="edit_2").first()).data

        del edit['modules'][1]

        import json
        data = json.loads(json.dumps(edit))

        data['modules'][0]['questions'][0]['answers'] = data['modules'][0]['questions'][0]['question_body']['answers']

        del data['modules'][0]['questions'][0]['question_body']

        data['modules'][0]['questions'][0]['order'] = 0

        data['responsible_mod'] = self.u1
        course = serializers.CourseSerializer(data=data)
        if not course.is_valid():
            self.assertTrue(False)
        course.create(data)

        self.assertFalse(models.Module.objects.filter(name='another module').exists())


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
