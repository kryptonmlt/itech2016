from django.conf.urls import patterns, url
from game import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='game'),
                       url(r'^get_logs/$', views.get_logs, name='get_logs'),  
                       url(r'^logout/$', views.user_logout, name='user_logout'),
                       )
