# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_exam_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='testlog',
            name='answer',
            field=models.ForeignKey(default=None, to='data.Answer', null=True),
        ),
    ]
