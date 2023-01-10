from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Webspace(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  site_name = models.CharField(max_length=10, default="", blank=False, primary_key=True)
  admin_email = models.EmailField(max_length=50) 
