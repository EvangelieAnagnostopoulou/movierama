from django.shortcuts import render, redirect, render_to_response
from django import forms
from movierama.forms import MovieForm, UserForm
from movierama.models import Movies, MovieRate
from datetime import datetime



__author__ = 'evangelie'


def WelcomePage(request):
     #get all movies from database
    sort = request.GET.get('sort_by')
    if sort == 'like':
        all_entries = Movies.objects.all().order_by('-likes')
    elif sort == 'hate':
        all_entries = Movies.objects.all().order_by('-hates')
    elif sort == 'date':
        all_entries = Movies.objects.all().order_by('-date')
    else:
        all_entries = Movies.objects.all().order_by('-date')
    m_rate =MovieRate.objects.all()
    params = {'all_entries': all_entries, 'home': True, 'movie_rate': m_rate}
    return render(request, "mainPage.html", params)


#Create movie
def create(request):
    if request.method == 'GET':
        form = MovieForm(initial={'title': "", 'description': "", 'username': "",})
        params = {'form': form}
        return render(request, "create_movie.html", params)
    if request.method == 'POST':
        form = MovieForm(request.POST)
        #validate form
        if not form.is_valid():
            error = "Invalid value"
            print form.errors
            params = {'form': form, 'error': error}
            return render(request, "create_movie.html", params)
        else:
            new_movie = form.save(commit=False)
            new_movie.username = request.user.username
            #save to database new movie
            new_movie.save()
            all_entries = Movies.objects.all()
            params = {'all_entries': all_entries}
            return render(request, "mainPage.html",params)


#Vote movie
def vote(request):
    if request.method == 'GET':
        m= request.GET.get('id')
        vote = int(request.GET.get('vote'))
        movie =Movies.objects.get(id=m)

        if movie.username != request.user.username:
            f = MovieRate.objects.filter(movie=movie, user=request.user)
            if vote == 0:
                f.delete()
            else:
                MovieRate.objects.create(movie=movie, user=request.user, rate=vote)
        else:
            print('You cannnot vote your movie')

        movie.likes = MovieRate.objects.filter(movie=movie, rate=1).count()
        movie.hates = MovieRate.objects.filter(movie=movie, rate=-1).count()
        movie.save()

        return redirect("/")

def user_profile(request):
    #get all user's movies
    name= request.GET.get('name')
    sort = request.GET.get('sort_by')
    if sort == 'like':
        all_entries = Movies.objects.filter(username=name).order_by('-likes')
    elif sort == 'hate':
        all_entries = Movies.objects.filter(username=name).order_by('-hates')
    elif sort == 'date':
        all_entries = Movies.objects.filter(username=name).order_by('-date')
    else:
        all_entries = Movies.objects.filter(username=name).order_by('-date')
        #all_entries = Movies.objects.filter(username=name)
    print all_entries
    return render(request, "mainPage.html", {'all_entries': all_entries, 'userprofile': True, 'name': name })

def like(request):
    m= request.GET.get('movie')
    movie_id =Movies.objects.get(id=m)
    exist_like = MovieRate.objects.filter(movie=movie_id, rate=1)
    user=[]
    for e in exist_like:
        user.append(e.user)
    return render(request, "likePage.html", {'user': user, 'movie_id': movie_id, })

def dislike(request):
    m= request.GET.get('movie')
    movie_id =Movies.objects.get(id=m)
    exist_like = MovieRate.objects.filter(movie=movie_id, rate=-1)
    user=[]
    for e in exist_like:
        user.append(e.user)
    return render(request, "hatePage.html", {'user': user, 'movie_id': movie_id, })
