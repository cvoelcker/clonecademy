from django.contrib import admin

from .models import LearningGroup, Profile, Try


# Register your models here.

admin.site.register(LearningGroup)
admin.site.register(Profile)
admin.site.register(Try)
