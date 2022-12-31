from django.conf.urls import url

from . import views
from .forms import CreateWebspaceForm
from .views import CreateWebspaceFormView

urlpatterns = [
    url(r'^create_webspace/$', CreateWebspaceFormView.as_view(), name='webspace'),
]
