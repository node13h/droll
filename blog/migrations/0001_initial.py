# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('public', models.BooleanField(default=False, db_index=True, verbose_name='public')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, db_index=True, verbose_name='timestamp')),
                ('title', models.CharField(max_length=140, verbose_name='title')),
                ('body', models.TextField(verbose_name='body')),
            ],
        ),
    ]
