from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(StudentRequest)
admin.site.register(Teacher)
admin.site.register(TeacherRequest)
