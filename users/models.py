from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User, Group
from django.db import models

# User._meta.get_field('email')._unique = True

# if not Group.objects.filter(name='admin').exists():
#     Group.objects.create(name='admin')

# if not Group.objects.filter(name='teacher').exists():
#     Group.objects.create(name='teacher')

# if not Group.objects.filter(name='student').exists():
#     Group.objects.create(name='student')


class User(AbstractUser):
    email = models.EmailField(unique=True)
