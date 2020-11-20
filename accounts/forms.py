# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from .models import UserProfileInfo
from accounts.models import Appointment
from django.forms.widgets import DateInput, SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from accounts.models import *
from django.forms.fields import *
from .models import *
from django import forms
from django.core.validators import RegexValidator


class PatientForm(forms.ModelForm):
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(),)
    email = forms.EmailField(required=True,)
    is_doctor = forms.BooleanField(required=False, label="Are you a doctor?")

    class Meta:
        fields = ('email', 'password', 'is_doctor')
        model = Patient

class DoctorForm(forms.ModelForm):
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(),)
    email = forms.EmailField(required=True,)
    is_doctor = forms.BooleanField(required=False, label="Are you a doctor?")

    class Meta:
        fields = ('email', 'password', 'is_doctor')
        model = Doctor

# class PatientForm(forms.ModelForm):

#     class Meta:
#         model = Patient


# class DateInput(forms.DateInput):
#     input_type = 'date'


class UpdateViewForm(forms.ModelForm):
    date_of_birth = DateField(widget=AdminDateWidget(attrs={'placeholder': 'YYYY:MM:DD'}))

    class Meta:
        model = Patient
        fields = ('fullname', 'date_of_birth', 'phone_number', 'blood_group', 'allergies', 'marital_status', 'emergency_Name',
                  'emergency_phone_number', 'emergency_relationship', 'insurance_id', 'insurance_company', 'insurance_validity')
        # widgets = {
        #     'date_of_birth': AdminDateWidget(),
        # }

class DoctorUpdateViewForm(forms.ModelForm):
    date_of_birth = DateField(widget=AdminDateWidget(attrs={'placeholder': 'YYYY:MM:DD'}))

    class Meta:
        model = Doctor
        fields = ('fullname', 'date_of_birth', 'speciality', 'college', 'experience_years',)
        # widgets = {
        #     'date_of_birth': AdminDateWidget(),
        # }

class make_appointment_form(forms.ModelForm):
    day1 = DateField(widget=AdminDateWidget(attrs={'placeholder': 'YYYY:MM:DD'}))
    day2 = DateField(widget=AdminDateWidget(attrs={'placeholder': 'YYYY:MM:DD'}))
    day3 = DateField(widget=AdminDateWidget(attrs={'placeholder': 'YYYY:MM:DD'}))
    # patient = forms.CharField(widget=forms.HiddenInput())
    # message = CharField(widget=forms.Textarea)

    class Meta:
        model = Appointment
        fields = ('doctor', 'day1', 'day2', 'day3','message')  # 'patient')
        
        widgets = {
          'message': forms.Textarea(attrs={'rows':4, 'cols':60}),
        }


# class approve_appointment(forms.ModelForm):
#     day1 = DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
#     day2 = DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
#     day3 = DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
#     patient = CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
#     message = CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    
#     approved_for = forms.ChoiceField(choices=(
#         ('1', 'day 1'), ('2', 'day 2'), ('3', 'day 3'),), label="Approved for day: ")

#     class Meta:
#         model = Appointment
#         fields = ('approved_for',)#'patient', 'day1', 'day2', 'day3','message')
#         widget={'message':forms.Textarea()}


class approve_appointment(forms.ModelForm):
    # day1 = DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # day2 = DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # day3 = DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # patient = CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # message = CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    approved_time = CharField(widget=AdminTimeWidget(attrs={'placeholder': 'hh:mm XM'}))
    approved_for = forms.ChoiceField(choices=(
        ('1', 'day 1'), ('2', 'day 2'), ('3', 'day 3'),), label="Approved for day: ")

    # def __init__(self, ap_id, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList, label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None, renderer=None):
    #     super().__init__(data=data, files=files, auto_id=auto_id, prefix=prefix, initial=initial, error_class=error_class, label_suffix=label_suffix, empty_permitted=empty_permitted, instance=instance, use_required_attribute=use_required_attribute, renderer=renderer)
    # def __init__(self, ap_id, *args, **kwargs):
    #     approved_for = forms.ModelChoiceField(ap_id)
    #     accountid = kwargs.pop('accountid', None)
    #     super(approve_appointment, self).__init__(*args, **kwargs)

    class Meta:
        model = Appointment
        fields = ('approved_for','approved_time')
        # widget={'message':forms.Textarea()}

class write_prescription_form(forms.ModelForm):
    prescription = CharField(widget=forms.Textarea(attrs={'placeholder': 'Prescription '}))
    class Meta:
        model = Appointment
        fields = ('prescription',)


# [[int(pregnancies),int(glucose),float(bp),int(skin_thickness),int(insulin),float(bmi),float(dpf),int(age)]]
class heart_disease_predict_form(forms.Form):
    pregnancies = forms.IntegerField()
    glucose = forms.IntegerField()
    bp = forms.FloatField()
    skin_thickness = forms.IntegerField()
    insulin = forms.IntegerField()
    bmi = forms.FloatField()
    dpf = forms.FloatField()
    age = forms.IntegerField()

# [[int(age),int(gender),float(cp),int(trestbps),int(chol),int(fbs),int(restecg),int(lach),int(exang),float(oldpeak),int(slope),int(ca),int(thal)]]
class diabetes_predict_form(forms.Form):
    age = forms.IntegerField()
    gender = forms.IntegerField()
    cp = forms.FloatField()
    trestbps = forms.IntegerField()
    chol = forms.IntegerField()
    fbs = forms.IntegerField()
    restecg = forms.IntegerField()
    lach = forms.IntegerField()
    exang = forms.IntegerField()
    oldpeak = forms.FloatField()
    slope = forms.IntegerField()
    ca = forms.IntegerField()
    thal = forms.IntegerField()