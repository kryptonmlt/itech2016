from django.conf.urls import patterns, url
from game import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='game'),
<<<<<<< HEAD
                       url(r'^get_logs/$', views.get_logs, name='get_logs'),  
                       url(r'^logout/$', views.user_logout, name='user_logout'),
=======
                       url(r'^stats/$', views.top_stats, name='top_stats'),
                       url(r'^get_logs/$', views.get_logs, name='get_logs'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^battle/(?P<user_name>[\w\-]+)/$', views.battle, name='battle'),
>>>>>>> 54f6000914e30d17a9dd2fc14c39c2d07d311952
                       )
