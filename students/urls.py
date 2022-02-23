from django.urls import path
from .views import *

app_name = "students"

urlpatterns = [
    path("exams/", exams_list, name="exams_list"),
    path("exams/<int:pk>/start/", exam_start, name="exam_start"),
    path("results/", result_list, name="result_list"),
]
