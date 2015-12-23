#-*- coding: utf-8 -*- 
from django import forms
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

from .models import *
from django.contrib.auth.models import Group

#QuestionForm
class ChoiceQuestionForm(forms.Form):
    point = forms.ModelChoiceField(label='知识点',queryset=Point.objects.all())
    question = forms.CharField(label='题干', max_length=100,widget=forms.Textarea(attrs={'cols':'110','rows':'5'}))
    choiceA = forms.CharField(label='A', max_length=100)
    choiceB = forms.CharField(label='B', max_length=100)
    choiceC = forms.CharField(label='C', max_length=100)
    choiceD = forms.CharField(label='D', max_length=100)
    CHOICES = ( ('A','A'),
				('B','B'),
				('C','C'),
				('D','D'),
			  )
    ans = forms.ChoiceField(label = '答案',choices = CHOICES)
    DIFFCULTYS= (('ez','简单'),
				 ('nm','普通'),
				 ('hd','困难'),
				)
    diffculty = forms.ChoiceField(label = '难度',choices = DIFFCULTYS)

class FillQuestionForm(forms.Form):
	point = forms.ModelChoiceField(label='知识点',queryset=Point.objects.all())
	question = forms.CharField(label='题干', max_length=100,widget=forms.Textarea(attrs={'cols':'110','rows':'5'}))
	ans =  forms.CharField(label='答案', max_length=100)
  	DIFFCULTYS= (('ez','简单'),
				 ('nm','普通'),
				 ('hd','困难'),
				)
	diffculty = forms.ChoiceField(label = '难度',choices = DIFFCULTYS)

class TfQuestionForm(ModelForm):
	point = forms.ModelChoiceField(label='知识点',queryset=Point.objects.all())
	class Meta:
		model = TfQuestion
		fields = ['question_text','ans','diffculty']
		widgets = {
         	'question_text':forms.Textarea(attrs={'cols':'110','rows':'5'})
        		}
class SAQuestionForm(ModelForm):
	point = forms.ModelChoiceField(label='知识点',queryset=Point.objects.all())
	class Meta:
		model = SAQuestion
		fields = ['question_text','ans','diffculty']
		widgets = {
         	'question_text':forms.Textarea(attrs={'cols':'110','rows':'5'})
        		}
class SearchQuestionForm(forms.Form):
	point = forms.ModelChoiceField(label='知识点',queryset=Point.objects.all(),required = False)
	STYLE = (('select','选择题'),('fill','填空题'),('tf','判断题'),('sa','简答题'))
	style = forms.ChoiceField(label = '题型',choices = STYLE)
	question_keyword = forms.CharField(label = '题目关键词',max_length = 100,required=False)

#exam
class AddExamForm(ModelForm):
	count = forms.IntegerField(label='总分')
	class Meta:
		model = Exam
		fields = ['name','subject','diffculty']
		'''widgets = {
            'fillquestions': CheckboxSelectMultiple(),
            'choicequestions':CheckboxSelectMultiple(),
        		}'''

class SearchExamForm(forms.Form):
	name = forms.CharField(label = '名称',max_length = 20,required = False)
	subject = forms.ModelChoiceField(label = '知识点',queryset = Point.objects.all(),required =False)
	DIFFCULTYS= (('ez','简单'),
				 ('nm','普通'),
				 ('hd','困难'),
				 ('all','全部')
				)
	diffculty = forms.ChoiceField(label = '难度',choices = DIFFCULTYS)
	state = forms.BooleanField(label = '是否可见',required = False)

class SearchAnswerForm(forms.Form):
	name = forms.CharField(label = '名称',max_length = 20,required = False)
	author = forms.CharField(label = '答题者',max_length = 20,required = False)

#test
class NewTestForm(ModelForm):
	class Meta:
		model = Test
		fields =['name','Type']

class TestSearchForm(forms.Form):
	name = forms.CharField(label = '名称',max_length = 50,required = False)
	user = forms.CharField(label = '使用者',max_length = 30,required = False)
	TYPE =(('homework','作业'),
			('exam','考试'))
	Type = forms.ChoiceField(label = '事件类型',choices = TYPE,required = False)
#user
class StudentSignInForm(forms.Form):
	name = forms.CharField(label='用户名', max_length=10)
	num = forms.CharField(label='学号', max_length=15)
	age = forms.IntegerField(label = '年龄')
	SEX =(('m','男'),('f','女'),)
	sex = forms.ChoiceField(label = '性别',choices = SEX)
	birth = forms.DateField(label ='生日',required=False)
	COLLEGE = (('计算机','计算机学院'),('软件','软件学院'),)
	college = forms.ChoiceField(label = '学院',choices = COLLEGE)
	tel = forms.CharField(label = '电话',max_length = 15,required=False)
	email =forms.EmailField(label = 'email',required=False)

class TeacherSignInForm(forms.Form):
	name = forms.CharField(label='用户名', max_length=10)
	num = forms.CharField(label='教职工号', max_length=15)
	age = forms.IntegerField(label = '年龄')
	SEX =(('m','男'),('f','女'),)
	sex = forms.ChoiceField(label = '性别',choices = SEX)
	birth = forms.DateField(label ='生日',required=False)
	COLLEGE = (('计算机','计算机学院'),('软件','软件学院'),)
	college = forms.ChoiceField(label = '学院',choices = COLLEGE)
	tel = forms.CharField(label = '电话',max_length = 15,required=False)
	email =forms.EmailField(label = 'email',required=False)

class NewUserSignInForm(forms.Form):
	username = forms.CharField(label = '用户名',max_length = 30)
	password = forms.CharField(label = '密码',max_length = 10,widget=forms.PasswordInput)
	GROUPS = (('teacher','教师'),('student','学生'))
	group = forms.ModelChoiceField(label = '身份',queryset=Group.objects.all())

class NewUserLoginForm(forms.Form):
	username = forms.CharField(label = '用户名',max_length = 30)
	password = forms.CharField(label = '密码',max_length = 10,widget=forms.PasswordInput)

class ChooseTeacherForm(forms.Form):
	name = forms.CharField(label = '姓名',max_length = 30 ,required=False)
	subject = forms.CharField(label = '学院',max_length = 30,required = False)