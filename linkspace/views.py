from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate 
from django.contrib.auth import login as auth_login 
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from meet.models import UserMeet
from django.db import transaction
import json
import datetime
from django.utils import timezone

HOST_MEET_TIMECHECK = 3600


# Create your views here.

def login(request):
	if request.method == "POST":
		json_data = json.loads(request.body)
		user = authenticate(username = json_data['username'],
			password = json_data['password'])
		if user is not None:
			auth_login(request, user)
			return HttpResponse("Ok")
		else:
			return HttpResponse(status=404, reason="authentication failed")
	else:
		return HttpResponse(status=404, reason="post required")

