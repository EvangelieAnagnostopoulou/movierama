# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate', models.DecimalField(max_digits=2, decimal_places=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.TextField(db_column=b'userName', blank=True)),
                ('title', models.TextField(max_length=200)),
                ('description', models.TextField(max_length=1000)),
                ('date', models.DateField(auto_now=True)),
                ('like', models.IntegerField(default=0, blank=True)),
                ('dislike', models.IntegerField(default=0, blank=True)),
            ],
            options={
                'db_table': 'movies',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='movierate',
            name='movie',
            field=models.ForeignKey(to='movierama.Movies'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movierate',
            name='user',
            field=models.ForeignKey(related_name=b'rates', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
