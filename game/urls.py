from django.conf.urls import patterns, url
from game import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='game'),
                       url(r'^get_logs/$', views.get_logs, name='get_logs'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^buy/$', views.buy, name='buy'),
                       url(r'^alliance_request/(?P<alliance_name>[\w\-]+)/$', views.alliance_request,
                           name='alliance_request'),
                       url(r'^accept_alliance/(?P<from_account_username>[\w\-]+)/$', views.accept_alliance,
                           name='accept_alliance'),
                       url(r'^decline_alliance/(?P<from_account_username>[\w\-]+)/$', views.decline_alliance,
                           name='decline_alliance'),
                       url(r'^leave_alliance/', views.leave_alliance, name='leave_alliance'),
                       url(r'^alliance/(?P<alliance_name>[\w\-]+)/$', views.alliance, name='alliance'),
                       url(r'^battle/(?P<user_name>[\w\-]+)/$', views.battle, name='battle'),
                       )
