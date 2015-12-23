#-*- coding: utf-8 -*- 
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^choiceQ/', views.get_choicequestion, name='get_choicequestion'),
    url(r'^fillQ/', views.get_fillquestion, name='get_fillquestion'),
    url(r'^Questionlist/$', views.Questionlist, name='Questionlist'),
    url(r'^Questionlist/(?P<point>[^/]+)/(?P<style>[a-z]+)/$', views.Questionlist, name='Questionlist'),
   #url(r'^SearchQuestion/$', views.SearchQuestion, name='search_question'),
   #url(r'^SearchQuestion/(?P<point>[^/]+)/(?P<style>[a-z]+)/(?P<pagenum>[0-9]+)/$', views.SearchQuestion, name='search_question'),
    url(r'^StudentSignIn/$', views.StudentSignIn, name='StudentSignIn'),
    url(r'^TeacherSignIn/$', views.TeacherSignIn, name='TeacherSignIn'),
    url(r'^AddExam/$',views.AddExam,name = 'AddExam'),
    url(r'^AddExam/(?P<pk>[^/]+)/Questionlist/$',views.SelectQuestion,name = 'SelectQuestion'),
    url(r'^AddExam/(?P<pk>[^/]+)/Questionlist/(?P<point>[^/]+)/(?P<style>[a-z]+)/$', views.SelectQuestion, name='SelectQuestion'),
    url(r'^ExamList/$',views.ExamList,name = 'ExamList'),
    url(r'^ExamDetail/(?P<pk>[0-9]+)/$',views.ExamDetail,name = 'ExamDetail'),

    ]

