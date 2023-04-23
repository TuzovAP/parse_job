from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from accounts_app.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm

User = get_user_model()


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


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        messages.success(request, 'Пользователь зарегистрирован.')
        return render(request, 'accounts_app/register_done.html',
                      {'new_user': new_user})
    return render(request, 'accounts_app/register.html', {'form': form})



def update_view(request):
    # contact_form = ContactForm()
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.language_programm = data['language_programm']
                user.send_message = data['send_message']
                user.save()
                messages.success(request, 'Данные сохраненны.')
                return redirect('accounts:update')

        form = UserUpdateForm(
            initial={'city': user.city, 'language_programm': user.language_programm,
                     'send_message': user.send_message})
        return render(request, 'accounts_app/update.html',
                      {'form': form,
                       # 'contact_form': contact_form
                       })
    else:
        return redirect('accounts_app:login')


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, 'Пользователь удален :(')
    return redirect('home')
