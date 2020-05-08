from django.contrib.auth.models import User
from django_registration.forms import RegistrationForm
from django import forms
from django.http import Http404, HttpResponse, JsonResponse

class MyCustomUserForm(RegistrationForm):
    zoom_meeting_id = forms.CharField(required=False)
    helper = forms.BooleanField(required=False)
    skills = forms.CharField(required=False) 

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
                'zoom_meeting_id': user.usermeet.zoom_meeting_id,
                'helper': user.usermeet.helper,
                'skills': user.usermeet.skills,
            }
            return JsonResponse(data)
        else:
            return response 


    def save(self, commit=True):
        result = super(MyCustomUserForm, self).save(commit)

        #username = self.request.user
        if result is not None: #and self.request.user == None:
            user = User.objects.get(username=self.cleaned_data['username'])
            user.usermeet.zoom_meeting_id = self.cleaned_data['zoom_meeting_id']
            user.usermeet.helper = self.cleaned_data['helper']
            user.usermeet.skills = self.cleaned_data['skills']
            user.usermeet.save()
            user.save()

        #if result is not None:  # and self.request.user: 
        #    user = User.objects.get(username=self.cleaned_data['username'])
        #    user.usermeet.zoom_meeting_id = self.cleaned_data['zoom_meeting_id']
        #    user.usermeet.helper = self.cleaned_data['helper']
        #    user.usermeet.skills = self.cleaned_data['skills']
        #    user.usermeet.save()
        #    user.save()

        return result
 
