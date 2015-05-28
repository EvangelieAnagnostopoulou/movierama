__author__ = 'evangelie'
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Movies(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.TextField(db_column='userName', blank=True)  # Field name made lowercase.
    title = models.TextField(blank=False, max_length=200)
    description = models.TextField(blank=False, max_length=1000)
    date = models.DateField(auto_now=True)
    like = models.IntegerField(default=0, blank=True)
    dislike = models.IntegerField(default=0, blank=True)
    status = models.IntegerField(default=0)

    class Meta:
        db_table = 'movies'

class MovieRate(models.Model):
    user = models.ForeignKey(User, related_name="rates")
    movie = models.ForeignKey(Movies)
    rate = models.DecimalField(max_digits=2,decimal_places=1,)

