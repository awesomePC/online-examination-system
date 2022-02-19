import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from core.decorators import *
from core.models import Exam, Session


@login_required
@is_verified_student
def exams_list(request):
    exams = Exam.objects.filter(active=True)
    return render(request, "students/exams_list.html", {"exams": exams})


@require_POST
@login_required
@is_verified_student
def exam_start(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if not Session.objects.filter(
        user=request.user, exam=exam, completed=False
    ).exists():
        Session.objects.create(
            user=request.user,
            exam=exam,
            seed=random.randrange(10000),
        )

    return redirect("exam_start", exam_pk=pk)
