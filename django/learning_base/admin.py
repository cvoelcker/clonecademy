from django.contrib import admin

from .models import CourseCategory, Course, Module, Question, LearningGroup, Try, ModRequest
from learning_base.multiple_choice.models import *

# Register your models here.

admin.site.register(LearningGroup)
admin.site.register(Try)
admin.site.register(Module)
admin.site.register(CourseCategory)
admin.site.register(Course)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(MultipleChoiceAnswer)
admin.site.register(ModRequest)
