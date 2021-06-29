from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Create admin, teacher and student groups'

    def handle(self, *args, **kwargs):
        Group.objects.create(name='admin')
        Group.objects.create(name='teacher')
        Group.objects.create(name='student')
