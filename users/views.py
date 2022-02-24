from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import *
from .models import User


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            account_type = form.cleaned_data.get("account_type")
            if account_type == "S":
                user.is_student = True
            else:
                user.is_teacher = True
            user.save()

            messages.success(
                request, f"Account created for {user.username}. They can now login."
            )
            return redirect("login")
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            messages.success(request, "Profile updated successfully.")
            return redirect("users:profile")
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "users/profile.html", {"form": form})


@login_required
def student_profile(request):
    user = request.user
    if hasattr(user, "student"):
        form = StudentForm(instance=user.student)

    elif request.method == "POST":
        if hasattr(user, "studentrequest"):
            form = StudentRequestForm(request.POST, instance=user.studentrequest)
        else:
            form = StudentRequestForm(request.POST)

        if form.is_valid():
            sr = form.save(commit=False)
            sr.user = user
            sr.save()

            messages.success(request, "Profile updated successfully.")
            return redirect("users:student_profile")
    else:
        if hasattr(user, "studentrequest"):
            form = StudentRequestForm(instance=user.studentrequest)
        else:
            form = StudentRequestForm()

    return render(request, "users/student_profile.html", {"form": form})


@require_POST
@login_required
def student_delete(request):
    student = request.user.student
    student.user = None
    student.save()
    messages.success(request, "Profile deleted successfully.")
    return redirect("users:student_profile")


@login_required
def teacher_profile(request):
    user = request.user
    if hasattr(user, "teacher"):
        form = TeacherForm(instance=user.teacher)

    elif request.method == "POST":
        if hasattr(user, "teacherrequest"):
            form = TeacherRequestForm(request.POST, instance=user.teacherrequest)
        else:
            form = TeacherRequestForm(request.POST)

        if form.is_valid():
            tr = form.save(commit=False)
            tr.user = user
            tr.save()

            messages.success(request, "Profile updated successfully.")
            return redirect("users:teacher_profile")
    else:
        if hasattr(user, "teacherrequest"):
            form = TeacherRequestForm(instance=user.teacherrequest)
        else:
            form = TeacherRequestForm()

    return render(request, "users/teacher_profile.html", {"form": form})


@require_POST
@login_required
def teacher_delete(request):
    request.user.teacher.delete()
    messages.success(request, "Profile deleted successfully.")
    return redirect("users:teacher_profile")


@login_required
def redirect_on_login(request):
    if request.user.is_student:
        if hasattr(request.user, "student"):
            return redirect("students:exams_list")
        else:
            return redirect("users:student_profile")

    elif request.user.is_teacher:
        if hasattr(request.user, "teacher"):
            return redirect("teachers:students_list")
        else:
            return redirect("users:teacher_profile")

    else:
        return redirect("hod:teachers_list")


@require_POST
def demo_login(request):
    user = User.objects.get(pk=1)
    login(request, user)
    return redirect("redirect_on_login")
