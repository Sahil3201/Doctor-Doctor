from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
def home(request):
	if request.method=='POST':
		return render(request,'DoctorDoctor/home.html')
	else:
		return render(request,'DoctorDoctor/home.html')

class departments(TemplateView):
	template_name='DoctorDoctor/departments.html'

class doctors(TemplateView):
	template_name='DoctorDoctor/doctors.html'