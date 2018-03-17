from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^meet$', views.meet, name='meet'),
]
