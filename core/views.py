from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import ExamForm, MCQForm
from .models import Exam, MCQ

def exams_list(request):

    active_exams = Exam.objects.filter(active=True)
    inactive_exams = Exam.objects.filter(active=False)

    context = {
        'active_exams': active_exams,
        'inactive_exams': inactive_exams
    }

    return render(request, 'core/exams_list.html', context)

@login_required
def exam_create(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)

        if form.is_valid():
            exam = form.save(commit=False)
            exam.user = request.user
            exam.save()

            messages.success(request, 
                f'Exam "{exam}" created successfully.')

            return redirect('exam_detail', pk=exam.pk)
    else:
        form = ExamForm()

    return render(request, 'core/exam_create.html', {'form': form})

@login_required
def exam_detail(request, pk):

    exam = get_object_or_404(Exam, pk=pk)
    if exam.user != request.user:
        raise PermissionDenied()

    return render(request, 'core/exam_detail.html', {'exam': exam})

@login_required
def exam_edit(request, pk):

    exam = get_object_or_404(Exam, pk=pk)
    if exam.user != request.user:
        raise PermissionDenied()

    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)

        if form.is_valid():
            form.save()

            messages.success(request, 
                f'Exam "{exam}" saved successfully.')

            return redirect('exam_detail', pk=exam.pk)
    else:
        form = ExamForm(instance=exam)

    context = {
        'form': form,
        'exam': exam
    }

    return render(request, 'core/exam_edit.html', context)

@require_POST
@login_required
def exam_delete(request, pk):

    exam = get_object_or_404(Exam, pk=pk)
    if exam.user != request.user:
        raise PermissionDenied()

    exam.delete()
    messages.success(request, 'Exam deleted successfully')

    return redirect('exams_list')

@login_required
def mcq_create(request, exam_pk):

    exam = get_object_or_404(Exam, pk=exam_pk)
    if exam.user != request.user:
        raise PermissionDenied()

    if request.method == 'POST':
        form = MCQForm(request.POST)

        if form.is_valid():
            mcq = form.save(commit=False)
            mcq.exam = exam
            mcq.save()

            messages.success(request, 
            f'MCQ "{mcq}" created successfully.')

            return redirect('mcq_create', exam_pk=exam_pk)
    else:
        form = MCQForm()

    return render(request, 'core/mcq_create.html', {'form': form})

@login_required
def mcq_edit(request, pk):

    mcq = get_object_or_404(MCQ, pk=pk)
    if mcq.exam.user != request.user:
        raise PermissionDenied()

    if request.method == 'POST':
        form = MCQForm(request.POST, instance=mcq)

        if form.is_valid():
            form.save()

            messages.success(request, 
                f'MCQ "{mcq}" saved successfully.')

            return redirect('exam_detail', pk=mcq.exam.pk)
    else:
        form = MCQForm(instance=mcq)

    context = {
        'form': form,
        'mcq': mcq
    }

    return render(request, 'core/mcq_edit.html', context)

@require_POST
@login_required
def mcq_delete(request, pk):
    
    mcq = get_object_or_404(MCQ, pk=pk)
    if mcq.exam.user != request.user:
        raise PermissionDenied()

    exam_pk = mcq.exam.pk
    mcq.delete()
    messages.success(request, 'MCQ deleted successfully')

    return redirect('exam_detail', pk=exam_pk)
