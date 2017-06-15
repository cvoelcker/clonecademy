from django.contrib import admin

from .models import CourseCategory, Course, Module, Question
from learning_base.multiply_choice.models import *

admin.site.register(Module)
admin.site.register(CourseCategory)
admin.site.register(Course)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(MultipleChoiceAnswer)
