#-*- coding: utf-8 -*- 
from django import forms
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

from .models import *

#QuestionForm
class ChoiceQuestionForm(forms.Form):
    point = forms.ModelChoiceField(label='point',queryset=Point.objects.all())
    question = forms.CharField(label='question', max_length=100)
    choiceA = forms.CharField(label='A', max_length=100)
    choiceB = forms.CharField(label='B', max_length=100)
    choiceC = forms.CharField(label='C', max_length=100)
    choiceD = forms.CharField(label='D', max_length=100)
    CHOICES = ( ('A','A'),
				('B','B'),
				('C','C'),
				('D','D'),
			  )
    ans = forms.ChoiceField(label = 'ans',choices = CHOICES)
    DIFFCULTYS= (('ez','easy'),
				 ('nm','normal'),
				 ('hd','hard'),
				)
    diffculty = forms.ChoiceField(label = 'diffculty',choices = DIFFCULTYS)

class FillQuestionForm(forms.Form):
	point = forms.ModelChoiceField(label='point',queryset=Point.objects.all())
	question = forms.CharField(label='question', max_length=100)
	ans =  forms.CharField(label='ans', max_length=100)
	DIFFCULTYS= (('ez','easy'),
			 ('nm','normal'),
			 ('hd','hard'),
			)
	diffculty = forms.ChoiceField(label = 'diffculty',choices = DIFFCULTYS)

class SearchQuestionForm(forms.Form):
	point = forms.ModelChoiceField(label='point',queryset=Point.objects.all())
	STYLE = (('select','select'),('fill','fill'))
	style = forms.ChoiceField(label = 'style',choices = STYLE)

#exam
class AddExamForm(ModelForm):
	#count = forms.IntegerField(label='count')
	class Meta:
		model = Exam
		fields = ['name','subject','diffculty']
		'''widgets = {
            'fillquestions': CheckboxSelectMultiple(),
            'choicequestions':CheckboxSelectMultiple(),
        		}'''

class SearchExamForm(forms.Form):
	name = forms.CharField(label = 'name',max_length = 20)
	subject = forms.ModelChoiceField(label = 'subject',queryset = Point.objects.all(),required = False)
	DIFFCULTYS= (('ez','easy'),
				 ('nm','normal'),
				 ('hd','hard'),
				)
	diffculty = forms.ChoiceField(label = 'diffculty',choices = DIFFCULTYS)

#user
class StudentSignInForm(forms.Form):
	name = forms.CharField(label='name', max_length=10)
	num = forms.CharField(label='num', max_length=15)
	age = forms.IntegerField(label = 'age')
	SEX =(('m','男'),('f','女'),)
	sex = forms.ChoiceField(label = 'sex',choices = SEX)
	birth = forms.DateField(label ='birth',required=False)
	COLLEGE = (('计算机','计算机学院'),('软件','软件学院'),)
	college = forms.ChoiceField(label = 'college',choices = COLLEGE)
	tel = forms.CharField(label = 'tel',max_length = 15,required=False)
	email =forms.EmailField(label = 'email',required=False)

class TeacherSignInForm(forms.Form):
	name = forms.CharField(label='name', max_length=10)
	num = forms.CharField(label='num', max_length=15)
	age = forms.IntegerField(label = 'age')
	SEX =(('m','男'),('f','女'),)
	sex = forms.ChoiceField(label = 'sex',choices = SEX)
	birth = forms.DateField(label ='birth',required=False)
	COLLEGE = (('计算机','计算机学院'),('软件','软件学院'),)
	college = forms.ChoiceField(label = 'college',choices = COLLEGE)
	tel = forms.CharField(label = 'tel',max_length = 15,required=False)
	email =forms.EmailField(label = 'email',required=False)