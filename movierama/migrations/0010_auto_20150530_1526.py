# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movierama', '0009_remove_movies_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movies',
            old_name='like',
            new_name='likes',
        ),
        migrations.RemoveField(
            model_name='movies',
            name='unlike',
        ),
        migrations.AddField(
            model_name='movies',
            name='hates',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=True,
        ),
    ]
