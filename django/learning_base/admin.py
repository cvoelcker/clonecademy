from django.contrib import admin

from .models import CourseCategory, Course
from learning_base.question.multiply_choice.models import *

admin.site.register(CourseCategory)
admin.site.register(Course)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(MultipleChoiceAnswer)
