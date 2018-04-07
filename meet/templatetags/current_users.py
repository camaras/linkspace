from django import template
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)

register = template.Library()

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
    logged_in_users = User.objects.filter(id__in=uid_list)

    # get all users who are hosting meetings
    hosting_users = []
    for u in logged_in_users:
	logger.info("checking " + u.username)
	hosting_users.append(u)
	try:
            if u.usermeet.meet:
                hosting_users.append(u)
	except ObjectDoesNotExist:
            pass  

    return hosting_users



@register.inclusion_tag('meet/logged_in_user_list.html', takes_context=True)
def render_logged_in_user_list(context):
    return { 'users': get_all_logged_in_users(), 'user' : context['request'].user }
