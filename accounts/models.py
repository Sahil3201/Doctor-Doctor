from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

# Ref: https://stackoverflow.com/questions/18130124/django-two-different-child-classes-point-to-same-parent-class
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Phone Number must be set')

        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        user = self.create_user(email, password, **kwargs)
        user.is_admin = True
        user.save()
        return user

# User:


class CustomUser(AbstractUser):
    id              = models.AutoField(primary_key=True)
    fullname        = models.CharField(blank=True, null=True, max_length=255)##
    is_doctor       = models.BooleanField(default=False, blank=True, null=True)
    password        = models.CharField(max_length=255)
    email           = models.EmailField(max_length=254, unique=True)
    date_of_birth   = models.DateField(blank=True, editable=True,null=True)
    date_created    = models.DateField(auto_now=True, editable=False)
    is_active       = models.BooleanField(default=True)
    is_admin        = models.BooleanField(default=False)
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # class Meta:
    #     abstract = True

    def __str__(self):
        return str(self.email)
    class Meta:
        verbose_name = 'All User'
blood_group_choices = [
    ('a+', 'A+ve'),
    ('a-', 'A-ve'),
    ('b+', 'B+ve'),
    ('b-', 'B-ve'),
    ('c+', 'AB+ve'),
    ('c-', 'AB-ve'),
    ('o+', 'O+ve'),
    ('o-', 'O-ve'),
]
marital_status_choices = [
    ('s', 'single'),
    ('m', 'married'),
    ('d', 'divorsed'),
    ('w', 'windowed'),
]
from django.urls import reverse
class Patient(CustomUser):

    # customuser = models.OneToOneField(CustomUser, parent_link=True,on_delete=models.CASCADE)
    phone_number = models.IntegerField(blank=True, null=True)
    blood_group = models.CharField(
        blank=True, null=True, max_length=2, choices=blood_group_choices)
    allergies = models.CharField(blank=True, null=True, max_length=512)
    marital_status = models.CharField(
        blank=True, null=True, max_length=1, choices=marital_status_choices)

    # emergency contact info
    emergency_Name = models.CharField(
        blank=True, null=True, max_length=30, verbose_name='Your emergency name')
    emergency_phone_number = models.IntegerField(
        blank=True, null=True, verbose_name='Your emergency phone number')
    emergency_relationship = models.CharField(
        blank=True, null=True, max_length=30, verbose_name='Relationship')

    # insurance info
    insurance_id        = models.IntegerField(blank=True,null=True)
    insurance_company    = models.CharField(blank=True, null=True, max_length=512)
    insurance_validity    = models.DateField(blank=True, editable=True,null=True)

    def get_absolute_url(self):
        return reverse('accounts:profile')#, args=[str(self.id)])
    class Meta:
        verbose_name = 'User: Patient'


class Doctor(CustomUser):
    # customuser         = models.OneToOneField(CustomUser, parent_link=True,on_delete=models.CASCADE)
    speciality          = models.CharField(blank=True, null=True, max_length=512)
    college             = models.CharField(blank=True, null=True, max_length=60)
    experience_years    = models.IntegerField(blank=True,null=True)

    class Meta:
        verbose_name = 'User: Doctor'

class Appointment(models.Model):
    doctor          = models.ForeignKey(Doctor,related_name='appointment_doctor',on_delete=models.CASCADE)
    patient         = models.ForeignKey(Patient,related_name='appointment_patient',on_delete=models.CASCADE,null=True)
    day1            = models.DateField(blank=True, editable=True,null=True)
    day2            = models.DateField(blank=True, editable=True,null=True)
    day3            = models.DateField(blank=True, editable=True,null=True)
    approved_for    = models.DateField(blank=True, editable=True,null=True)
    
    class Meta:
        verbose_name = 'Appointment'
    def __str__(self):
        return 'For '+str(self.doctor)+' by '+str(self.patient)

class Medicines(models.Model):
    appointment        = models.ForeignKey(Doctor,related_name='medicines_appointment',on_delete=models.CASCADE)
    medicine_name    = models.CharField(blank=True, null=True, max_length=512)

    class Meta:
        verbose_name = 'Medicine'


# class prescription(models.Model):
#     doctor    = models.ForeignKey(Doctor,related_name='appointment_doctor',on_delete=models.CASCADE)
#     patient    = models.ForeignKey(Patient,related_name='appointment_patient',on_delete=models.CASCADE)
#     appo