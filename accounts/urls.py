from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
	url(r'^login/$',views.user_login,name='login'),
	url(r'^logout/$',views.user_logout,name='logout'),
	url(r'^signup/$',views.user_signup,name='signup'),
	url(r'^profile/$',views.profile,name='profile'),
]