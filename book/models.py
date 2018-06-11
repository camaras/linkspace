from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from schedule.models.calendars import Calendar 

# Create your models here.

class UserCalendar(models.Model):
    user = models.OneToOneField(User)
    slug = models.CharField(max_length=200)

def create_usercalendar(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
	calendar = Calendar(name=user.username + "'s calendar")
	calendar.slug = user.username
        #calendar = CalendarManager().get_or_create_calendar_for_object(user)
	calendar.save()
	calendar.create_relation(user)
	user_calendar = UserCalendar(user=user)
	user_calendar.slug = calendar.slug
        user_calendar.save()

post_save.connect(create_usercalendar, sender=User)
