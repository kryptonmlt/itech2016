"""itech2016 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import patterns
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'home.views.register'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^game/', include('game.urls', namespace="game")),
    url(r'^register/$', 'home.views.register'),
    url(r'^login/$', 'home.views.user_login'),
    url(r'^stats/$', 'home.views.top_stats'),
]

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
         'serve',
         {'document_root': settings.MEDIA_ROOT}), )
