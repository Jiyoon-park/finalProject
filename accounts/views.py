from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        messages.warning(request, '로그인된 상태입니다. 로그아웃 후 이용해주세요😉')
        return redirect('movies:index')
    else:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, '축하합니다! 성공적으로 가입되었습니다😉')
                return redirect('accounts:login')
        else:
            form = CustomUserCreationForm()
        context = {
            'form' : form
        }
        return render(request, 'accounts/signup.html', context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, '깜빡하셨군요? 이미 로그인하신 상태입니다😉')
        return redirect('movies:index')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                auth_login(request, form.get_user())
                return redirect('movies:index')
        else:
            form = AuthenticationForm()
        context = {
            'form' : form
        }
        return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('movies:index')