# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0003_user_otp_secret'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='two_fa_enabled',
            field=models.BooleanField(default=False, help_text='Designates whether the user has enabled two-factor auth.', verbose_name='2FA enabled'),
        ),
    ]
