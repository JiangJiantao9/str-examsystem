# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_auto_20151222_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saquestion',
            name='diffculty',
            field=models.CharField(max_length=2, verbose_name=b'\xe9\x9a\xbe\xe5\xba\xa6', choices=[(b'ez', b'\xe7\xae\x80\xe5\x8d\x95'), (b'nm', b'\xe6\x99\xae\xe9\x80\x9a'), (b'hd', b'\xe5\x9b\xb0\xe9\x9a\xbe')]),
        ),
        migrations.AlterField(
            model_name='tfquestion',
            name='diffculty',
            field=models.CharField(max_length=2, verbose_name=b'\xe9\x9a\xbe\xe5\xba\xa6', choices=[(b'ez', b'\xe7\xae\x80\xe5\x8d\x95'), (b'nm', b'\xe6\x99\xae\xe9\x80\x9a'), (b'hd', b'\xe5\x9b\xb0\xe9\x9a\xbe')]),
        ),
    ]
