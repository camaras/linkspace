from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
from django.forms.renderers import DjangoTemplates
from django.template import loader
from django.http import Http404, HttpResponse, JsonResponse
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
from .models import Webspace
from django.conf import settings
from django.http import QueryDict
import logging
import hashlib
# Create your views here.


class CreateWebspaceFormView(FormMixin, ProcessFormView):
    template_name = "webspace/webspace.html"
    form_class = CreateWebspaceForm
    success_url = "/webspace/create_webspace/"

    def post(self, request, *args, **kwargs):
      super().post(request, *args, **kwargs)
      username = request.user.username
      user_webspaces = Webspace.objects.filter(user__username=username)
      form = self.get_form()
      site_name = form['site_name'].value()
      admin_email = form['admin_email'].value()
      admin_password = form['admin_password'].value()

      if len(user_webspaces) >= settings.MAX_WEBSITES_PER_USER:
          http_response = JsonResponse({"1" : "Error: maximum number of websites per user is {}".format(settings.MAX_WEBSITES_PER_USER)})
          http_response.status_code = 406
          return http_response

      if site_name in [webspace.site_name for webspace in Webspace.objects.all()]:
          http_response = JsonResponse({"1" : "Error: {} is already taken".format(site_name)})
          http_response.status_code = 409
          return http_response

      output = subprocess.run([settings.CREATE_WORDPRESS_SCRIPT, site_name, admin_email, admin_password, username], capture_output=True)
      if (output.returncode == 0):
          user = User.objects.get(username=username)
          webspace = Webspace(user=user, site_name=site_name, admin_email=admin_email)
          webspace.save()
          return JsonResponse({ "site_name" : site_name, "site_url" : settings.WORDPRESS_URL_BASE + "/" + username + "/" + site_name + "/", "admin_site_url" : settings.WORDPRESS_URL_BASE + "/" + username + "/" + site_name + "/wp-admin/"})
      elif ("already" in str(output.stdout) or "exists" in str((output.stdout))):
          http_response = JsonResponse({"one" : "conflicts in installing  wordpress"})
          http_response.status_code = 409
          return http_response
      else:
          http_response = JsonResponse({"one" : "Errors in installing wordpress"})
          http_response.status_code = 409
          return http_response

      # do update to webspace table here. 

    def render_to_response(self, context):
        return HttpResponse(DjangoTemplates().render('webspace/webspace.html', context, request=self.request))


    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):

      super().get(request, *args, **kwargs)
      username = self.request.user.username
      user_webspaces = Webspace.objects.filter(user__username=username)
      webspace_urls = [] 
      for webspace in user_webspaces:
        webspace_urls.append(
          { 
            "name" : webspace.site_name,
            "site" : settings.WORDPRESS_URL_BASE + "/" + username + "/" + webspace.site_name + "/",
            "admin_site" : settings.WORDPRESS_URL_BASE + "/" + username + "/" + webspace.site_name + "/wp-admin/" 
          }) 

      return self.render_to_response({"webspaces": webspace_urls})

    @method_decorator(ensure_csrf_cookie)
    def delete(self, request, *args, **kwargs):
      username = self.request.user.username
      query_params = QueryDict(request.body)
      site_name = query_params['site_name']

      user_webspace = Webspace.objects.filter(user__username=username).filter(site_name=site_name)

      if len(user_webspace) == 1:
          user_webspace.delete()
          return JsonResponse({})


      http_response = JsonResponse({"error" : "Errors in installing wordpress"})
      http_response.status_code = 500 
      return http_response

def get_webspaces(request):
    if request.user.is_authenticated:
      username = request.user.username
      user_webspaces = Webspace.objects.filter(user__username=username)
      webspace_urls = [] 
      for webspace in user_webspaces:
        webspace_urls.append(
          { 
            "name" : webspace.site_name,
            "site" : settings.WORDPRESS_URL_BASE + "/" + username + "/" + webspace.site_name + "/",
            "admin_site" : settings.WORDPRESS_URL_BASE + "/" + username + "/" + webspace.site_name + "/wp-admin/" 
          }) 

      response = JsonResponse({"websites" : webspace_urls})
      response.set_cookie("webspace_username", request.user.username)
      return response

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


def login_admin(request, site_name=None):
 
  logger = logging.getLogger(__name__)
 
  if request.user.is_authenticated:
    auth_cookie = subprocess.run(['php', 'webspace/get_auth_cookie.php', settings.ROOT_WORDPRESS_DIR + "/" + request.user.username + "/" + site_name], capture_output=True).stdout.decode("utf-8")
    logger.info("auth_cookie is {auth_cookie}".format(auth_cookie=auth_cookie))
    login_cookie = subprocess.run(['php', 'webspace/get_logged_in_cookie.php', settings.ROOT_WORDPRESS_DIR + "/" + request.user.username + "/" + site_name], capture_output=True).stdout.decode("utf-8")
    logger.info("login_cookie is {login_cookie}".format(login_cookie=login_cookie))
    response = HttpResponse(status=302)
    site_url = 'https://wordpress.webnote.com.au/wordpress/{user_name}/{site_name}'.format(user_name=request.user.username, site_name=site_name)
    cookie_name = "wordpress_sec_" + hashlib.md5(site_url.encode('utf-8')).hexdigest()
    logged_cookie_name = "wordpress_logged_in_" + hashlib.md5(site_url.encode('utf-8')).hexdigest()
    response['Location'] = (site_url + '/wp-admin/').format(user_name=request.user.username, site_name=site_name)
    response.set_cookie(cookie_name, auth_cookie, domain="webnote.com.au")
    response.set_cookie(logged_cookie_name, login_cookie, domain="webnote.com.au")
    return response
