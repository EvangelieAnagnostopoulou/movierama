# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movierama', '0008_auto_20150528_2143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movies',
            name='status',
        ),
    ]
