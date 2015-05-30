from django.db.models.signals import post_delete

__author__ = 'evangelie'
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Movies(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.TextField(db_column='userName', blank=True)  # Field name made lowercase.
    title = models.CharField(blank=False, max_length=50)
    description = models.TextField(blank=False, max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    hates = models.IntegerField(default=0)

    class Meta:
        db_table = 'movies'

class MovieRate(models.Model):
    user = models.ForeignKey(User, related_name="rates")
    movie = models.ForeignKey(Movies)
    rate = models.DecimalField(max_digits=2,decimal_places=1,)

    @staticmethod
    def on_delete(sender, instance, *args, **kwargs):
        if instance.rate == 1:
            instance.movie.likes -= 1
        else:
            instance.movie.hates -= 1

        instance.movie.save()

post_delete.connect(MovieRate.on_delete, sender=MovieRate)

