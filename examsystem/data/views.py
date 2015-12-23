#-*- coding: utf-8 -*- 
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout

from .forms import *
from .models import*

# Create your views here.
#setup
'''def setup():

'''
#questions
def HomePage(request):
    return render(request,'data/HomePage.html')
def get_choicequestion(request):
    if request.method == 'POST':
        form = ChoiceQuestionForm(request.POST)
        if form.is_valid():
            question = ChoiceQuestion(question_text = form.cleaned_data['question'],
                                    ans = form.cleaned_data['ans'],
                                    diffculty = form.cleaned_data['diffculty'],
                                    user = request.user)
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
            question = FillQuestion(question_text = form.cleaned_data['question'],
                                    ans = form.cleaned_data['ans'],
                                    diffculty = form.cleaned_data['diffculty'],
                                    user = request.user)
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
        else:
            point = Point.objects.all()[0]
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
    context = {'questions': questions,
                'style':style,
                'form':form}
    return render(request,'data/Questionlist.html',context)

#exam_teacher
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
            return HttpResponseRedirect(reverse('data:SelectQuestion', args=(pk,point,style)))
        else:
            print request.POST
            exam = Exam.objects.get(id = pk)
            if style == 'select':
                question = ChoiceQuestion.objects.get(id = request.POST['question_id'])
                temp = ChoiceQuestionDetail(exam = exam , choicequestion= question,mark = 0)
                temp.save()
            elif style == 'fill':
                question = FillQuestion.objects.get(id = request.POST['select'])
                temp = FillQuestionDetail(exam = exam , choicequestion= question,mark = 0)
                temp.save()
            #select question
    if point:
        point = Point.objects.get(name = point)
    else:
        point = Point.objects.all()[0]
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
    exam = Exam.objects.get(id = pk)
    choicequestions = ChoiceQuestionDetail.objects.filter(exam = exam)
    fillquestions = FillQuestionDetail.objects.filter(exam = exam)
    form = SearchQuestionForm(initial = {'point':point,'style':style})
    context = {'questions': questions,
            'style':style,
            'SelectQuestion':True,
            'form':form,
            'exam':exam,
            'choicequestions':choicequestions,
            'fillquestions':fillquestions}
    return render(request,'data/Questionlist.html',context)

def SetMark(request,pk):
    exam = Exam.objects.get(id = pk)
    choicequestions = ChoiceQuestionDetail.objects.filter(exam = exam)
    fillquestions = FillQuestionDetail.objects.filter(exam = exam)
    if request.method == 'POST':
        if 'submit' in request.POST:
            for question in choicequestions:
                pos =  str(question.id)
                question.mark = request.POST[pos]
                question.save()
            return  HttpResponse('success')
        return HttpResponse('fail')
    else:
        return render(request,'data/SetMark.html',{'exam':exam,
                                                'choicequestions':choicequestions,
                                                'fillquestions':fillquestions})
def ExamDetail(request,pk):
    exam = Exam.objects.get(id = pk)
    choicequestions = ChoiceQuestionDetail.objects.filter(exam = exam)
    fillquestions = FillQuestionDetail.objects.filter(exam = exam)
    return render(request,'data/ExamDetail.html',{'exam':exam,
                                                'choicequestions':choicequestions,
                                                'fillquestions':fillquestions})

def ExamList(request):
    exams = Exam.objects.all()
    return render(request,'data/ExamList.html',{'exams':exams})

#exam_student
def AnswerExam(request,pk):
    exam = Exam.objects.get(id = pk)
    choicequestions = ChoiceQuestionDetail.objects.filter(exam = exam)
    return render(request,'data/AnswerExam.html',{'exam':exam,
                                                'choicequestions':choicequestions})

def ExamResult(request,pk):
    if request.method ==  'POST':
        if 'save' in request.POST:
            exam = Exam.objects.get(id = pk)
            choicequestions = ChoiceQuestion.objects.filter(exam = exam)
            answer = Answer.objects.create(exam = exam,user = request.user)
            pos = 0
            anslist = request.session['anslist']
            for choicequestion in choicequestions:
                ans = ChoiceQuestionAns(answer = answer,
                                        choicequestion = choicequestion,
                                        ans = anslist[pos])
                ans.save()
                pos += 1
                
            return HttpResponse('success')
        else:
            exam = Exam.objects.get(id = pk)
            choicequestions = ChoiceQuestionDetail.objects.filter(exam = exam)
            anslist =  []
            resultlist = []
            score = 0
            num = 0
            for question in choicequestions:
                pos = str(question.id)
                if pos in request.POST:
                    ans = request.POST[pos]
                    anslist.append(ans)
                    num += question.mark
                    if ans == question.choicequestion.ans:
                        resultlist.append('right')
                        score += question.mark
                        print score
                    else:
                        resultlist.append('false')
                else:
                    anslist.append('null')
                request.session['anslist'] = anslist
            return render(request,'data/ExamResult.html',locals())   

def ResultList(request):
    character = request.user.groups.all()[0].name
    if character == 'student':
         answers = Answer.objects.filter(user = request.user)
    elif character == 'teacher':
        answers = Answer.objects.all()
    return render(request,'data/ResultList.html',{'answers':answers})
def ResultDetail(request,pk):
    answer = Answer.objects.get(id = pk)
    choicequestions = ChoiceQuestionDetail.objects.filter(exam = answer.exam)
    print(len(choicequestions))
    choicequestionans = ChoiceQuestionAns.objects.filter(answer = answer)
    anslist = []
    resultlist = []
    num = 0
    score = 0
    for ans in choicequestionans:
        choicequestiondetail =  choicequestions.get(choicequestion = ans.choicequestion)
        num += choicequestiondetail.mark
        if ans.choicequestion.ans == ans.ans:
            resultlist.append('right')
            score += choicequestiondetail.mark
        else:
            resultlist.append('false')
        anslist.append(ans.ans)
    return render(request,'data/ResultDetail.html',{'answer':answer,
                                                    'choicequestions':choicequestions,
                                                    'anslist':anslist,
                                                    'resultlist':resultlist,
                                                    'score':score,
                                                    'num':num})
#users
def StudentUpdate(request):
    if request.method == 'POST':
        form = StudentSignInForm(request.POST)
        if form.is_valid():
            student = Student.objects.filter(user = request.user.id).update(name = form.cleaned_data['name'],
                                                                        num = form.cleaned_data['num'],
                                                                        age = form.cleaned_data['age'],
                                                                        sex = form.cleaned_data['sex'],
                                                                        birth = form.cleaned_data['birth'],
                                                                        college = form.cleaned_data['college'],
                                                                        tel = form.cleaned_data['tel'],
                                                                        email = form.cleaned_data['email'])
            return HttpResponse('success')
    else:      
        form = StudentSignInForm(initial = {'name':request.user.username})
    character = request.user.groups.all()[0].name
    return render(request,'data/SignIn.html',{'form':form,'character':character})

def TeacherUpdate(request):
    if request.method == 'POST':
        form = TeacherSignInForm(request.POST)
        if form.is_valid():
            teacher = Teacher.objects.filter(user = request.user.id).update(name = form.cleaned_data['name'],
                                                                        num = form.cleaned_data['num'],
                                                                        age = form.cleaned_data['age'],
                                                                        sex = form.cleaned_data['sex'],
                                                                        birth = form.cleaned_data['birth'],
                                                                        college = form.cleaned_data['college'],
                                                                        tel = form.cleaned_data['tel'],
                                                                        email = form.cleaned_data['email'])
            return HttpResponse('success')
    else:  
        form = TeacherSignInForm(initial = {'name':request.user.username})
    character = request.user.groups.all()[0].name
    return render(request,'data/SignIn.html',{'form':form,'character':character})

def NewUser(request):
    if request.method == 'POST':
        form = NewUserSignInForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'],
                                            'hori@sina.com',
                                            form.cleaned_data['password'])
            user.groups = [form.cleaned_data['group']] 
        user = authenticate(username=form.cleaned_data['username'], 
                            password=form.cleaned_data['password'])
        login(request, user)
        character = request.user.groups.all()[0].name
        if character == 'student':
            student = Student.objects.create(name = form.cleaned_data['username'],
                                            user = request.user,)
        elif character == 'teacher':
            teacher = Teacher.objects.create(name = form.cleaned_data['username'],
                                            user = request.user,)
        return HttpResponseRedirect('/data/RegesteSuccess/')
    else:
        form = NewUserSignInForm()
    return  render(request,'data/NewUser.html',{'form':form})

def RegesteSuccess(request):
    character = request.user.groups.all()[0].name
    context = {'character':character}
    return render(request,'data/RegesteSuccess.html',context)

def Login(request):
    if request.method == 'POST':
        form = NewUserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], 
                                password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    message = "User is valid, active and authenticated"
                    return HttpResponseRedirect('/data/HomePage/')
                else:
                    message = "The password is valid, but the account has been disabled!"
            else:
                message = "The username and password were incorrect."
            return HttpResponse(message)
    else:
        form = NewUserLoginForm()
    return  render(request,'data/Login.html',{'form':form})

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/data/welcome/')

def UserDetail(request,pk):
    if not request.user.is_authenticated():
        form = NewUserLoginForm()
        return HttpResponseRedirect('/data/Login/')
    user = User.objects.get(id = pk)
    if request.user.groups.all()[0].name == 'student':
        detail = Student.objects.get(user = request.user)
    elif request.user.groups.all()[0].name == 'teacher':
        detail = Teacher.objects.get(user = request.user)
    context= {'detail':detail,'user':user}
    return render(request,'data/UserDetail.html',context)

#common views
def welcome(request):
    return render(request,'data/welcome.html')

def HomePage(request):
    character = request.user.groups.all()[0].name
    print character
    return render(request,'data/HomePage.html',{'character':character})
