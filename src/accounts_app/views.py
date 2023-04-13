from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from accounts_app.forms import UserLoginForm


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts_app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
