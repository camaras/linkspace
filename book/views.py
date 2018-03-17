from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
# Create your views here.

def book(request):
	if request.user.is_authenticated:
		template = loader.get_template('book/book.html')
		context = {}
		return HttpResponse(template.render(context, request))
	else:
		raise Http404("Error") 


def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    return User.objects.filter(id__in=uid_list) 
