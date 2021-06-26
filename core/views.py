import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import JsonResponse, Http404
from django.utils import timezone
from django.views.decorators.http import require_POST
from .decorators import group_required
from .forms import ExamForm, QuestionForm
from .models import Exam, Question, Answer, Session

@login_required
@group_required('admin', 'teacher')
def exams_list(request):
    exams = request.user.exam_set.all().order_by('-created')
    return render(request, 'core/exams_list.html', {'exams': exams})

@login_required
@group_required('admin', 'teacher')
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
@group_required('admin', 'teacher')
def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if exam.user != request.user:
        raise PermissionDenied()

    context = {
        'exam': exam,
        'questions': exam.question_set.filter(deleted=None)
    }
    return render(request, 'core/exam_detail.html', context)

@login_required
@group_required('admin', 'teacher')
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
        'exam_pk': exam.pk
    }
    return render(request, 'core/exam_edit.html', context)

@require_POST
@login_required
@group_required('admin', 'teacher')
def exam_delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if exam.user != request.user:
        raise PermissionDenied()

    exam.delete()
    messages.success(request, 'Exam deleted successfully')

    return redirect('exams_list')

@login_required
@group_required('admin', 'teacher')
def question_create(request, exam_pk):
    exam = get_object_or_404(Exam, pk=exam_pk)
    if exam.user != request.user:
        raise PermissionDenied()

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.exam = exam
            question.save()

            messages.success(request, 
            f'Question "{question}" created successfully.')

            return redirect('question_create', exam_pk=exam_pk)
    else:
        form = QuestionForm()

    context = {
        'form': form,
        'exam_pk': exam_pk
    }
    return render(request, 'core/question_create.html', context)

@login_required
@group_required('admin', 'teacher')
def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if question.exam.user != request.user:
        raise PermissionDenied()

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()

            messages.success(request, 
                f'Question "{question}" saved successfully.')

            return redirect('exam_detail', pk=question.exam.pk)
    else:
        form = QuestionForm(instance=question)

    context = {
        'form': form,
        'question_pk': question.pk,
        'exam_pk': question.exam.pk
    }
    return render(request, 'core/question_edit.html', context)

@require_POST
@login_required
@group_required('admin', 'teacher')
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if question.exam.user != request.user:
        raise PermissionDenied()

    exam = question.exam
    if (Session.objects.filter(exam=exam, created__gt=question.created)
            .exists()):
        question.deleted = timezone.now()
        question.save()
    else:
        question.delete()

    messages.success(request, 'Question deleted successfully')
    return redirect('exam_detail', pk=exam.pk)

@group_required('student')
def exam_start(request):
    session = get_object_or_404(
        Session,
        user=request.user,
        completed=False
    )
    questions = session.get_questions()

    if len(questions) == 0:
        raise Http404()

    # send question on ajax
    if request.is_ajax():
        q_num = int(request.GET.get('question'))
        question = questions[q_num-1]

        try:
            answer = Answer.objects.get(session=session, question=question)
            answer = answer.answer
        except ObjectDoesNotExist:
            answer = None

        prev_q_num = q_num-1 if q_num > 1 else None
        next_q_num = q_num+1 if q_num < len(questions) else None

        return JsonResponse({
            'q_num': q_num,
            'prev_q_num': prev_q_num,
            'next_q_num': next_q_num,
            'question': question.question,
            'option_A': question.option_A,
            'option_B': question.option_B,
            'option_C': question.option_C,
            'option_D': question.option_D,
            'answer': answer,
            'marks_on_correct_answer': question.marks_on_correct_answer,
            'marks_on_wrong_answer': question.marks_on_wrong_answer,
        })

    context = {
        'session': session,
        'timestamp':  session.get_timeover_timestamp() * 1000,
        'duration': session.exam.duration.total_seconds() * 1000,
    }
    return render(request, 'core/exam_start.html', context)

@require_POST
@group_required('student')
def exam_submit(request):
    session = get_object_or_404(
        Session,
        user=request.user,
        completed=False
    )
    session.completed = True
    session.submitted = timezone.now()
    session.save()

    logout(request)

    return render(request, 'core/submit.html', {'session': session})

@require_POST
@group_required('student')
def answer_clear(request):
    session = get_object_or_404(
        Session,
        user=request.user,
        completed=False
    )
    if timezone.now().timestamp() > session.get_timeover_timestamp():
        raise PermissionDenied()
    questions = session.get_questions()

    q_num = int(request.POST.get('q_num'))
    question = questions[q_num-1]

    Answer.objects.get(session=session, question=question).delete()

    return JsonResponse({
        'status': 'ok',
        'message': 'Answer cleared.'
    })

@require_POST
@group_required('student')
def answer_submit(request):
    session = get_object_or_404(
        Session,
        user=request.user,
        completed=False
    )
    if timezone.now().timestamp() > session.get_timeover_timestamp():
        raise PermissionDenied()
    questions = session.get_questions()
    q_num = int(request.POST.get('q_num'))
    ans = request.POST.get('answer')
    question = questions[q_num-1]

    Answer.objects.update_or_create(
        session=session,
        question=question,
        defaults={'answer': ans}
    )

    return JsonResponse({
        'status': 'ok',
        'message': f'Answer "{ans}" saved.'
    })

@group_required('student')
def question_list(request):
    session = get_object_or_404(
        Session,
        user=request.user,
        completed=False
    )
    questions = session.get_questions()

    data = []
    for question in questions:
        try:
            answer = Answer.objects.get(session=session, question=question)
            answer = answer.answer
        except ObjectDoesNotExist:
            answer = None

        if session.bookmarks.filter(id=question.id).exists():
            bookmark = True
        else:
            bookmark = False

        data.append({
            'answer': answer,
            'bookmark': bookmark
        })

    return JsonResponse({
        'questions': data
    })

@require_POST
@group_required('student')
def bookmark(request):
    session = get_object_or_404(
        Session,
        user=request.user,
        completed=False
    )
    questions = session.get_questions()
    q_num = int(request.POST.get('q_num'))
    question = questions[q_num-1]

    if session.bookmarks.filter(id=question.id).exists():
        session.bookmarks.remove(question)
        msg = 'Bookmark removed.'
    else:
        session.bookmarks.add(question)
        msg = 'Bookmark added.'

    return JsonResponse({
        'status': 'ok',
        'message': msg
    })