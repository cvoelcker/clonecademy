"""clonecadamy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from rest_framework import routers
from django.contrib import admin

from learning_base import views
from rest_framework.authtoken import views as auth_views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth', auth_views.obtain_auth_token),

    url(r'^courses/$', views.MultiCourseView.as_view()),
    url(r'^courses/(?P<course_id>[0-9]+)/?$', views.CourseView.as_view()),
    url(r'^courses/(?P<course_id>[0-9]+)?/edit$',
        views.CourseEditView.as_view()),
    url(r'^courses/(?P<course_id>[0-9]+)/(?P<module_id>[0-9]+)/?$',
        views.ModuleView.as_view()),
    url(
        r'^courses/(?P<course_id>[0-9]+)/(?P<module_id>[0-9]+)/'
        r'(?P<question_id>[0-9]+)/?$',
        views.QuestionView.as_view()),
    url(
        r'^courses/(?P<course_id>[0-9]+)/(?P<module_id>[0-9]+)/'
        r'(?P<question_id>[0-9]+)/?answers',
        views.AnswerView.as_view()),
    url(r'^courses/save$', views.CourseView.as_view()),
    url(r'^get-course-categories/$', views.CategoryView.as_view()),

    url(r'^user/$', views.MultiUserView.as_view()),
    url(r'^user/(?P<user_id>[0-9]+)/?$', views.UserView.as_view()),
    url(r'^user/(?P<user_id>[0-9]+)/grantmodrights$',
        views.GrantModRightsView.as_view()),
    url(r'^user/(?P<user_id>[0-9]+)/statistics$',
        views.StatisticsView.as_view()),
    url(r'^user/statistics$', views.StatisticsView.as_view()),
    url(r'^user/mod_request$', views.RequestView.as_view()),
    url(r'^user/current$', views.UserView.as_view()),

    url(r'^register/$', views.UserRegisterView.as_view())
]
