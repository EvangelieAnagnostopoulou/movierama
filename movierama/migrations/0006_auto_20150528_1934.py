# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movierama', '0005_auto_20150528_1311'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movies',
            old_name='dislike',
            new_name='unlike',
        ),
    ]
