# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='test',
            field=models.ForeignKey(default=True, to='data.Test', null=True),
        ),
    ]
