# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='user',
        ),
        migrations.DeleteModel(
            name='Link',
        ),
    ]
