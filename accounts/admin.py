from django.contrib import admin
from .models import CustomUser
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import *

class CustomUserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label = 'Password',widget = forms.PasswordInput)
	password2 = forms.CharField(label = 'Password Confirmation',
		widget = forms.PasswordInput)

	class Meta:
		model = CustomUser
		fields = ('email','password')

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError('Passwords dont match')
		return password2

	def save(self,commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user


class CustomUserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField(help_text=("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"../password/\">this form</a>."))

	class Meta:
		model = CustomUser
		fields = ('email','fullname',)

	def clean_password(self):
		return self.initial['password']

class CustomUserAdmin(BaseUserAdmin):
	form = CustomUserChangeForm
	add_form = CustomUserCreationForm

	list_display = ('email','fullname','date_created')
	list_filter = ('is_admin',)

	fieldsets = (
		(None,{'fields': ('email','password')}),
		('Personal info',{'fields':('fullname',)}),
		('Other info',{'fields':('is_doctor',)}),
		('Permissions',{'fields':('is_admin','is_active','is_staff'),}),
		)

	add_fieldsets = (
		(None, {
			# 'classes': ('wide'),
			'fields':('email','password1','password2'),
			}),
		)

	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()

	# def has_add_permission(self, request, obj=None):
	# 	return False
	# def has_change_permission(self, request, obj=None):
	# 	return False

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Newsletter)