from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
	url(r'^accounts/login/$',views.user_login,name='login'),
	url(r'^accounts/logout/$',views.user_logout,name='logout'),
	url(r'^accounts/signup/$',views.user_signup,name='signup'),
	url(r'^accounts/profile/$',views.profile,name='profile'),
	url(r'^accounts/client_profile/(?P<id>[\d]+)/$',views.patient_profile,name='patient_profile'),
	url(r'^accounts/profile/update/$',views.user_update.as_view(),name='user_update'),
	url(r'^accounts/profile/update/doctor/$',views.doctor_user_update.as_view(),name='doctor_user_update'),
	url(r'^appointments/new/$',views.make_appointment.as_view(),name='make_appointment'),
	url(r'^appointments/new/(?P<id>[\d]+)/$',views.make_appointment.as_view(),name='make_appointment'),
	url(r'^appointments/list-all/$',views.past_appointment.as_view(),name='past_appointment'),
	# url(r'^appointments/all/$',views.active_appointments.as_view(),name='active_appointments'),
	url(r'^doctor-portal/see-schedule/$',views.see_schedule.as_view(),name='see_schedule'),
	url(r'^doctor-portal/detail-appointment/(?P<pk>[\d]+)/$',views.detail_appointment,name='detail_appointment'),
	url(r'^see-profile/(?P<pk>[\d]+)/$',views.see_public_profile.as_view(),name='see_public_profile'),


	url(r'^predict_heart_disease/$',views.predict_heart_disease,name='predict_heart_disease'),
	url(r'^diabetes_predict/$',views.diabetes_predict,name='diabetes_predict'),
]
