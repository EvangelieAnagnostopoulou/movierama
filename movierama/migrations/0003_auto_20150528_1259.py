# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movierama', '0002_movies_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movierate',
            name='movie',
            field=models.ForeignKey(to='movierama.Movies', unique=True),
        ),
    ]
