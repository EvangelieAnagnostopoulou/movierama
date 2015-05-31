from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, CreateView, DeleteView
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


class MovieCreate(CreateView):
    form_class = MovieForm
    model = Movies
    context_object_name = 'movie'
    template_name = "movie/create.html"
    success_url = "/"

    def form_valid(self, form):
        form.instance.username = self.request.user.username
        form.save()
        return super(MovieCreate, self).form_valid(form)


class MovieUpdate(UpdateView):
    form_class = MovieForm
    model = Movies
    context_object_name = 'movie'
    template_name = "movie/update.html"
    success_url = "/"

    def form_valid(self, form):
        form.instance.username = self.request.user.username
        form.save()
        return super(MovieUpdate, self).form_valid(form)

class MovieDelete(DeleteView):
    form_class = MovieForm
    model = Movies
    context_object_name = 'movie'
    template_name = "movie/delete.html"
    success_url = "/"


# Vote movie
@login_required
def vote(request):
    if request.method == 'GET':
        m= request.GET.get('id')
        vote = int(request.GET.get('vote'))
        movie =Movies.objects.get(id=m)

        if movie.username != request.user.username:
            import pdb; pdb.set_trace()
            f = MovieRate.objects.filter(movie=movie, user=request.user)
            if vote == 0:
                f.delete()
            else:
                if f:
                    return HttpResponseForbidden("You must first unlike/unhate to vote again")
                else:
                    MovieRate.objects.create(movie=movie, user=request.user, rate=vote)
        else:
            return HttpResponseForbidden('You can not vote your movie')

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
