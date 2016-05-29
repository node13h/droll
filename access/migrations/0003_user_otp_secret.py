# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0002_auto_20160528_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp_secret',
            field=models.CharField(verbose_name='OTP secret', max_length=16, editable=False, default=''),
        ),
    ]
