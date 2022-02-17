from django.urls import path
from .views import *

app_name = "hod"

urlpatterns = [
    path("teacher-profiles/", teachers_list, name="teachers_list"),
    path("teacher-requests/", teachers_request_list, name="teachers_request_list"),
    path("teacher-delete/<int:pk>/", teacher_delete, name="teacher_delete"),
    path(
        "teacher-request-accept/<int:pk>/",
        teacher_request_accept,
        name="teacher_request_accept",
    ),
]
