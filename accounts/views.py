from .models import *
from .decorators import *
from .forms import *

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

from django.contrib.auth.models import Group
def user_signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    else:
        registered = False
        if request.method == 'POST':
            if request.POST.get('is_doctor'):
                user_form = DoctorForm(data=request.POST)
            else:
                user_form = PatientForm(data=request.POST)

            if user_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user.password)
                user.save()

                if request.POST.get('is_doctor'):
                    my_group = Group.objects.get(name='Doctors') 
                    my_group.user_set.add(user)
                else:
                    my_group = Group.objects.get(name='Patients')
                    my_group.user_set.add(user)
                welcome_email(user.email)

                registered = True
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, 'accounts/signup.html',
                              {'user_form': user_form,
                               'registered': registered})
        else:
            if request.POST.get('is_doctor'):
                user_form = DoctorForm()
            else:
                user_form = PatientForm()
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

class see_public_profile(DetailView):
    model = Doctor
    template_name = 'accounts/see_public_profile.html'
    context_object_name = 'fields'
    def get_object(self, queryset=None):
        queryset = Doctor.objects.get(id=self.kwargs.get('pk'))
        return queryset

def profile(request):
    context = {}
    if request.user.is_authenticated:
        queryset = get_user_type(request.user).objects.filter(customuser_ptr_id=request.user.id)
        # context['allergies'] = queryset.get().allergies
        context['fields'] = queryset.get()
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
from django.shortcuts import get_object_or_404
from accounts.forms import *

class user_update( UpdateView):
    model = Patient
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('accounts:profile')
    form_class = UpdateViewForm
    # def get_context_data(self, **kwargs):
    #     return super().get_context_data(**kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = Patient.objects.filter(customuser_ptr_id=user.id)
        return queryset
    
    def get_object(self):
        user = self.request.user
        return get_object_or_404(Patient, id=user.id)

class doctor_user_update( UpdateView):
    model = Doctor
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('accounts:profile')
    form_class = DoctorUpdateViewForm
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = Doctor.objects.filter(customuser_ptr_id=user.id)
        return queryset

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Doctor, id=user.id)

class list_doctors(ListView):
    model = Doctor
    template_name = 'accounts/list_doctors.html'
    context_object_name = 'doctors'

from django.views.generic.edit import FormView
class make_appointment(PermissionRequiredMixin, CreateView):
    permission_required = 'accounts.add_appointment'

    form_class = make_appointment_form
    template_name = 'accounts/make_appointment.html'
    success_url = reverse_lazy('accounts:past_appointment')

    # def get_initial(self):
    #     return super().get_initial()

    def get_form_kwargs(self):
        s = super().get_form_kwargs()
        if self.kwargs.get('id'):
            # print(self.kwargs.get('id'))
            # print(super().get_form_kwargs())
            s['initial']['doctor'] = Doctor.objects.get(id=self.kwargs.get('id'))
        return s

    def form_valid(self, form):
        print('\n\n\n\nin form_valid')
        form.instance.patient = Patient.objects.filter(customuser_ptr_id=self.request.user.id).get()
        return super().form_valid(form)

class see_schedule(PermissionRequiredMixin, ListView):
    permission_required = 'accounts.view_appointment'

    model = Appointment
    template_name = 'accounts/doctor_schedule.html'
    context_object_name = 'schedule'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Appointment.objects.filter(doctor=self.request.user)
        return queryset

from django.core.exceptions import PermissionDenied
def detail_appointment(request,pk):
    query = Appointment.objects.get(id=pk)
    if request.method=='GET':
        context = {}
        context['day1'] = query.day1
        context['day2'] = query.day2
        context['day3'] = query.day3
        context['message'] = query.message

        if str(request.user)==str(query.doctor):
            context['patient'] = query.patient
            if query.approved_for == None:
                form = approve_appointment(instance=query)
                context['form'] = form
            else:
                context['approved_for'] = query.day1 if query.approved_for==1 else query.day2 if query.approved_for==2 else query.day3
                context['approved_time'] = query.approved_time
                if query.prescription == None:
                    form = write_prescription_form(instance=query)
                    context['form'] = form
                else:
                    context['prescription'] = query.prescription
            return render(request,'accounts/doctor_appointment_view.html',context=context)
        elif str(request.user) == str(query.patient):
            context['doctor'] = query.doctor
            if not query.approved_for == None:
                context['approved_for'] = query.day1 if query.approved_for==1 else query.day2 if query.approved_for==2 else query.day3
                context['approved_time'] = query.approved_time
            if not query.prescription == None:
                context['prescription'] = query.prescription
            return render(request,'accounts/appointment_view.html',context=context)
        else:
            raise PermissionDenied

    else:
        if query.approved_for:
            query.prescription = request.POST.get('prescription')
            query.save()
            return redirect('accounts:detail_appointment', pk=query.id)
        else:
            query.approved_for=request.POST.get('approved_for')
            query.approved_time=request.POST.get('approved_time')
            query.save()
            return redirect('accounts:see_schedule')

class past_appointment(ListView):
    # permission_required = 'accounts.view_appointment'

    model = Appointment
    template_name = 'accounts/past_appointments.html'
    context_object_name = 'past'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Appointment.objects.filter(patient=self.request.user)
        print(queryset)
        return queryset

def predict_heart_disease(request):
    if request.method == 'POST':
        form = heart_disease_predict_form()
        age=request.POST.get("age")
        gender=request.POST.get("gender")
        cp=request.POST.get("cp")
        trestbps=request.POST.get("trestbps")
        chol=request.POST.get("chol")
        fbs=request.POST.get("fbs")
        restecg=request.POST.get("restecg")
        lach=request.POST.get("lach")
        exang=request.POST.get("exang")
        oldpeak=request.POST.get("oldpeak")
        slope=request.POST.get("slope")
        ca=request.POST.get("ca")
        thal=request.POST.get("thal")
        import pickle
        model = pickle.load(open('./ML/LogisticRegression.pkl','rb'))
        pred = model.predict([[int(age),int(gender),float(cp),int(trestbps),int(chol),int(fbs),int(restecg),int(lach),int(exang),float(oldpeak),int(slope),int(ca),int(thal)]])
        
        if pred == 0 :
            print("Patient has a heart problem")
        else:
            print("Patient is healthy")

    return render(request,'accounts/heart_disease_predict.html')

def diabetes_predict(request):
    if request.method == 'POST':
        pregnancies=request.POST.get("pregnancies")
        glucose=request.POST.get("glucose")
        bp=request.POST.get("bp")
        skin_thickness=request.POST.get("skin_thickness")
        insulin=request.POST.get("insulin")
        bmi=request.POST.get("bmi")
        dpf=request.POST.get("dpf")
        age=request.POST.get("age")

        import pickle
        model = pickle.load(open('./ML/Random_Forest.pkl','rb'))
        pred = model.predict([[int(pregnancies),int(glucose),float(bp),int(skin_thickness),int(insulin),float(bmi),float(dpf),int(age)]])

        if pred == 1 :
            print("Patient has Diabetes")
        else:
            print("Patient is healthy")
    return render(request, 'accounts/predict_diabetes.html')
