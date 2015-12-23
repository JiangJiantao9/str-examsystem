# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_student_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='diffculty',
            field=models.CharField(max_length=2, verbose_name=b'\xe9\x9a\xbe\xe5\xba\xa6', choices=[(b'ez', b'\xe7\xae\x80\xe5\x8d\x95'), (b'nm', b'\xe6\x99\xae\xe9\x80\x9a'), (b'hd', b'\xe5\x9b\xb0\xe9\x9a\xbe')]),
        ),
        migrations.AlterField(
            model_name='exam',
            name='name',
            field=models.CharField(max_length=50, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='subject',
            field=models.ForeignKey(verbose_name=b'\xe5\xad\xa6\xe7\xa7\x91', to='data.Point'),
        ),
        migrations.AlterField(
            model_name='saquestion',
            name='ans',
            field=models.CharField(max_length=200, verbose_name=b'\xe7\xad\x94\xe6\xa1\x88'),
        ),
        migrations.AlterField(
            model_name='saquestion',
            name='diffculty',
            field=models.CharField(max_length=2, verbose_name=b'\xe9\x9a\xbe\xe5\xba\xa6', choices=[(b'ez', b'easy'), (b'nm', b'normal'), (b'hd', b'hard')]),
        ),
        migrations.AlterField(
            model_name='saquestion',
            name='question_text',
            field=models.CharField(max_length=200, verbose_name=b'\xe9\xa2\x98\xe5\xb9\xb2'),
        ),
        migrations.AlterField(
            model_name='test',
            name='Type',
            field=models.CharField(max_length=10, verbose_name=b'\xe7\xb1\xbb\xe5\x88\xab', choices=[(b'homework', b'\xe4\xbd\x9c\xe4\xb8\x9a'), (b'exam', b'\xe6\xb5\x8b\xe8\xaf\x95')]),
        ),
        migrations.AlterField(
            model_name='test',
            name='name',
            field=models.CharField(max_length=50, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0'),
        ),
        migrations.AlterField(
            model_name='tfquestion',
            name='ans',
            field=models.BooleanField(verbose_name=b'\xe7\xad\x94\xe6\xa1\x88'),
        ),
        migrations.AlterField(
            model_name='tfquestion',
            name='diffculty',
            field=models.CharField(max_length=2, verbose_name=b'\xe9\x9a\xbe\xe5\xba\xa6', choices=[(b'ez', b'easy'), (b'nm', b'normal'), (b'hd', b'hard')]),
        ),
        migrations.AlterField(
            model_name='tfquestion',
            name='question_text',
            field=models.CharField(max_length=200, verbose_name=b'\xe9\xa2\x98\xe5\xb9\xb2'),
        ),
    ]
