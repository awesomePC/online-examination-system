from django.urls import path
from .views import *

app_name = "users"

urlpatterns = [
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
    path("student-profile/", student_profile, name="student_profile"),
    path("student-delete/", student_delete, name="student_delete"),
    path("teacher-profile/", teacher_profile, name="teacher_profile"),
    path("teacher-delete/", teacher_delete, name="teacher_delete"),
    path("demo-login", demo_login, name="demo_login"),
]
