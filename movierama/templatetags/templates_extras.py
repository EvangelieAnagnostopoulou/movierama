__author__ = 'evangelie'
from django import template
from movierama.models import Movies, MovieRate

register = template.Library()

@register.filter(name='is_like')
def is_like(movie, user):
    #import pdb;pdb.set_trace()
    return MovieRate.objects.filter(movie=movie, user=user, rate=1).exists()

@register.filter(name='is_hate')
def is_hate(movie, user):
    return MovieRate.objects.filter(movie=movie, user=user, rate=-1).exists()
