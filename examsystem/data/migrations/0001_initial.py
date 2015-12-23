# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('select_score', models.IntegerField(default=None, null=True)),
                ('fill_score', models.IntegerField(default=None, null=True)),
                ('tf_score', models.IntegerField(default=None, null=True)),
                ('sa_score', models.IntegerField(default=None, null=True)),
                ('score', models.IntegerField(default=None, null=True)),
                ('state', models.BooleanField(default=True)),
                ('date', models.DateTimeField(auto_now=True, verbose_name=b'date_input')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice_text', models.CharField(max_length=200)),
                ('number', models.CharField(max_length=1, choices=[(b'A', b'A'), (b'B', b'B'), (b'C', b'C'), (b'D', b'D')])),
            ],
        ),
        migrations.CreateModel(
            name='ChoiceQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_text', models.CharField(max_length=200)),
                ('ans', models.CharField(max_length=1, choices=[(b'A', b'A'), (b'B', b'B'), (b'C', b'C'), (b'D', b'D')])),
                ('diffculty', models.CharField(max_length=2, choices=[(b'ez', b'easy'), (b'nm', b'normal'), (b'hd', b'hard')])),
                ('date', models.DateTimeField(auto_now=True, verbose_name=b'date input')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChoiceQuestionAns',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ans', models.CharField(max_length=2, null=True)),
                ('state', models.NullBooleanField(default=None)),
                ('answer', models.ForeignKey(to='data.Answer')),
                ('choicequestion', models.ForeignKey(to='data.ChoiceQuestion')),
            ],
        ),
        migrations.CreateModel(
            name='ChoiceQuestionDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mark', models.IntegerField()),
                ('choicequestion', models.ForeignKey(to='data.ChoiceQuestion')),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('diffculty', models.CharField(max_length=2, choices=[(b'ez', b'easy'), (b'nm', b'normal'), (b'hd', b'hard')])),
                ('count', models.IntegerField(default=100)),
                ('date', models.DateTimeField(auto_now=True, verbose_name=b'date_input')),
                ('choicequestions', models.ManyToManyField(to='data.ChoiceQuestion', through='data.ChoiceQuestionDetail', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='FillQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_text', models.CharField(max_length=200)),
                ('ans', models.CharField(max_length=200)),
                ('diffculty', models.CharField(max_length=2, choices=[(b'ez', b'easy'), (b'nm', b'normal'), (b'hd', b'hard')])),
                ('date', models.DateTimeField(auto_now=True, verbose_name=b'date input')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FillQuestionAns',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ans', models.CharField(max_length=100, null=True)),
                ('state', models.NullBooleanField(default=None)),
                ('answer', models.ForeignKey(to='data.Answer')),
                ('fillquestion', models.ForeignKey(to='data.FillQuestion')),
            ],
        ),
        migrations.CreateModel(
            name='FillQuestionDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mark', models.IntegerField()),
                ('choicequestion', models.ForeignKey(to='data.FillQuestion')),
                ('exam', models.ForeignKey(to='data.Exam')),
            ],
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('choicequestions', models.ManyToManyField(to='data.ChoiceQuestion', blank=True)),
                ('fillquestions', models.ManyToManyField(to='data.FillQuestion', blank=True)),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='data.Point', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SAQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_text', models.CharField(max_length=200)),
                ('ans', models.CharField(max_length=200)),
                ('diffculty', models.CharField(max_length=2, choices=[(b'ez', b'easy'), (b'nm', b'normal'), (b'hd', b'hard')])),
                ('date', models.DateTimeField(auto_now=True, verbose_name=b'date input')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SAQuestionAns',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ans', models.CharField(max_length=200, null=True)),
                ('mark', models.IntegerField(default=10)),
                ('score', models.IntegerField(null=True)),
                ('state', models.NullBooleanField(default=None)),
                ('answer', models.ForeignKey(to='data.Answer')),
                ('saquestion', models.ForeignKey(to='data.SAQuestion')),
            ],
        ),
        migrations.CreateModel(
            name='SAQuestionDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mark', models.IntegerField()),
                ('exam', models.ForeignKey(to='data.Exam')),
                ('saquestion', models.ForeignKey(to='data.SAQuestion')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10, null=True)),
                ('num', models.CharField(max_length=15, null=True)),
                ('age', models.IntegerField(null=True)),
                ('sex', models.CharField(max_length=1, null=True, choices=[(b'm', b'\xe7\x94\xb7'), (b'f', b'\xe5\xa5\xb3')])),
                ('birth', models.DateField(null=True, blank=True)),
                ('college', models.CharField(max_length=10, null=True, choices=[(b'\xe8\xae\xa1\xe7\xae\x97\xe6\x9c\xba', b'\xe8\xae\xa1\xe7\xae\x97\xe6\x9c\xba\xe5\xad\xa6\xe9\x99\xa2'), (b'\xe8\xbd\xaf\xe4\xbb\xb6', b'\xe8\xbd\xaf\xe4\xbb\xb6\xe5\xad\xa6\xe9\x99\xa2')])),
                ('tel', models.CharField(max_length=15, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10, null=True)),
                ('num', models.CharField(max_length=15, null=True)),
                ('age', models.IntegerField(null=True)),
                ('sex', models.CharField(max_length=1, null=True, choices=[(b'm', b'\xe7\x94\xb7'), (b'f', b'\xe5\xa5\xb3')])),
                ('birth', models.DateField(null=True, blank=True)),
                ('college', models.CharField(blank=True, max_length=20, null=True, choices=[(b'sc', b'\xe8\xae\xa1\xe7\xae\x97\xe6\x9c\xba\xe5\xad\xa6\xe9\x99\xa2'), (b'sw', b'\xe8\xbd\xaf\xe4\xbb\xb6\xe5\xad\xa6\xe9\x99\xa2')])),
                ('tel', models.CharField(max_length=15, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('students', models.ManyToManyField(related_name='students', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('Type', models.CharField(max_length=10, choices=[(b'homework', b'homework'), (b'exam', b'exam')])),
                ('date', models.DateTimeField(auto_now=True)),
                ('exam', models.ForeignKey(default=None, to='data.Exam', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(related_name='STUDENT', to=settings.AUTH_USER_MODEL)),
                ('test', models.ForeignKey(to='data.Test')),
            ],
        ),
        migrations.CreateModel(
            name='TfQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_text', models.CharField(max_length=200)),
                ('ans', models.BooleanField()),
                ('diffculty', models.CharField(max_length=2, choices=[(b'ez', b'easy'), (b'nm', b'normal'), (b'hd', b'hard')])),
                ('date', models.DateTimeField(auto_now=True, verbose_name=b'date input')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TfQuestionAns',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ans', models.NullBooleanField()),
                ('state', models.NullBooleanField(default=None)),
                ('Tfquestion', models.ForeignKey(to='data.TfQuestion')),
                ('answer', models.ForeignKey(to='data.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='TfQuestionDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mark', models.IntegerField()),
                ('exam', models.ForeignKey(to='data.Exam')),
                ('tfquestion', models.ForeignKey(to='data.TfQuestion')),
            ],
        ),
        migrations.AddField(
            model_name='test',
            name='students',
            field=models.ManyToManyField(related_name='testlog', through='data.TestLog', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='test',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='point',
            name='saquestions',
            field=models.ManyToManyField(to='data.SAQuestion', blank=True),
        ),
        migrations.AddField(
            model_name='point',
            name='tfquestions',
            field=models.ManyToManyField(to='data.TfQuestion', blank=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='fillquestions',
            field=models.ManyToManyField(to='data.FillQuestion', through='data.FillQuestionDetail', blank=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='saquestions',
            field=models.ManyToManyField(to='data.SAQuestion', through='data.SAQuestionDetail', blank=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='subject',
            field=models.ForeignKey(to='data.Point'),
        ),
        migrations.AddField(
            model_name='exam',
            name='tfquestions',
            field=models.ManyToManyField(to='data.TfQuestion', through='data.TfQuestionDetail', blank=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='choicequestiondetail',
            name='exam',
            field=models.ForeignKey(to='data.Exam'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(to='data.ChoiceQuestion'),
        ),
        migrations.AddField(
            model_name='answer',
            name='Tfquestion',
            field=models.ManyToManyField(to='data.TfQuestion', through='data.TfQuestionAns'),
        ),
        migrations.AddField(
            model_name='answer',
            name='choicequestion',
            field=models.ManyToManyField(to='data.ChoiceQuestion', through='data.ChoiceQuestionAns'),
        ),
        migrations.AddField(
            model_name='answer',
            name='exam',
            field=models.ForeignKey(to='data.Exam'),
        ),
        migrations.AddField(
            model_name='answer',
            name='fillquestion',
            field=models.ManyToManyField(to='data.FillQuestion', through='data.FillQuestionAns'),
        ),
        migrations.AddField(
            model_name='answer',
            name='saquestion',
            field=models.ManyToManyField(to='data.SAQuestion', through='data.SAQuestionAns'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
