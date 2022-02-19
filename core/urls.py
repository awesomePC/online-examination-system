from django.urls import path
from .views import *

urlpatterns = [
    path("teachers/exams/", exams_list, name="exams_list"),
    path("teachers/exams/create/", exam_create, name="exam_create"),
    path("teachers/exams/<int:pk>/", exam_detail, name="exam_detail"),
    path("teachers/exams/<int:pk>/edit/", exam_edit, name="exam_edit"),
    path("teachers/exams/<int:pk>/delete/", exam_delete, name="exam_delete"),
    path(
        "teachers/exams/<int:exam_pk>/question-create/",
        question_create,
        name="question_create",
    ),
    path(
        "teachers/questions/<int:pk>/edit/",
        question_edit,
        name="question_edit",
    ),
    path(
        "teachers/questions/<int:pk>/delete/",
        question_delete,
        name="question_delete",
    ),
    path("students/exams/<int:exam_pk>/", exam_start, name="exam_start"),
    path(
        "students/exams/<int:exam_pk>/submit/",
        exam_submit,
        name="exam_submit",
    ),
    path(
        "students/exams/<int:exam_pk>/clear/",
        answer_clear,
        name="answer_clear",
    ),
    path(
        "students/exams/<int:exam_pk>/answer/",
        answer_submit,
        name="answer_submit",
    ),
    path(
        "students/exams/<int:exam_pk>/question-list/",
        question_list,
        name="question_list",
    ),
    path("students/exams/<int:exam_pk>/bookmark/", bookmark, name="bookmark"),
]
