from django import forms
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
import subprocess
from .models import Webspace

class CreateWebspaceForm(forms.Form):
    site_name = forms.CharField(required=False)
    admin_email = forms.CharField(required=False)
    admin_password = forms.CharField(required=False) 

    def __init__(self, *args, **kwargs):
        self.request  = kwargs.pop('request', None)
        super(CreateWebspaceForm, self).__init__(*args, **kwargs)

