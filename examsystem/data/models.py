#-*- coding: utf-8 -*-
from django.db import models

# Create your models here.
#question
class ChoiceQuestion(models.Model):
	"""docstring for Question_select"""
	question_text = models.CharField(max_length=200)
	CHOICES = ( ('A','A'),
				('B','B'),
				('C','C'),
				('D','D'),
			  )
	ans = models.CharField(max_length = 1,choices = CHOICES)
	DIFFCULTYS= (('ez','easy'),
				 ('nm','normal'),
				 ('hd','hard'),
				)
	diffculty = models.CharField(max_length = 2,choices = DIFFCULTYS)
	date = models.DateTimeField('date input',auto_now = True)
	def __unicode__(self):
		return self.question_text
class Choice(models.Model):
	"""docstring for ClassName"""
	question = models.ForeignKey(ChoiceQuestion)
	choice_text = models.CharField(max_length = 200)
	CHOICES = ( ('A','A'),
				('B','B'),
				('C','C'),
				('D','D'),
			  )
	number = models.CharField(max_length = 1,choices = CHOICES)
	def __unicode__(self):
		return self.choice_text
class FillQuestion(models.Model):
	question_text = models.CharField(max_length=200)
	ans = models.CharField(max_length = 200)
	DIFFCULTYS= (('ez','easy'),
				 ('nm','normal'),
				 ('hd','hard'),
				)
	diffculty = models.CharField(max_length = 2,choices = DIFFCULTYS)
	date = models.DateTimeField('date input',auto_now = True)
	def __unicode__(self):
		return self.question_text
#point&subject
class Point(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children")
    choicequestions= models.ManyToManyField(ChoiceQuestion,blank = True) 
    fillquestions = models.ManyToManyField(FillQuestion,blank = True) 
    def __unicode__(self):
        return self.name

#exam
class Exam(models.Model):
	name = models.CharField(max_length=50)
	subject = models.ForeignKey(Point)
	DIFFCULTYS= (('ez','easy'),
				 ('nm','normal'),
				 ('hd','hard'),
				)
	diffculty = models.CharField(max_length = 2,choices = DIFFCULTYS)
	choicequestions= models.ManyToManyField(ChoiceQuestion,through = 'ChoiceQuestionDetail',blank = True)
	fillquestions = models.ManyToManyField(FillQuestion,through = 'FillQuestionDetail',blank = True)
	date = models.DateTimeField('date_input',auto_now = True)
	def __unicode__(self):
		return self.name

class ChoiceQuestionDetail(models.Model):
	choicequestion = models.ForeignKey(ChoiceQuestion)
	exam = models.ForeignKey(Exam)
	mark = models.IntegerField()

class FillQuestionDetail(models.Model):
	choicequestion = models.ForeignKey(FillQuestion)
	exam = models.ForeignKey(Exam)
	mark = models.IntegerField()
#user
class Student(models.Model):
	name = models.CharField(max_length=10)
	num = models.CharField(max_length=15)
	age = models.IntegerField()
	SEX =(('m','男'),('f','女'),)
	sex = models.CharField(max_length = 1,choices = SEX)
	birth = models.DateField(blank = True)
	COLLEGE = (('计算机','计算机学院'),('软件','软件学院'),)
	college = models.CharField(max_length = 10,choices = COLLEGE)
	tel = models.CharField(max_length = 15,blank = True)
	email =models.EmailField(blank = True)
	def __unicode__(self):
		return self.name

class Teacher(models.Model):
	name = models.CharField(max_length=10)
	num = models.CharField(max_length=15)
	age = models.IntegerField()
	SEX =(('m','男'),('f','女'),)
	sex = models.CharField(max_length = 1,choices = SEX)
	birth = models.DateField(blank = True)
	COLLEGE = (('计算机','计算机学院'),('软件','软件学院'),)
	college = models.CharField(max_length = 10,choices = COLLEGE)
	tel = models.CharField(max_length = 15,blank = True)
	email =models.EmailField(blank = True)
	def __unicode__(self):
		return self.name