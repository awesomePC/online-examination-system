from django.db import models
from django.contrib.auth.models import User, Group

User._meta.get_field('email')._unique = True

if not Group.objects.filter(name='teacher').exists():
    Group.objects.create(name='teacher')

if not Group.objects.filter(name='student').exists():
    Group.objects.create(name='student')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} Profile"
