from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from movierama.forms import MovieForm
from movierama.models import Movies, MovieRate

__author__ = 'evangelie'


"""
* gets all Movies in the database
* optionally specify ORDER BY clause
* optionally specify movie creator
"""
def get_movies(sort=None, username=None):
    if sort == 'like':
        order = '-likes'
    elif sort == 'hate':
        order = '-hates'
    else:
        order = '-date'

    # fetch movies from database
    if username:
        movies = Movies.objects.filter(username=username)
    else:
        movies = Movies.objects.all()

    movies = movies.order_by(order)

    return movies


def WelcomePage(request):
    sort = request.GET.get("sort_by")
    movies = get_movies(sort=sort)

    m_rate =MovieRate.objects.all()
    params = {'movies': movies, 'home': True, 'movie_rate': m_rate}
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

            # return to home page
            return redirect("/")


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
            return HttpResponseForbidden('You cannnot vote your movie')

        movie.likes = MovieRate.objects.filter(movie=movie, rate=1).count()
        movie.hates = MovieRate.objects.filter(movie=movie, rate=-1).count()
        movie.save()

        return redirect("/")

def user_profile(request):
    # get all user's movies
    name= request.GET.get('name')
    sort = request.GET.get('sort_by')

    movies = get_movies(sort=sort, username=name)
    return render(request, "mainPage.html", {'movies': movies, 'userprofile': True, 'name': name })

def like(request):
    m= request.GET.get('movie')
    movie_id =Movies.objects.get(id=m)
    exist_like = MovieRate.objects.filter(movie=movie_id, rate=1)
    user=[]
    for e in exist_like:
        user.append(e.user)
    return render(request, "likePage.html", {'user': user, 'movie_id': movie_id, })

def hate(request):
    m= request.GET.get('movie')
    movie_id =Movies.objects.get(id=m)
    exist_like = MovieRate.objects.filter(movie=movie_id, rate=-1)
    user=[]
    for e in exist_like:
        user.append(e.user)
    return render(request, "hatePage.html", {'user': user, 'movie_id': movie_id, })
