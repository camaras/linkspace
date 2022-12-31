from django.shortcuts import render
from django.forms.renderers import DjangoTemplates
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
from django.views.generic.edit import FormView, ProcessFormView, FormMixin 
from .forms import CreateWebspaceForm
# Create your views here.


class CreateWebspaceFormView(FormMixin, ProcessFormView):
    template_name = "webspace/webspace.html"
    form_class = CreateWebspaceForm
    success_url = "/webspace/create_webspace/"

    def form_valid(self, form):
        import pdb; pdb.set_trace()
        form = self.get_form()
        return form.form_valid(form)

    def render_to_response(self, context):
        import pdb; pdb.set_trace()
        #template = DjangoTemplates('webspace/webspace.html')
        return HttpResponse(DjangoTemplates().render('webspace/webspace.html', context, request=self.request))

    #def get_context_data(self, **kwargs):

    #    return {} 


def create_webspace(request):
    if request.user.is_authenticated:
        template = loader.get_template('webspace/webspace.html')
        return HttpResponse(template.render(request=request))
    else:
        return HttpResponse("Error") 

def submit_create_webspace(request):
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

