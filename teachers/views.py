from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from core.decorators import *
from core.models import Exam, Session
from users.models import Student, StudentRequest

User = get_user_model()


@login_required
@is_verified_teacher
def students_list(request):
    teacher = request.user.teacher
    search = request.GET.get("search", None)
    if search:
        students = User.objects.filter(
            student__standard=teacher.standard,
            student__branch=teacher.branch,
            student__division=teacher.division,
        ).filter(Q(username__icontains=search) | Q(email__icontains=search))
    else:
        students = User.objects.filter(
            student__standard=teacher.standard,
            student__branch=teacher.branch,
            student__division=teacher.division,
        )

    paginator = Paginator(students, 15)
    page = request.GET.get("page")
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    return render(request, "teachers/students_list.html", {"students": students})


@require_POST
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
    search = request.GET.get("search", None)
    if search:
        students = User.objects.filter(
            studentrequest__standard=teacher.standard,
            studentrequest__branch=teacher.branch,
            studentrequest__division=teacher.division,
        ).filter(Q(username__icontains=search) | Q(email__icontains=search))
    else:
        students = User.objects.filter(
            studentrequest__standard=teacher.standard,
            studentrequest__branch=teacher.branch,
            studentrequest__division=teacher.division,
        )

    paginator = Paginator(students, 15)
    page = request.GET.get("page")
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    return render(
        request, "teachers/students_request_list.html", {"students": students}
    )


@require_POST
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


@login_required
@is_verified_teacher
def result_list(request, exam_pk):
    exam = get_object_or_404(Exam, pk=exam_pk)
    if exam.user != request.user:
        raise PermissionDenied()
    sessions = exam.session_set.filter(completed=True)

    paginator = Paginator(sessions, 15)
    page = request.GET.get("page")
    try:
        sessions = paginator.page(page)
    except PageNotAnInteger:
        sessions = paginator.page(1)
    except EmptyPage:
        sessions = paginator.page(paginator.num_pages)

    context = {
        "exam": exam,
        "sessions": sessions,
    }
    return render(request, "teachers/result_list.html", context)


@login_required
@is_verified_teacher
def result_detail(request, pk):
    session = get_object_or_404(Session, pk=pk, completed=True)
    if session.exam.user != request.user:
        raise PermissionDenied()

    search = request.GET.get("search", None)
    if search:
        answers = session.answer_set.filter(
            question__question__icontains=search
        ).order_by("question__created")
    else:
        answers = session.answer_set.all().order_by("question__created")

    paginator = Paginator(answers, 15)
    page = request.GET.get("page")
    try:
        answers = paginator.page(page)
    except PageNotAnInteger:
        answers = paginator.page(1)
    except EmptyPage:
        answers = paginator.page(paginator.num_pages)

    context = {"session": session, "answers": answers}
    return render(request, "teachers/result_detail.html", context)
