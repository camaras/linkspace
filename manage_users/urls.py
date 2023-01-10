"""linkspace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .forms import MyCustomUserForm
from .views import MyCustomUserFormView, MyAccountFormView
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^accounts/register/$', MyCustomUserFormView.as_view(
        form_class=MyCustomUserForm), name='registration_register'),
    url(r'^accounts/change/$', MyAccountFormView.as_view(
        form_class=MyCustomUserForm), name='account'),
    url(r'^login/$', views.login, name='login_front'),
    url(r'^register/$', views.register, name='register_front'),
    url(r'^accounts/password_reset/$', auth_views.PasswordResetView.as_view(template_name="django_registration/password_reset_form.html", success_url = '/'), name='password_reset'),
]
