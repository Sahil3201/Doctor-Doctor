from django.shortcuts import render, redirect, HttpResponseRedirect, reverse, HttpResponse
from django.views.generic import TemplateView
from accounts.models import Newsletter

# Create your views here.
def home(request):
	if request.method=='POST':
		email = request.POST.get('email')
		newsletter = Newsletter(email=email)
		newsletter.save()
		return redirect('home')
	# 	return HttpResponseRedirect(reverse('home'))
	try:
		con = {}

		import requests
		url = ('https://newsapi.org/v2/top-headlines?category=health&country=in&q=covid&q=india&apiKey=e3723180c39644e791fa3b87cc5fe5f2')
		response = requests.get(url)

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
	except :
		pass
	finally:
		return render(request,'DoctorDoctor/home.html',context=con)

class doctors(TemplateView):
	template_name='DoctorDoctor/doctors.html'