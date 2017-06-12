from django.contrib.auth.models import Permission, Group, ContentType, User
from itertools import chain
from datetime import datetime
from learning_base.models import *
from user_model.models import Profile


import sys

question_type = ContentType.objects.filter(model="question").first()
course_type = ContentType.objects.filter(model="course").first()
module_type = ContentType.objects.filter(model="module").first()

all_permissions = Permission.objects.filter(content_type=ContentType.objects.all())

question_permissions = Permission.objects.filter(content_type=question_type)
course_permissions = Permission.objects.filter(content_type=course_type)
module_permissions = Permission.objects.filter(content_type=module_type)

#admin has all permissions
if not Group.objects.filter(name="admin").exists():
    admin = Group(name="admin")
    admin.save()
    admin.permissions = all_permissions

# create moderator group with all permissions on questions, modules and courses
if not Group.objects.filter(name="moderator").exists():
    moderator = Group(name="moderator")
    moderator.save()
    moderator.permissions = list(chain(question_permissions, course_permissions, module_permissions))
    moderator.save()

admin_user = User.objects.filter(username="admin").first()

admin_user.groups = Group.objects.filter(name="admin")
admin_user.save()

p = Profile(user=admin_user, date_registered= datetime.now())
p.save()
