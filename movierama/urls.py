from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from movierama import views


urlpatterns = patterns('',
    # Home page
    url(r'^$', views.WelcomePage, name='home'),
    url(r'^create_movie', views.create),
    url(r'^vote', views.vote),
    url(r'^user', views.user_profile),
    url(r'^like', views.like),
    url(r'^dislike', views.dislike),
    # Authentication module
    url(r'^accounts/', include('allauth.urls')),


    #url(r'^admin/', include(admin.site.urls)),
)
