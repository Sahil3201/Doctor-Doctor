from .decorators import *
from .forms import CustomUserForm

from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin)
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView, ListView, CreateView

def get_user_type(user):
    if user.is_doctor == True:
        return Doctor
    else:
        return Patient

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
                welcome_email(user.email)

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
    context = {}
    print(request)
    if request.user.is_authenticated:
        queryset = get_user_type(request.user).objects.filter(customuser_ptr_id=request.user.id)
        # context['allergies'] = queryset.get().allergies
        context['fields'] = queryset.get()
        print(context['fields'].allergies)
        return render(request, 'accounts/profile.html',context)
    else:
        return HttpResponseRedirect(reverse('accounts:login'))

# Email
from DoctorDoctor.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
def welcome_email(email):
    subject = 'Verify your DoctorDoctor account'
    message = 'Hope you are enjoying your Django Tutorials'
    html_message = render_to_string('accounts/mail_template.html', {'email': email})
    recepient = email
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False,html_message=html_message)
    return HttpResponseRedirect(reverse('home'))


from django.views.generic.edit import UpdateView
from .models import *
from django.shortcuts import get_object_or_404
from accounts.forms import *

class user_update(UpdateView, PermissionRequiredMixin):
    # permission_required = 'polls.add_choice'
    
    model = Patient
    template_name = 'DoctorDoctor/profile_update.html'
    success_url = reverse_lazy('accounts:profile')
    form_class = UpdateViewForm
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = Patient.objects.filter(customuser_ptr_id=user.id)
        return queryset
    
    def get_object(self):
        user = self.request.user
        return get_object_or_404(Patient, id=user.id)#pk=self.request.session['user_id'])

class active_appointments(ListView):
    model = Appointment
    context_object_name = 'appointments'

class list_doctors(ListView):
    model = Doctor
    template_name = 'accounts/list_doctors.html'
    context_object_name = 'doctors'

from django.views.generic.edit import FormView
class make_appointment(PermissionRequiredMixin, CreateView):
    permission_required = 'accounts.add_appointment'

    # success_url = reverse('accounts:active_appointments')
    form_class = make_appointment_form
    template_name = 'accounts/make_appointment.html'
    success_url = reverse_lazy('accounts:active_appointments')

    def form_valid(self, form):
        print('\n\n\n\nin form_valid')
        form.instance.patient = Patient.objects.filter(customuser_ptr_id=self.request.user.id).get()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form)
        return super().form_invalid(form)

class see_schedule(PermissionRequiredMixin, ListView):
    permission_required = 'accounts.view_appointment'

    model = Appointment
    template_name = 'accounts/doctor_schedule.html'
    context_object_name = 'schedule'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Appointment.objects.filter(doctor=self.request.user)
        return queryset

class detail_appointment(PermissionRequiredMixin, UpdateView):
    permission_required = 'accounts.view_appointment'

    model = Appointment
    form_class = approve_appointment
    template_name = 'accounts/doctor_appointment_view.html'
    context_object_name = 'ap'