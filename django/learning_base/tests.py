from django.test import TestCase
from django.utils import timezone

from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from django.contrib.auth.models import User, Group
from learning_base import views, models, serializers
import learning_base.multiple_choice as multiple_choice


class MultiCourseViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.MultiCourseView.as_view()

        self.u1 = User(username='admin')
        self.u1.save()

        self.category = models.CourseCategory(name="test")
        self.category.save()
        self.c1_test_en = models.Course(name="test_1", category=self.category,
                                        difficulty=0, language='en',
                                        responsible_mod=self.u1,
                                        is_visible=True)
        self.c1_test_en.save()

    def test_get(self):
        request = self.factory.get('/courses/')
        force_authenticate(request, self.u1)
        response = self.view(request)
        self.assertEqual(response.status_code, 405)

    def test_post(self):
        c1_test_en_serialized = serializers.CourseSerializer(
            self.c1_test_en).data

        request_1 = self.factory.post('/courses/', {'type': '',
                                                    'language': 'de',
                                                    'category': ''})
        request_2 = self.factory.post('/courses/', {'type': '',
                                                    'language': 'en',
                                                    'category': ''})
        request_3 = self.factory.post('/courses/',
                                      {'stuff': 'kajiger'})

        force_authenticate(request_1, self.u1)
        force_authenticate(request_2, self.u1)
        force_authenticate(request_3, self.u1)

        response_1 = self.view(request_1)
        response_2 = self.view(request_2)
        response_3 = self.view(request_3)

        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_1.data, [])

        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(response_2.data, [c1_test_en_serialized])

        self.assertEqual(response_3.status_code, 400)


class CourseViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.CourseView.as_view()

        self.u1 = User(username='admin')
        self.u1.save()

        self.category = models.CourseCategory(name="test")
        self.category.save()
        self.c1_test_en = models.Course(name="test_1", category=self.category,
                                        difficulty=0, language='en',
                                        responsible_mod=self.u1,
                                        is_visible=True)
        self.c1_test_en.save()

    def test_get(self):
        c1_test_en_serialized = serializers.CourseSerializer(
            self.c1_test_en).data
        request = self.factory.get('/courses/1')
        force_authenticate(request, self.u1)
        response = self.view(request, course_id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, c1_test_en_serialized)

    def test_post(self):
        request = self.factory.post('/courses/save',
                                    {'name': 'test_2',
                                     'category': 'test',
                                     'difficulty': 2,
                                     'modules': [],
                                     'language': 'en'}, format='json')
        force_authenticate(request, self.u1)
        response = self.view(request)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(models.Course.objects.filter(name='test_2').exists())

        request = self.factory.post('/courses/save',
                                    {'name': 'test_2',
                                     'category': 'test',
                                     'difficulty': 2,
                                     'modules': [],
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

        request = self.factory.post(
            '/courses/save',
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
                            'is_correct': False}]}]}],
             'language': 'en'}, format='json')
        force_authenticate(request, self.u1)
        response = self.view(request)
        self.assertEquals(response.status_code, 400)
        self.assertFalse(models.Course.objects.filter(name='test_4').exists())
        self.assertFalse(
            multiple_choice.models.MultipleChoiceQuestion.objects.filter(
                title='a question').exists())

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
            multiple_choice.models.MultipleChoiceQuestion.objects.filter(
                title='a question').exists())


class RequestViewTest(TestCase):
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

    def test_get(self):
        "Test for true positive"
        request_1 = self.factory.get('/user/can_request_mod')
        force_authenticate(request_1, self.u1)
        response = self.view(request_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, True)

        "Test for true negative"
        request_2 = self.factory.get('/user/can_request_mod')
        force_authenticate(request_2, self.u2)
        response = self.view(request_2)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(not response.data)

        "Test for true negative"
        request_3 = self.factory.get('/user/can_request_mod')
        force_authenticate(request_3, self.u3)
        response = self.view(request_3)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(not response.data)

    def test_post(self):
        request_1 = self.factory.post("user/request_mod",
                                      {"reason": "you need me"}, format='json')
        force_authenticate(request_1, self.u1)
        response = self.view(request_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"Request": "ok"})
        self.assertTrue(self.mod_group in self.u1.groups.all())

        request_2 = self.factory.post("user/request_mod",
                                      {"reason": "you need me"}, format='json')
        force_authenticate(request_2, self.u2)
        response = self.view(request_2)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"Request": "ok"})
        self.assertTrue(self.mod_group in self.u1.groups.all())

        request_3 = self.factory.post("user/request_mod",
                                      {"reason": "you need me"}, format='json')
        force_authenticate(request_3, self.u3)
        response = self.view(request_3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"Request": "ok"})
        self.assertFalse(self.mod_group in self.u1.groups.all())

        pass

# factory = APIRequestFactory()
# request = factory.post('/notes/', {'title': 'new idea'}, format='json')
# request = factory.post('/notes/', json.dumps({'title': 'new idea'}), content_type='application/json')

# user = User.objects.get(username='olivia')
# view = AccountDetail.as_view()

# Make an authenticated request to the view...
# request = factory.get('/accounts/django-superstars/')
# force_authenticate(request, user=user)
# response = view(request)
# force_authenticate(request, user=user, token=user.token)
