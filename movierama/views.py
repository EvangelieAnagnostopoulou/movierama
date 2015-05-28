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
        all_entries = Movies.objects.all().order_by('-like')
    elif sort == 'hate':
        all_entries = Movies.objects.all().order_by('-dislike')
    elif sort == 'date':
        all_entries = Movies.objects.all().order_by('date')
    else:
        all_entries = Movies.objects.all().order_by('date')

    params = {'all_entries': all_entries}
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
        status = request.GET.get('status')
        movie_id =Movies.objects.get(id=m)
        exist_like = MovieRate.objects.filter(movie=movie_id, user=request.user, rate=1)
        exist_dislike = MovieRate.objects.filter(movie=movie_id, user=request.user, rate=-1)
        if movie_id.username != request.user.username:
            #if user hadn't vote
            if not exist_dislike and not exist_like:
                if status == 'like':
                    MovieRate.objects.create(movie=movie_id, user=request.user, rate=1)
                    movie_id.status=1

                elif status == 'dislike':
                    MovieRate.objects.create(movie=movie_id, user=request.user, rate=-1)
                    movie_id.status=-1
            #if user disliked the movie
            elif exist_dislike:
                if status == 'like':
                    r = MovieRate.objects.filter(movie=movie_id, user=request.user, rate=-1)[0]
                    r.rate = 1
                    movie_id.status=1
                    r.save()
                    print('You change status')
                else:
                    print('You have disliked this movie!')
            #if user liked the movie
            elif exist_like:
                if status == 'dislike':
                    r = MovieRate.objects.filter(movie=movie_id, user=request.user,rate=1)[0]
                    r.rate = -1
                    movie_id.status=-1
                    r.save()
                    print('You change status')
                else:
                    print('You have liked this movie!')
        else:
            print('You cannnot vote your movie')

        likes = MovieRate.objects.filter(movie=movie_id, rate=1).count()
        dislikes = MovieRate.objects.filter(movie=movie_id, rate=-1).count()
        movie_id.like = likes
        movie_id.dislike = dislikes
        movie_id.save()
        all_entries = Movies.objects.all()
        params = {'all_entries': all_entries}
        return render(request, "mainPage.html", params)

def user_profile(request):
    #get all user's movies
    name= request.GET.get('name')
    sort = request.GET.get('sort_by')
    if sort == 'like':
        all_entries = Movies.objects.filter(username=name).order_by('-like')
    elif sort == 'hate':
        all_entries = Movies.objects.filter(username=name).order_by('-dislike')
    elif sort == 'date':
        all_entries = Movies.objects.filter(username=name).order_by('date')
    else:
        all_entries = Movies.objects.filter(username=name).order_by('date')
        #all_entries = Movies.objects.filter(username=name)
    print all_entries
    return render(request, "mainPage.html", {'all_entries': all_entries, 'user': True, 'name': name })

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
    return render(request, "likePage.html", {'user': user, 'movie_id': movie_id, })
