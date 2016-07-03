# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(verbose_name='slug', editable=False),
        ),
    ]
