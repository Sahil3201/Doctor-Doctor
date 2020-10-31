from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
	url(r'^login/$',views.user_login,name='login'),
	url(r'^logout/$',views.user_logout,name='logout'),
	url(r'^signup/$',views.user_signup,name='signup'),
	url(r'^profile/$',views.profile,name='profile'),
	url(r'^profile/update/$',views.user_update.as_view(),name='user_update'),
	url(r'^appointments/new/$',views.make_appointment.as_view(),name='make_appointment'),
	url(r'^appointments/all/$',views.active_appointments.as_view(),name='active_appointments'),
	url(r'^doctors/$',views.list_doctors.as_view(),name='list_doctors'),
]