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
from django.urls import path
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.exams_list, name='exams_list'),
    path('exam-create/', core_views.exam_create, name='exam_create'),
    path('exam/<int:pk>/', core_views.exam_detail, name='exam_detail'),
    path('exam/<int:exam_pk>/question-create/',
        core_views.question_create,
        name='question_create'),
    path('exam-edit/<int:pk>/', core_views.exam_edit, name='exam_edit'),
    path('question-edit/<int:pk>/',
        core_views.question_edit,
        name='question_edit'),
    path('exam-delete/<int:pk>/', core_views.exam_delete, name='exam_delete'),
    path('question-delete/<int:pk>/',
        core_views.question_delete,
        name='question_delete'),
    path('exam-participate/<int:pk>/',
        core_views.exam_participate,
        name='exam_participate'),
    path('exam-start/<int:pk>/', core_views.exam_start, name='exam_start'),
    path('exam-start/<int:pk>/submit/',
        core_views.exam_submit,
        name='exam_submit'),
    path('exam-start/<int:exam_pk>/clear/',
        core_views.answer_clear,
        name='answer_clear'),
    path('exam-start/<int:exam_pk>/answer/',
        core_views.answer_submit,
        name='answer_submit'),
    path('exam-start/<int:pk>/question-list/',
        core_views.question_list,
        name='question_list'),
    path('exam-start/<int:pk>/bookmark/',
        core_views.bookmark,
        name='bookmark'),
]
