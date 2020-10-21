# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from .models import UserProfileInfo
from .models import CustomUser
from django import forms
from django.core.validators import RegexValidator


class CustomUserForm(forms.ModelForm):
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(),)
    email = forms.EmailField(required=True,)
    is_doctor = forms.BooleanField(label="Are you a doctor?")

    class Meta:
        fields = ('email', 'password','is_doctor')
        model = CustomUser
        