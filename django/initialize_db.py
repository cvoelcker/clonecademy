from django.contrib.auth.models import User, Group
from learning_base.models import CourseCategory, Profile, Settings
import settings_secret as secrets

User.objects.create_superuser(
        'admin',
        secrets.ADMIN_EMAIL,
        secrets.ADMIN_PASSWORD)

admin = User.objects.first()

admin_profile = Profile(user=admin)
admin_profile.save()

admins = Group(name="admin")
moderator = Group(name="moderator")
trusted_moderator = Group(name="trusted_moderator")

admins.save()
moderator.save()
trusted_moderator.save()

admins.user_set.add(admin)
moderator.user_set.add(admin)
trusted_moderator.user_set.add(admin)

general = CourseCategory(name='General')
general.save()

settings = Settings()
settings.save()
