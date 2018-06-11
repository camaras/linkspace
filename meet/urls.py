from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^meet$', views.meet, name='meet'),
	url(r'^meet/$', views.meet, name='meet'),
	url(r'^host$', views.host, name='host'),
	url(r'^get_all_hosting_users$', views.get_all_hosting_users, name='get_all_hosting_users')
]
