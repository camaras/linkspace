from django.contrib.auth.models import User
from django_registration.forms import RegistrationForm
from django import forms
from django.http import Http404, HttpResponse, JsonResponse

class MyCustomUserForm(RegistrationForm):

    def __init__(self, *args, **kwargs):
        self.request  = kwargs.pop('request', None)
        super(MyCustomUserForm, self).__init__(*args, **kwargs)

    def form_valid(self, form):

        form.save()
        response = super(MyCustomUserForm, self).form_valid(form)
        if self.request.is_ajax():
            user = User.objects.get(username=self.request.user)
            data = {
                'username': self.request.user,
            }
            return JsonResponse(data)
        else:
            return response 


    def save(self, commit=True):
        result = super(MyCustomUserForm, self).save(commit)

        return result
 
