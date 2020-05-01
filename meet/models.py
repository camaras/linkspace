from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class UserMeet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    meet = models.BooleanField(default=False)
    zoom_meeting_id = models.CharField(max_length=30, default="", required=False)
    helper = models.BooleanField(default=False, required=False)
    skills = models.CharField(max_length=200, default="", required=False)
    host_dt = models.DateTimeField(null=True)
    
def create_usermeet(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_meet = UserMeet(user=user)
        user_meet.meet = False 
        user_meet.save()

post_save.connect(create_usermeet, sender=User)
