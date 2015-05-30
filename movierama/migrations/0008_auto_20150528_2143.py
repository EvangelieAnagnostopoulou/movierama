# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movierama', '0007_auto_20150528_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movies',
            name='title',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]
