from django.contrib import admin

from .models import *
from .multiple_choice.models import *
from .info.models import *

# Register your models here.

admin.site.register(Profile)
admin.site.register(LearningGroup)
admin.site.register(Try)
admin.site.register(Module)
admin.site.register(CourseCategory)
admin.site.register(Course)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(MultipleChoiceAnswer)
admin.site.register(InformationText)
admin.site.register(InformationYoutube)

