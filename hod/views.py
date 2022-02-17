from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from core.decorators import *
from users.models import Teacher, TeacherRequest

User = get_user_model()


@login_required
@is_hod
def teachers_list(request):
    teachers = User.objects.exclude(teacher=None)
    return render(request, "hod/teachers_list.html", {"teachers": teachers})


@login_required
@is_hod
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.delete()
    messages.success(request, "Profile deleted successfully")

    return redirect("hod:teachers_list")


@login_required
@is_hod
def teachers_request_list(request):
    teachers = User.objects.exclude(teacherrequest=None)
    return render(request, "hod/teachers_request_list.html", {"teachers": teachers})


@login_required
@is_hod
def teacher_request_accept(request, pk):
    teacherrequest = get_object_or_404(TeacherRequest, pk=pk)

    if Teacher.objects.filter(
        standard=teacherrequest.standard,
        branch=teacherrequest.branch,
        division=teacherrequest.division,
    ).exists():
        messages.error(
            request,
            "Teacher to this class is already assigned, please delete their profile first",
        )
    else:
        Teacher.objects.create(
            user=teacherrequest.user,
            standard=teacherrequest.standard,
            branch=teacherrequest.branch,
            division=teacherrequest.division,
        )
        teacherrequest.delete()
        messages.success(request, "Profile request accepted")

    return redirect("hod:teachers_request_list")
