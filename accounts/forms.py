# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from .models import UserProfileInfo
from .models import *
from django import forms
from django.core.validators import RegexValidator


class CustomUserForm(forms.ModelForm):
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(),)
    email = forms.EmailField(required=True,)
    is_doctor = forms.BooleanField(required=False, label="Are you a doctor?")

    class Meta:
        fields = ('email', 'password', 'is_doctor')
        model = CustomUser

# class PatientForm(forms.ModelForm):

#     class Meta:
#         model = Patient

class DateInput(forms.DateInput):
    input_type = 'date'

from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import *
from django.forms.widgets import DateInput,SelectDateWidget
from accounts.models import *
class UpdateViewForm(forms.ModelForm):
    date_of_birth = DateField(widget=AdminDateWidget)
    class Meta:
        model = Patient
        fields = ('fullname','date_of_birth', 'phone_number', 'blood_group', 'allergies', 'marital_status', 'emergency_Name',
                  'emergency_phone_number', 'emergency_relationship', 'insurance_id', 'insurance_company', 'insurance_validity')
        # widgets = {
        #     'date_of_birth': AdminDateWidget(),
        # }

class make_appointment_form(forms.ModelForm):
    day1 = DateField(widget=AdminDateWidget)
    day2 = DateField(widget=AdminDateWidget)
    day3 = DateField(widget=AdminDateWidget)
    patient = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = Appointment
        fields = ('doctor','day1','day2','day3','patient')