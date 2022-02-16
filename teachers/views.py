from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from core.decorators import *
from users.models import Student, StudentRequest

User = get_user_model()


@login_required
@is_verified_teacher
def students_list(request):
    teacher = request.user.teacher
    students = User.objects.filter(
        student__standard=teacher.standard,
        student__branch=teacher.branch,
        student__division=teacher.division,
    )

    return render(request, "teachers/students_list.html", {"students": students})


@login_required
@is_verified_teacher
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    teacher = request.user.teacher
    if (
        student.standard != teacher.standard
        or student.branch != teacher.branch
        or student.division != teacher.division
    ):
        raise PermissionDenied()

    student.delete()
    messages.success(request, "Profile deleted successfully")

    return redirect("teachers:students_list")


@login_required
@is_verified_teacher
def students_request_list(request):
    teacher = request.user.teacher
    students = User.objects.filter(
        studentrequest__standard=teacher.standard,
        studentrequest__branch=teacher.branch,
        studentrequest__division=teacher.division,
    )

    return render(
        request, "teachers/students_request_list.html", {"students": students}
    )


@login_required
@is_verified_teacher
def student_request_accept(request, pk):
    studentrequest = get_object_or_404(StudentRequest, pk=pk)
    teacher = request.user.teacher
    if (
        studentrequest.standard != teacher.standard
        or studentrequest.branch != teacher.branch
        or studentrequest.division != teacher.division
    ):
        raise PermissionDenied()

    if Student.objects.filter(
        standard=studentrequest.standard,
        branch=studentrequest.branch,
        division=studentrequest.division,
        roll_no=studentrequest.roll_no,
    ).exists():
        messages.error(
            request,
            f"Profile with roll number {studentrequest.roll_no} already exists, please delete it first",
        )
    else:
        Student.objects.create(
            user=studentrequest.user,
            standard=studentrequest.standard,
            branch=studentrequest.branch,
            division=studentrequest.division,
            roll_no=studentrequest.roll_no,
        )
        studentrequest.delete()
        messages.success(request, "Profile request accepted")

    return redirect("teachers:students_request_list")
