from django.conf.urls import patterns, url
from game import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='game'),
                       url(r'^get_logs/$', views.get_logs, name='get_logs'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^alliance/(?P<alliance_name>[\w\-]+)/$', views.alliance, name='alliance'),
                       url(r'^battle/(?P<user_name>[\w\-]+)/$', views.battle, name='battle'),
                       )
