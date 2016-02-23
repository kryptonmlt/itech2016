from django.conf.urls import patterns, url
from game import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='game'),
                       url(r'^get_logs/$', views.get_logs, name='get_logs'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^buy/$', views.buy, name='buy'),
                       url(r'^get_gold/$', views.get_gold, name='get_gold'),
                       url(r'^create_alliance/$', views.create_alliance, name='create_alliance'),
                       url(r'^alliance_request/(?P<alliance_name>[\w\-]+)/$', views.alliance_request,
                           name='alliance_request'),
                       url(r'^accept_alliance/(?P<from_account_username>[\w\-]+)/$', views.accept_alliance,
                           name='accept_alliance'),
                       url(r'^decline_alliance/(?P<from_account_username>[\w\-]+)/$', views.decline_alliance,
                           name='decline_alliance'),
                       url(r'^attack/(?P<opponent>[\w\-]+)/$', views.attack,
                           name='attack'),
                       url(r'^leave_alliance/', views.leave_alliance, name='leave_alliance'),
                       url(r'^alliance/(?P<alliance_name>[\w\-]+)/$', views.alliance, name='alliance'),
                       url(r'^alliance_search/(?P<query>[\w\-]+)/$', views.alliance_search, name='alliance_search'),
                       url(r'^alliance_search/$', views.alliance_search_empty, name='alliance_search_empty'),
                       url(r'^battle/(?P<user_name>[\w\-]+)/$', views.battle, name='battle'),
                       )
