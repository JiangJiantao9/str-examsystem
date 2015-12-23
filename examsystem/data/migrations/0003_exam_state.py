# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_answer_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='state',
            field=models.BooleanField(default=False),
        ),
    ]
