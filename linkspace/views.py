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
from django_registration.views import RegistrationView
from django_registration.forms import RegistrationForm
from django.views.generic.edit import FormView
from .forms import MyCustomUserForm

HOST_MEET_TIMECHECK = 3600

class MyCustomUserFormView(RegistrationView):
    form_class = MyCustomUserForm
    template_name = "registration/registration_form.html" 
    success_url = '/accounts/register/complete'

    def post(self, request):

        self.request = request
        return super().post(request)


    def form_valid(self, form):
        form.save()
        return HttpResponse("Ok") 

    def form_invalid(self, form):
        return HttpResponse(status=404, reason="registration failed") 


class AjaxableResponseMixin:

    def get(self, request):
        user = User.objects.get(username=self.request.user.username)
        data = {
                'username': self.request.user.username,
                'email': self.request.user.email,
                'zoom_meeting_id': user.usermeet.zoom_meeting_id,
                'helper': user.usermeet.helper,
                'skills': user.usermeet.skills,
        }
        return JsonResponse(data)


    def form_valid(self, form):
        result = super(MyAccountFormView, self).form_valid(form)
        username = self.request.user.username

        user = User.objects.get(username=username)
        user.usermeet.zoom_meeting_id = self.cleaned_data['zoom_meeting_id']
        user.usermeet.helper = self.cleaned_data['helper']
        user.usermeet.skills = self.cleaned_data['skills']
        user.usermeet.save()
        user.save()

        return result


    def post(self, commit=True):
        result = super(FormView, self).post(commit)
        username = self.request.user.username
        f = self.get_form()
        user = User.objects.get(username=username)
        user.usermeet.zoom_meeting_id = f.data['zoom_meeting_id']
        #user.usermeet.helper = f.data['helper']
        user.usermeet.skills = f.data['skills']
        user.usermeet.save()
        user.save()

        return result

    def save(self, commit=True):
        result = super(MyAccountFormView, self).save(commit)
        username = self.request.user

        user = User.objects.get(username=self.cleaned_data['username'])
        user.usermeet.zoom_meeting_id = self.cleaned_data['zoom_meeting_id']
        user.usermeet.helper = self.cleaned_data['helper']
        user.usermeet.skills = self.cleaned_data['skills']
        user.usermeet.save()
        user.save()

        return result


class MyAccountFormView(AjaxableResponseMixin, FormView):
    form_class = MyCustomUserForm 
    template_name = "registration/registration_form.html" 
    success_url = '/accounts/change/complete'

# Create your views here.

def login(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        user = authenticate(username = json_data['username'],
            password = json_data['password'])
        if user is not None:
            auth_login(request, user)
            return HttpResponse("user.usermeet.zoom_meeting_id")
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
        zoom_meeting_id = json_data['zoom_meeting_id']
        print("hello")
        print(zoom_meeting_id)
                
        if result is not None:
            user = User.objects.get(username=request.user.username)
            user.usermeet.zoom_meeting_id = zoom_meeting_id
            user.usermeet.save()
            user.save()

            return HttpResponse("Ok")
        else:
            return HttpResponse(status=404, reason="registration failed")
    else:
        return HttpResponse(status=404, reason="post required")

