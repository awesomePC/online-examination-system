"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from core import views as core_views
from results import views as results_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path(
        "accounts/password-reset/",
        auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
        name="password_reset",
    ),
    path(
        "accounts/password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "accounts/password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "accounts/password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("accounts/", include("users.urls", namespace="users")),
    path("", include("teachers.urls", namespace="teachers")),
    # core
    path("exams-list/", core_views.exams_list, name="exams_list"),
    path("exam-create/", core_views.exam_create, name="exam_create"),
    path("exam/<int:pk>/", core_views.exam_detail, name="exam_detail"),
    path(
        "exam/<int:exam_pk>/question-create/",
        core_views.question_create,
        name="question_create",
    ),
    path("exam-edit/<int:pk>/", core_views.exam_edit, name="exam_edit"),
    path("question-edit/<int:pk>/", core_views.question_edit, name="question_edit"),
    path("exam-delete/<int:pk>/", core_views.exam_delete, name="exam_delete"),
    path(
        "question-delete/<int:pk>/", core_views.question_delete, name="question_delete"
    ),
    path("exam-start/", core_views.exam_start, name="exam_start"),
    path("submit/", core_views.exam_submit, name="exam_submit"),
    path("clear/", core_views.answer_clear, name="answer_clear"),
    path("answer/", core_views.answer_submit, name="answer_submit"),
    path("question-list/", core_views.question_list, name="question_list"),
    path("bookmark/", core_views.bookmark, name="bookmark"),
    # results
    path(
        "exam/<int:exam_pk>/results/", results_views.results_list, name="results_list"
    ),
    path("result/<int:pk>/", results_views.result_detail, name="result_detail"),
    path("results/", results_views.result_all, name="result_all"),
]
