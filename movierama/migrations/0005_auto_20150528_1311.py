# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movierama', '0004_auto_20150528_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movierate',
            name='rate',
            field=models.DecimalField(max_digits=2, decimal_places=1),
        ),
    ]
