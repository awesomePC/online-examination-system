from django.urls import path
from .views import *

app_name = "teachers"

urlpatterns = [
    path("student-profiles/", students_list, name="students_list"),
    path("student-requests/", students_request_list, name="students_request_list"),
    path("student-delete/<int:pk>/", student_delete, name="student_delete"),
    path(
        "student-request-accept/<int:pk>/",
        student_request_accept,
        name="student_request_accept",
    ),
    path("exams/<int:exam_pk>/results/", result_list, name="result_list"),
    path("results/<int:pk>/", result_detail, name="result_detail"),
]
