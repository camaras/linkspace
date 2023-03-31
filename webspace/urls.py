from django.conf.urls import url

from . import views
from .forms import CreateWebspaceForm
from .views import CreateWebspaceFormView, get_webspaces

urlpatterns = [
    url(r'^create_webspace/$', CreateWebspaceFormView.as_view(), name='webspace'),
    url(r'^webspaces/$', get_webspaces, name='webspaces'),
    url(r'^login_admin/(?P<site_name>\w{1,50})/$', views.login_admin)
]
