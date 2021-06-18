from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from core.decorators import group_required
from core.models import Exam, Session
from .forms import ResultForm

@login_required
@group_required('admin', 'teacher')
def results_list(request, exam_pk):
    exam = get_object_or_404(Exam, pk=exam_pk)
    if exam.user != request.user:
        raise PermissionDenied()

    sessions = (exam.session_set.filter(completed=True)
        .order_by('user__username'))
    context = {
        'exam': exam,
        'sessions': sessions
    }
    return render(request, 'results/results_list.html', context)

@login_required
@group_required('admin', 'teacher')
def result_detail(request, pk):
    session = get_object_or_404(Session, pk=pk, completed=True)
    if session.exam.user != request.user:
        raise PermissionDenied()

    context = {
        'session': session,
        'answers': session.answer_set.all().order_by('question__created')
    }
    return render(request, 'results/result_detail.html', context)

def result_all(request):
    if request.method == 'POST':
        form = ResultForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            context = {
                'username': username,
                'sessions': (Session.objects
                    .filter(user__username=username, completed=True)
                    .order_by('-submitted'))
            }
            return render(request, 'results/result_all.html', context)
    else:
        form = ResultForm()

    return render(request, 'results/result_all_form.html', {'form': form})
