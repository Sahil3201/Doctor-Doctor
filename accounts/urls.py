from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
	url(r'^accounts/login/$',views.user_login,name='login'),
	url(r'^accounts/logout/$',views.user_logout,name='logout'),
	url(r'^accounts/signup/$',views.user_signup,name='signup'),
	url(r'^accounts/profile/$',views.profile,name='profile'),
	url(r'^accounts/profile/update/$',views.user_update.as_view(),name='user_update'),
	url(r'^appointments/new/$',views.make_appointment.as_view(),name='make_appointment'),
	url(r'^appointments/all/$',views.active_appointments.as_view(),name='active_appointments'),
	url(r'^doctor-portal/see_schedule/$',views.see_schedule.as_view(),name='see_schedule'),
	url(r'^doctor-portal/detail_appointment/(?P<pk>[\d]+)/$',views.detail_appointment.as_view(),name='detail_appointment'),
]