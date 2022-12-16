from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create_webspace$', views.webspace, name='webspace'),
]
