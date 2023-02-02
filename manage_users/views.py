from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate 
from django.contrib.auth import login as auth_login 
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import FormView
from meet.models import UserMeet
from django.db import transaction
import json
import datetime
from django.utils import timezone
from django_registration.backends.activation.views import RegistrationView
from django_registration.forms import RegistrationForm
from django.views.generic.edit import FormView
from .forms import MyCustomUserForm

HOST_MEET_TIMECHECK = 3600

class MyCustomUserFormView(RegistrationView):
    form_class = MyCustomUserForm
    template_name = "django_registration/registration_form.html" 
    success_url = '/accounts/register/complete'

    def post(self, request):

        self.request = request
        return super().post(request)


    def form_valid(self, form):
        user = form.save()
        if user is not None:
            self.send_activation_email(user)
            return HttpResponse("Ok") 
        else:
            return HttpResponse(status=404, reason="registration failed") 

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=404) 


class AjaxableResponseMixin:

    def get(self, request):
        user = User.objects.get(username=self.request.user.username)
        data = {
                'username': self.request.user.username,
                'email': self.request.user.email,
        }
        return JsonResponse(data)


    def form_valid(self, form):
        result = super(MyAccountFormView, self).form_valid(form)

        return result


    def post(self, commit=True):
        result = super(FormView, self).post(commit)
        return result

    def save(self, commit=True):
        result = super(MyAccountFormView, self).save(commit)
        return result


class MyAccountFormView(AjaxableResponseMixin, FormView):
    form_class = MyCustomUserForm 
    template_name = "django_registration/registration_form.html" 
    success_url = '/accounts/change/complete'

# Create your views here.

def login(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        user = authenticate(username = json_data['username'],
            password = json_data['password'])
        if user is not None:
            auth_login(request, user)
            return HttpResponse("ok")
        else:
            return HttpResponse(status=404, reason="authentication failed")
    else:
        return HttpResponse(status=404, reason="post required")


def register(request):

    if request.method == "POST":
        json_data = json.loads(request.body)
        username = json_data['username']
        password = json_data['password']
        email = json_data['email']
        rf = RegistrationForm(request.POST)

        result = register(username = json_data['username'],password = json_data['password'],email = json_data['email'])
                
        if result is not None:

            return HttpResponse("Ok")
        else:
            return HttpResponse(status=404, reason="registration failed")
    else:
        return HttpResponse(status=404, reason="post required")

