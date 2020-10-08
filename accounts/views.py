from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin)
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .forms import CustomUserForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))


def user_signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    else:
        registered = False
        if request.method == 'POST':
            user_form = CustomUserForm(data=request.POST)

            if user_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user.password)
                user.save()

                registered = True
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, 'accounts/signup.html',
                              {'user_form': user_form,
                               'registered': registered})
        else:
            user_form = CustomUserForm()
            return render(request, 'accounts/signup.html',
                          {'user_form': user_form,
                           'registered': registered})


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    else:
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)
            print(request.POST)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    return HttpResponse('user not active! [accounts/views.py]')
            else:
                return HttpResponse('Email and password not valid! [accounts/views.py]')
        else:
            return render(request, 'accounts/login.html')

def profile(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/profile.html')
    else:
        return HttpResponseRedirect(reverse('accounts:login'))