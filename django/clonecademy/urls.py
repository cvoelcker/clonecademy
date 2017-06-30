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

from learning_base import views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth', obtain_jwt_token),

    url(r'^courses/$', views.getCourses),
    url(r'^courses/(?P<courseID>[0-9]+)/?$', views.singleCourse),
    url(r'^courses/(?P<courseID>[0-9]+)/(?P<moduleIndex>[0-9]+)/?$', views.callModule),
    url(r'^courses/(?P<courseID>[0-9]+)/(?P<moduleIndex>[0-9]+)/(?P<questionIndex>[0-9]+)/?$', views.callQuestion),

    url(r'^get-course-categories/$', views.getCourseCategories),

    url(r'^save/course/$', views.save),
    url(r'^user/statistics$', views.getStatisticsOverview),
    url(r'^user/request_mod$', views.requestModStatus),
    url(r'^user/can_request_mod$', views.canRequestMod),
    url(r'^user/grant_mod/$', views.grantModStatus), #probably change pattern to pass the username to the function call
    url(r'^user/$', views.UserView.as_view()),
    url(r'^user/(?P<userID>[0-9]+)/?$', views.getUserDetails),
    url(r'^current_user/$', views.getCurrentUser),

    url(r'^list-user/', views.getUsers),

    url(r'^register/', views.createNewUser)
]
