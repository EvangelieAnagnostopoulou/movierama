from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from movierama import views


urlpatterns = patterns('',
    # Home page
    url(r'^$', views.WelcomePage, name='home'),

    # Movie actions
    url(r'^create_movie', views.MovieCreate.as_view()),
    url(r'^edit_movie/(?P<pk>\d+)/', views.MovieUpdate.as_view()),
    url(r'^delete_movie/(?P<pk>\d+)/', views.MovieDelete.as_view()),

    url(r'^vote', views.vote),
    url(r'^user', views.user_profile),
    url(r'^like', views.like),
    url(r'^hate', views.hate),

    # Authentication module
    url(r'^accounts/', include('allauth.urls')),
)
