from django.contrib import admin

from .models import CourseCategory, Course, MultipleChoiceQuestion, MultipleCoiceAnswer

admin.site.register(CourseCategory)
admin.site.register(Course)
admin.site.register(MultipleChoiceQuestion)
