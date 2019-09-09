from django.contrib.auth.models import User
from registration.forms import RegistrationForm
from django import forms
from django.http import Http404, HttpResponse

class MyCustomUserForm(RegistrationForm):
    zoom_meeting_id = forms.CharField() 


    def form_valid(self, form):
        form.save()
        super(MyCustomUserForm, self).form_valid(form)



    def save(self):
        result = super(MyCustomUserForm, self).save()

        if result is not None:
            user = User.objects.get(username=self.cleaned_data['username'])
            user.usermeet.zoom_meeting_id = self.cleaned_data['zoom_meeting_id']
            user.usermeet.save()
            user.save()

            return HttpResponse("Ok")
        else:
            return HttpResponse(status=404, reason="registration failed") 
 
