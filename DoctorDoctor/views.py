from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
def home(request):
	if request.method=='POST':
		return render(request,'DoctorDoctor/home.html')
	else:
		import requests
		url = ('https://newsapi.org/v2/top-headlines?category=health&country=in&q=covid&q=india&apiKey=e3723180c39644e791fa3b87cc5fe5f2')
		response = requests.get(url)

		con = {}

		con['news_1_name'] = response.json()['articles'][0]['source']['name']
		con['news_1_title'] = response.json()['articles'][0]['title']
		con['news_1_url'] = response.json()['articles'][0]['url']
		con['news_1_des'] = response.json()['articles'][0]['description']

		con['news_2_name'] = response.json()['articles'][1]['source']['name']
		con['news_2_title'] = response.json()['articles'][1]['title']
		con['news_2_url'] = response.json()['articles'][1]['url']
		con['news_2_des'] = response.json()['articles'][1]['description']

		con['news_3_name'] = response.json()['articles'][2]['source']['name']
		con['news_3_title'] = response.json()['articles'][2]['title']
		con['news_3_url'] = response.json()['articles'][2]['url']
		con['news_3_des'] = response.json()['articles'][2]['description']
		return render(request,'DoctorDoctor/home.html',context=con)

class departments(TemplateView):
	template_name='DoctorDoctor/departments.html'

class doctors(TemplateView):
	template_name='DoctorDoctor/doctors.html'