from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from meet.models import UserMeet
from django.db import transaction
import json
import datetime
from django.utils import timezone
import subprocess 
import os

HOST_MEET_TIMECHECK = 3600


# Create your views here.

def meet(request):
	if request.user.is_authenticated:
		template = loader.get_template('meet/meet.html')
		#token = get_token(request.user.username, "88739b.vidyo.io" , 18000)
                #key = open("api.key", "r").read().strip()
                #key = os.environ["API_KEY"]

		#cmd = "python3 generateToken.py --key " + key + " --appID 88739b.vidyo.io --userName " + request.user.username +  " --expiresInSecs 1800"
		#print cmd	 
                #token = subprocess.check_output(["python", "generateToken.py", "--key", key, "--appID", "88739b.vidyo.io", "--userName", request.user.username, "--expiresInSecs", "18000"]).strip()
                zoom_meeting_id = request.user.usermeet.zoom_meeting_id 
		context = {"zoom_meeting_id": zoom_meeting_id}
		#print token
		return HttpResponse(template.render(context, request))
	else:
		return HttpResponse("Error") 

def host(request):
	if request.user.is_authenticated:
		with transaction.atomic():
			user = User.objects.get(username=request.user.username)
			user.usermeet.meet = True
			user.usermeet.host_dt = timezone.now()
			user.usermeet.save()
			user.save()
			return HttpResponse("OK")
	else:
		return Http404("Error")

def time_diff(dt1, dt2):
    return (dt2-dt1).total_seconds()	

def get_all_hosting_users(request):
    users = User.objects.all()
    hosts = []
    for user in users:
	# if user is the same as the current user skip 
        if user.username == request.user.username:
             continue

        if user.usermeet.meet:
		if user.usermeet.host_dt and time_diff(user.usermeet.host_dt, timezone.now()) < HOST_MEET_TIMECHECK:
            		hosts.append({'username' : user.username, 'zoom_meeting_id' : user.usermeet.zoom_meeting_id}) 
    return HttpResponse(json.dumps(hosts))

def get_hosting_users(request):
    skill = None
    skill = request.GET['skill']
    if skill is None:
        users = User.objects.all()
    else:
        users = User.objects.filter(usermeet__skills__contains=skill)

    hosts = []
    for user in users:
	# if user is the same as the current user skip 
        if user.username == request.user.username:
             continue

        if user.usermeet.meet:
		if user.usermeet.host_dt and time_diff(user.usermeet.host_dt, timezone.now()) < HOST_MEET_TIMECHECK:
            		hosts.append({'username' : user.username, 'zoom_meeting_id' : user.usermeet.zoom_meeting_id}) 
    return HttpResponse(json.dumps(hosts))




