#-*- coding: utf-8 -*- 
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import *
from .models import*

# Create your views here.
#questions
def get_choicequestion(request):
    if request.method == 'POST':
        form = ChoiceQuestionForm(request.POST)
        if form.is_valid():
            question = ChoiceQuestion(question_text = form.cleaned_data['question'],ans = form.cleaned_data['ans'],
                                diffculty = form.cleaned_data['diffculty'])
            question.save()
            point = Point.objects.get(name = form.cleaned_data['point'])
            point.choicequestions.add(question)
            Choice.objects.create(number = 'A',choice_text = form.cleaned_data['choiceA'],question = question)
            Choice.objects.create(number = 'B',choice_text = form.cleaned_data['choiceB'],question = question)
            Choice.objects.create(number = 'C',choice_text = form.cleaned_data['choiceC'],question = question)
            Choice.objects.create(number = 'D',choice_text = form.cleaned_data['choiceD'],question = question)
            return HttpResponse('thanks')
    else:
        form = ChoiceQuestionForm()
    return render(request,'data/GetQuestion.html',{'form':form})

def get_fillquestion(request):
    if request.method == 'POST':
        form = FillQuestionForm(request.POST)
        if form.is_valid():
            question = FillQuestion(question_text = form.cleaned_data['question'],ans = form.cleaned_data['ans'],
                                diffculty = form.cleaned_data['diffculty'])
            question.save()
            point = Point.objects.get(name = form.cleaned_data['point'])
            point.fillquestions.add(question)
            return HttpResponse('thanks')
    else:
        form = FillQuestionForm()
    return render(request,'data/GetQuestion.html',{'form':form})

def Questionlist(request,point = None,style = 'select'):
    if request.method == 'POST':
        form = SearchQuestionForm(request.POST)
        if form.is_valid():
            style = form.cleaned_data['style']
            point = form.cleaned_data['point']
            return HttpResponseRedirect(reverse('data:Questionlist', args=(point,style)))
    else:
        if point:
            point = Point.objects.get(name = point)
        if style == 'select':
            if point == None:
                questions= ChoiceQuestion.objects.all()
            else:
                questions = ChoiceQuestion.objects.filter(point = point)
        elif style =='fill':
            if point == None:
                questions = FillQuestion.objects.all()
            else:
                questions = FillQuestion.objects.filter(point = point)
        paginator = Paginator(questions, 2) # Show 25 contacts per page
        page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    form = SearchQuestionForm(initial = {'point':point,'style':style})
    context = {'questions': questions,'style':style,'form':form}
    return render(request,'data/Questionlist.html',context)

'''def SearchQuestion(request,pagenum="1",style = "select",point = u"数学"):
    questioncount = 2
    form = SearchQuestionForm()
    if request.method == 'POST':
        form = SearchQuestionForm(request.POST)
        if 'nextpage' in request.POST:
            pagenum = int(pagenum)
            pagenum += 1
            return HttpResponseRedirect(reverse('data:search_question', args=(point,style,pagenum)))
        if 'jumppage' in request.POST:
            pagenum = request.POST['jumppage']
            return HttpResponseRedirect(reverse('data:search_question', args=(point,style,pagenum)))
        if form.is_valid():
            point = form.cleaned_data['point']
            style = form.cleaned_data['style']
            pagenum = int(pagenum)
            pagenum = 1
            return HttpResponseRedirect(reverse('data:search_question', args=(point,style,pagenum)))
    else:
        point = Point.objects.get(name = point)
        pagenum = int(pagenum)
    choicequestions = point.choicequestions.all()[0+(pagenum-1)*questioncount:questioncount*pagenum]
    fillquestions = point.fillquestions.all()[0+(pagenum-1)*questioncount:questioncount*pagenum]
    if style  == 'select':
        if len(point.choicequestions.all())%questioncount == 0:
            maxpagenum = len(point.choicequestions.all())/questioncount
        else:
            maxpagenum = len(point.choicequestions.all())/questioncount+1
    elif style == 'fill':
        if len(point.choicequestions.all())%questioncount==0:
            maxpagenum = len(point.choicequestions.all())/questioncount
        else:
            maxpagenum = len(point.choicequestions.all())/questioncount+1
    pagelist = []
    for i in range(1,maxpagenum+1):
        pagelist.append(i)
    context = {'form':form,'style':style,'choicequestions':choicequestions,'fillquestions':fillquestions,'pagenum':pagenum,'pagelist':pagelist}
    return render(request,'data/SearchQuestion.html',context)'''
#exam
def AddExam(request):   
    if request.method == 'POST':
        form = AddExamForm(request.POST)
        if form.is_valid():
            exam = form.save()
        return HttpResponseRedirect(reverse('data:SelectQuestion', args=(exam.id,)))
    else:
        form = AddExamForm()
    return render(request,'data/AddExam.html',{'form':form})
def SelectQuestion(request,pk,point = None,style = 'select'):
    if request.method == 'POST':
        form = SearchQuestionForm(request.POST)
        if form.is_valid():
            style = form.cleaned_data['style']
            point = form.cleaned_data['point']
            # 
            if 'select' not in request.POST:
                return HttpResponseRedirect(reverse('data:SelectQuestion', args=(pk,point,style)))
            else:
                exam = Exam.objects.get(id = pk)
                if style == 'select':
                    question = ChoiceQuestion.objects.get(id = request.POST['select'])
                    temp = ChoiceQuestionDetail(exam = exam , choicequestion= question,mark = 0)
                    temp.save()
                elif style == 'fill':
                    question = FillQuestion.objects.get(id = request.POST['select'])
                    temp = FillQuestionDetail(exam = exam , choicequestion= question,mark = 0)
                    temp.save()
            #select question
    if point:
        point = Point.objects.get(name = point)
    if style == 'select':
        if point == None:
            questions= ChoiceQuestion.objects.all()
        else:
            questions = ChoiceQuestion.objects.filter(point = point)
    elif style =='fill':
        if point == None:
            questions = FillQuestion.objects.all()
        else:
            questions = FillQuestion.objects.filter(point = point)
    paginator = Paginator(questions, 2) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    form = SearchQuestionForm(initial = {'point':point,'style':style})
    context = {'questions': questions,'style':style,'SelectQuestion':True,'form':form}
    return render(request,'data/Questionlist.html',context)

def ExamDetail(request,pk):
    exam = Exam.objects.get(id = pk)
    choicequestions = ChoiceQuestionDetail.objects.filter(exam = exam)
    fillquestions = FillQuestionDetail.objects.filter(exam = exam)
    return render(request,'data/ExamDetail.html',{'exam':exam,'choicequestions':choicequestions,'fillquestions':fillquestions})

def ExamList(request):
    exams = Exam.objects.all()
    return render(request,'data/ExamList.html',{'exams':exams})

#users
def StudentSignIn(request):
    if request.method == 'POST':
        form = StudentSignInForm(request.POST)
        if form.is_valid():
            student = Student.objects.create(name = form.cleaned_data['name'],num = form.cleaned_data['num'],
                                   age = form.cleaned_data['age'],sex = form.cleaned_data['sex'],
                                   birth = form.cleaned_data['birth'],college = form.cleaned_data['college'],
                                   tel = form.cleaned_data['tel'],email = form.cleaned_data['email'])
            return HttpResponse('success')
    else:      
        form = StudentSignInForm()
    return render(request,'data/SignIn.html',{'form':form})

def TeacherSignIn(request):
    if request.method == 'POST':
        form = TeacherSignInForm(request.POST)
        if form.is_valid():
            student = Teacher.objects.create(name = form.cleaned_data['name'],num = form.cleaned_data['num'],
                                   age = form.cleaned_data['age'],sex = form.cleaned_data['sex'],
                                   birth = form.cleaned_data['birth'],college = form.cleaned_data['college'],
                                   tel = form.cleaned_data['tel'],email = form.cleaned_data['email'])
            return HttpResponse('success')
    else:      
        form = TeacherSignInForm()
    return render(request,'data/SignIn.html',{'form':form})