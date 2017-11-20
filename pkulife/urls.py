"""pkulife URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'life.views.index', name='index'),
    url(r'^person/', 'life.views.person', name='person'),
    url(r'^room/', 'life.views.room', name='room'),
    url(r'^recommand/', 'life.views.recommand', name='recommand'),
    url(r'^membership/', 'life.views.mem', name='membership'),
    url(r'^source/', 'life.views.source', name='source'),
    url(r'^display_meta/', 'life.views.display_meta', name='display_meta'),
    url(r'^accounts/login/$', 'life.views.userLogin', name='login'),
    url(r'^accounts/register/$', 'life.views.userRegister', name='register'),
    url(r'^accounts/logout/$', 'life.views.userLogout', name='logout'),
    url(r'^accounts/activate/$', 'life.views.active_user', name='activate'),
]
