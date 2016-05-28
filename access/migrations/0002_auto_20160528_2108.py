# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import access.models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', access.models.UserManager()),
            ],
        ),
    ]
