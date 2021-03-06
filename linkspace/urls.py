"""linkspace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView, RedirectView
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import *
from django.contrib.auth import views as auth_views
from . import views


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet) 


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.hmac.urls')),

#    url(r'^$', RedirectView.as_view(url='accounts/login'), name='index'),	
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^meet/', include('meet.urls')),
    url(r'book/', include('book.urls')),
    url(r'api/', include(router.urls)),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^schedule/', include('schedule.urls'), name='scheduler')
]

if settings.DEBUG:
#	urlpatterns += [url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
#            {'document_root': settings.STATIC_ROOT, 'show_indexes': True})]

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
