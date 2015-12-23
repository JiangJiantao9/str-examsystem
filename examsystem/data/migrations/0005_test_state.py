# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_testlog_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='state',
            field=models.BooleanField(default=False),
        ),
    ]
