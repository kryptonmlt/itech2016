from django.conf.urls import patterns, url
from game import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
                       url(r'^$', views.index, name='game'),
                       url(r'^get_logs/$', views.get_logs, name='get_logs'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^buy/$', views.buy, name='buy'),
                       url(r'^get_resources/$', views.get_resources, name='get_resources'),
                       url(r'^collect/$', views.collect, name='collect'),
                       url(r'^get_map/$', views.get_map, name='get_map'),
                       url(r'^get_map_details/$', views.get_map_details, name='get_map_details'),
                       url(r'^last_attacked/(?P<enemy_acc_id>[\w\-]+)/$', views.last_attacked,
                           name='last_attacked'),
                       url(r'^get_messages/$', views.get_messages, name='get_messages'),
                       url(r'^get_alliance_messages/$', views.get_alliance_messages, name='get_alliance_messages'),
                       url(r'^add_message/$', views.add_message, name='add_message'),
                       url(r'^add_alliance_message/$', views.add_alliance_message, name='add_alliance_message'),
                       url(r'^change_orders/$', views.change_orders, name='change_orders'),
                       url(r'^kick_member/(?P<member>[\w\-]+)/$', views.kick_member,
                           name='kick_member'),
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

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
