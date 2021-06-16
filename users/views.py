from csv import DictReader
from io import TextIOWrapper
import random
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from myproject.settings import EMAIL_HOST_USER
from core.decorators import group_required, group_forbidden
from core.models import Session
from .forms import *

def staff_register(request):
    if request.method == 'POST':
        form = StaffRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 
                f'Account created for {username}. They can now login.')
            messages.info(request, 
                'Contact an admin to confirm your account.')

            return redirect('staff_login')
    else:
        form = StaffRegisterForm()

    return render(request, 'users/staff_register.html', {'form': form})

@login_required
@group_required('admin')
def student_mass_register(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data.get('file')
            file = TextIOWrapper(file, encoding='utf-8')
            dict_reader = DictReader(file)

            create_counter = 0
            update_counter = 0
            for row in dict_reader:
                user, created = User.objects.update_or_create(
                    username=row['student id'],
                    defaults={'email': row['email']}
                )

                if created:
                    create_counter += 1
                    group = Group.objects.get(name='student')
                    user.groups.add(group)

                    password = User.objects.make_random_password()
                    user.set_password(password)
                    user.save()

                    subject = 'Username and Password'
                    html = render_to_string(
                        'email/username_and_password.html',
                        {'user': user, 'raw_password': password}
                    )
                    plain = strip_tags(html)
                    from_ = EMAIL_HOST_USER

                    user.email_user(subject, plain, from_, html_message=html)

                else:
                    update_counter += 1

            messages.success(request,
                f'Successfully created {create_counter} user(s).')
            messages.info(request,
                f'Successfully updated {update_counter} user(s).')

            return redirect('student_mass_register')
    else:
        form = StudentRegisterForm()

    return render(request, 'users/student_mass_register.html', {'form': form})

def staff_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            groups = ('admin', 'teacher')
            if not (user.groups.filter(name__in=groups).exists() or
                    user.is_superuser or
                    user.is_staff):
                messages.error(request,
                    'Only confirmed staff can login.')

                return redirect('staff_login')

            login(request, user)
            next_ = request.GET.get("next")

            if next_:
                return redirect(next_)
            
            return redirect('exams_list')

    else:
        form = AuthenticationForm()

    return render(request, 'users/staff_login.html', {'form': form})

def student_login(request):
    if (request.user.is_authenticated and
            request.user.session_set.filter(completed=False).exists()):
        return redirect('exam_start')

    if request.method == 'POST':
        l_form = StudentLoginForm(data=request.POST)
        e_form = ExamChoiceForm(request.POST)

        if l_form.is_valid() and e_form.is_valid():
            user = l_form.get_user()
            if not (user.groups.filter(name='student').exists() or
                    user.is_superuser):
                messages.error(request,
                    'Only confirmed student can login.')

                return redirect('student_login')

            exam = e_form.cleaned_data.get('exam')
            try:
                session = user.session_set.get(completed=False)
                if session.exam != exam:
                    messages.error(request,
                        'Only one exam can be given at a time. '
                        f'Please complete "{session}" first.')

                    return redirect('student_login')

            except ObjectDoesNotExist:
                Session.objects.create(
                    user=user,
                    exam=exam,
                    seed=random.randrange(10000),
                    completed=False
                )

            login(request, user)

            return redirect('exam_start')

    else:
        l_form = StudentLoginForm()
        e_form = ExamChoiceForm()

    context = {
        'l_form': l_form,
        'e_form': e_form,
    }
    return render(request, 'users/student_login.html', context)

@login_required
@group_forbidden('student')
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            messages.success(request, 'Profile updated successfully.')

            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})

@login_required
@group_required('admin')
def users_list(request):
    if request.method == 'POST':
        form = ActionForm(request.POST)
        if form.is_valid():
            queryset = User.objects.filter(
                pk__in=request.POST.getlist('users')
            )
            ACTIONS[form.cleaned_data.get('action')](request, queryset)

            return redirect('users_list')

    else:
        form = ActionForm()

    context = {
        'form': form,
        'users': User.objects.all()
    }
    return render(request, 'users/users_list.html', context)
