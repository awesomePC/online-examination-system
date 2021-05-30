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
    path('exam/<int:exam_pk>/mcq-create/', core_views.mcq_create, name='mcq_create'),
    path('exam-edit/<int:pk>/', core_views.exam_edit, name='exam_edit'),
    path('mcq-edit/<int:pk>/', core_views.mcq_edit, name='mcq_edit'),
    path('exam-delete/<int:pk>/', core_views.exam_delete, name='exam_delete'),
    path('mcq-delete/<int:pk>/', core_views.mcq_delete, name='mcq_delete'),
]
