from django.test import TestCase
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
        self.c1_test_en = models.Course(name="test_1", category=self.category, difficulty=0, language='en', responsible_mod=self.u1, is_visible=True)
        self.c1_test_en.save()

    def test_get(self):
        request = self.factory.get('/courses/')
        force_authenticate(request, self.u1)
        response = self.view(request)
        self.assertEqual(response.status_code,405)

    def test_post(self):
        c1_test_en_serialized = serializers.CourseSerializer(self.c1_test_en).data

        request_1 = self.factory.post('/courses/', {'type':'all', 'language':'de', 'category':'all'})
        request_2 = self.factory.post('/courses/', {'type':'all', 'language':'en', 'category':'all'})
        request_3 = self.factory.post('/courses/', {'stuff':'kajiger'})

        force_authenticate(request_1, self.u1)
        force_authenticate(request_2, self.u1)
        force_authenticate(request_3, self.u1)

        response_1 = self.view(request_1)
        response_2 = self.view(request_2)
        response_3 = self.view(request_3)
        
        self.assertEqual(response_1.status_code,200)
        self.assertEqual(response_1.data, [])

        self.assertEqual(response_2.status_code,200)
        self.assertEqual(response_2.data, [c1_test_en_serialized])

        self.assertEqual(response_3.status_code,404)


class CourseViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.CourseView.as_view()
        
        self.u1 = User(username='admin')
        self.u1.save()

        self.category = models.CourseCategory(name="test")
        self.category.save()
        self.c1_test_en = models.Course(name="test_1", category=self.category, difficulty=0, language='en', responsible_mod=self.u1, is_visible=True)
        self.c1_test_en.save()

    def test_get(self):
        request = self.factory.get('/courses/1')
        force_authenticate(request, self.u1)
        response = self.view(request, course_id=1)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data, {'name': 'test_1', 'difficulty': 0, 'id': 1, 'modules': []})

    def test_post(self):
        request = self.factory.post('/courses/save', 
                   {'name':'test_2', 
                    'category':'test',
                    'difficulty': 2, 
                    'modules':[],
                    'language':'en'}, format='json')
        force_authenticate(request, self.u1)
        response = self.view(request)
        self.assertEqual(response.status_code,201)
        self.assertTrue(models.Course.objects.filter(name='test_2').exists())

        request = self.factory.post('/courses/save', 
                   {'name':'test_2', 
                    'category':'test',
                    'difficulty': 2, 
                    'modules':[],
                    'language':'en'}, format='json')
        force_authenticate(request, self.u1)
        response = self.view(request)
        self.assertEqual(response.status_code,409)

        request = self.factory.post('/courses/save', 
                   {'name':'test_3', 
                    'category':'test',
                    'difficulty': 2, 
                    'modules':[
                        {'name':'a module',
                         'learning_text':'no way',
                         'order':3,
                         'questions':[]},
                        {'name':'another module',
                         'learning_text':'appearing first',
                         'order':2,
                         'questions':[]}],
                    'language':'en'}, format='json')
        force_authenticate(request, self.u1)
        response = self.view(request)
        self.assertEqual(response.status_code,201)
        self.assertTrue(models.Course.objects.filter(name='test_3').exists())
        self.assertTrue(models.Module.objects.filter(name='a module').exists())
        self.assertTrue(models.Module.objects.filter(name='another module').exists())
        
        request = self.factory.post('/courses/save', 
                   {'name':'test_4', 
                    'category':'test',
                    'difficulty':2, 
                    'modules':[
                        {'name':'a module',
                         'learning_text':'no way',
                         'order':3,
                         'questions':[
                             {'title':'a question',
                              'body':'some text',
                              'feedback':'',
                              'type':'multiple_choice',
                              'order':1,
                              'answers':[
                                  {'text':'nope',
                                   'is_correct':False}]
                                 }]}],
                    'language':'en'}, format='json')
        force_authenticate(request, self.u1)
        response = self.view(request)
        self.assertEquals(response.status_code,400)
        self.assertFalse(models.Course.objects.filter(name='test_4').exists())
        self.assertFalse(multiple_choice.models.MultipleChoiceQuestion.objects.filter(title='a question').exists())

        request = self.factory.post('/courses/save', 
                   {'name':'test_4', 
                    'category':'test',
                    'difficulty':2, 
                    'modules':[
                        {'name':'a module',
                         'learning_text':'no way',
                         'order':3,
                         'questions':[
                             {'title':'a question',
                              'body':'some text',
                              'feedback':'',
                              'type':'multiple_choice',
                              'order':1,
                              'answers':[
                                  {'text':'nope',
                                   'is_correct':True}]
                                 }]}],
                    'language':'en'}, format='json')
        force_authenticate(request, self.u1)
        response = self.view(request)
        print(response.data)
        self.assertEqual(response.status_code,201)
        self.assertTrue(models.Course.objects.filter(name='test_4').exists())
        self.assertTrue(multiple_choice.models.MultipleChoiceQuestion.objects.filter(title='a question').exists())


#factory = APIRequestFactory()
#request = factory.post('/notes/', {'title': 'new idea'}, format='json')
#request = factory.post('/notes/', json.dumps({'title': 'new idea'}), content_type='application/json')

#user = User.objects.get(username='olivia')
#view = AccountDetail.as_view()

# Make an authenticated request to the view...
#request = factory.get('/accounts/django-superstars/')
#force_authenticate(request, user=user)
#response = view(request)
#force_authenticate(request, user=user, token=user.token)
