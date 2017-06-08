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
from rest_framework_jwt.views import obtain_jwt_token
from django.contrib import admin

from learning_base import views as learning_base_view
from user_model import views as user_view

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth', obtain_jwt_token),

    url(r'^courses/$', learning_base_view.getCourses),
    url(r'^courses/(?P<courseID>[0-9]+)/?$', learning_base_view.singleCourse),
    url(r'^courses/(?P<courseID>[0-9]+)/(?P<moduleIndex>[0-9]+)/?$', learning_base_view.callModule),
    url(r'^courses/(?P<courseID>[0-9]+)/(?P<moduleIndex>[0-9]+)/(?P<questionIndex>[0-9]+)/?$', learning_base_view.callQuestion),

    url(r'^get-course-categories/$', learning_base_view.getCourseCategories),

    url(r'^save/course/$', learning_base_view.save),

    url(r'^user/statistics$', user_view.getStatisticsOverview),
    url(r'^user/request_mod$', user_view.requestModStatus),
    url(r'^user/can_request_mod$', user_view.canRequestMod),
    url(r'^user/', user_view.getUserInfo),
    url(r'^user/(?P<userID>[0-9]+)/?$', user_view.getUserDetails),

    url(r'^list-user/', user_view.getAllUsers),

    url(r'^register/', user_view.createNewUser)
]
