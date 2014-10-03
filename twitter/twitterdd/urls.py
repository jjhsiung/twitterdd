from django.conf.urls import patterns, url

from twitterdd import views
from django.shortcuts import redirect

urlpatterns = patterns('', 
    url(r'^$', views.index, name='index'),
    # ex: /twitterdd/username/user_page/
    url(r'^userpage/(?P<username>\S+)$', views.userpage, name='userpage'),
    # ex: /twitterdd/username/home_page/

    url(r'^newuser$', views.newuser, name='newuser'),
    url(r'^newtweet$', views.newtweet, name='newtweet'),
    url(r'^createuser$', views.createuser, name='createuser'),
    url(r'^logout$', views.user_logout, name='logout'),
    url(r'^createsuccess/(?P<username>\S+)$', views.createsuccess, name='createsuccess'),

)
