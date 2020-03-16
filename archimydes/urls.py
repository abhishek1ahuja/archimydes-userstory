"""archimydes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf.urls import url
from userstory import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^stories$', views.stories_list),
    # url(r'^stories$', views.StoryListByUser.as_view()),
    url(r'^stories/(?P<pk>[0-9]+)$', views.story_detail),
    url(r'^stories/(?P<pk>[0-9]+)/submit', views.story_submit),
    url(r'^stories/(?P<pk>[0-9]+)/approve', views.story_approve),
    url(r'^stories/(?P<pk>[0-9]+)/reject', views.story_reject),
    url(r'^users$', views.users_list),
    url(r'^users/(?P<pk>[0-9]+)$', views.user_detail),
]
