import random
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from core.decorators import *
from core.models import Exam, Session


@login_required
@is_verified_student
def exams_list(request):
    search = request.GET.get("search", None)
    ques = Count("question", filter=Q(question__deleted=None))
    if search:
        exams = Exam.objects.annotate(ques=ques).filter(
            ques__gt=0, active=True, name__icontains=search
        )
    else:
        exams = Exam.objects.annotate(ques=ques).filter(ques__gt=0, active=True)

    paginator = Paginator(exams, 15)
    page = request.GET.get("page")
    try:
        exams = paginator.page(page)
    except PageNotAnInteger:
        exams = paginator.page(1)
    except EmptyPage:
        exams = paginator.page(paginator.num_pages)

    return render(request, "students/exams_list.html", {"exams": exams})


@require_POST
@login_required
@is_verified_student
def exam_start(request, pk):
    exam = get_object_or_404(Exam, pk=pk)

    if request.user.session_set.filter(exam=exam, completed=True).exists():
        messages.error(request, "An exam can only be taken once.")
        return redirect("students:exams_list")

    if not request.user.session_set.filter(exam=exam, completed=False).exists():
        if not exam.question_set.filter(deleted=None).exists():
            raise PermissionDenied()

        Session.objects.create(
            user=request.user,
            student=request.user.student,
            exam=exam,
            seed=random.randrange(10000),
        )

    return redirect("exam_start", exam_pk=pk)


@login_required
@is_verified_student
def result_list(request):
    search = request.GET.get("search", None)
    if search:
        sessions = request.user.session_set.filter(
            completed=True, exam__show_result=True, exam__name__icontains=search
        )
    else:
        sessions = request.user.session_set.filter(
            completed=True, exam__show_result=True
        )

    paginator = Paginator(sessions, 15)
    page = request.GET.get("page")
    try:
        sessions = paginator.page(page)
    except PageNotAnInteger:
        sessions = paginator.page(1)
    except EmptyPage:
        sessions = paginator.page(paginator.num_pages)

    return render(request, "students/result_list.html", {"sessions": sessions})


@login_required
@is_verified_student
def result_detail(request, pk):
    session = get_object_or_404(Session, pk=pk, completed=True)
    if session.user != request.user or not session.exam.show_result:
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
    return render(request, "students/result_detail.html", context)
