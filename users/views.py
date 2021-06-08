from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StaffRegisterForm

def staff_register(request):
    if request.method == 'POST':
        form = StaffRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 
                f'Account created for {username}. They can now login.')

            return redirect('staff_login')
    else:
        form = StaffRegisterForm()

    return render(request, 'users/staff_register.html', {'form': form})
