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
#method
def FindAllChildren(points):
    childlist = list('')
    for point in points:
        childlist.append(point)
        childs = point.children.all()
        if len(childs) > 0:
            childlist += FindAllChildren(point.children.all())
    return childlist

#questions
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
            return render(request,'data/Success.html')
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
            return render(request,'data/Success.html')
    else:
        form = FillQuestionForm()
    return render(request,'data/GetQuestion.html',{'form':form})

def get_tfquestion(request):
    if request.method =='POST':
        form = TfQuestionForm(request.POST)
        if form.is_valid():
            question = TfQuestion.objects.create(question_text = form.cleaned_data['question_text'],
                                                ans = form.cleaned_data['ans'],
                                                diffculty =form.cleaned_data['diffculty'],
                                                user =  request.user)
            point = Point.objects.get(name = form.cleaned_data['point'])
            point.tfquestions.add(question)
            return render(request,'data/Success.html')
    else:
        form = TfQuestionForm()
    return render(request,'data/GetQuestion.html',{'form':form})

def get_saquestion(request):
    if request.method =='POST':
        form = SAQuestionForm(request.POST)
        if form.is_valid():
            question = SAQuestion.objects.create(question_text = form.cleaned_data['question_text'],
                                                ans = form.cleaned_data['ans'],
                                                diffculty =form.cleaned_data['diffculty'],
                                                user =  request.user)
            point = Point.objects.get(name = form.cleaned_data['point'])
            point.saquestions.add(question)
            return render(request,'data/Success.html')
    else:
        form = SAQuestionForm()
    return render(request,'data/GetQuestion.html',{'form':form})

def Questionlist(request):
    #执行题目字段搜索
    if request.method == 'POST':
        form = SearchQuestionForm(request.POST)
        if form.is_valid():
            request.session['question_keyword'] =form.cleaned_data['question_keyword']
            request.session['question_point'] = form.cleaned_data['point'].name
            request.session['question_style']  = form.cleaned_data['style']
        return HttpResponseRedirect(reverse('data:Questionlist'))
    else:
        #知识点初始化/读入
        point = request.session['question_point']
        if point:
            point = Point.objects.filter(name = point)
            pointlist = FindAllChildren(point)
        else:
            point = Point.objects.all()[0]
            pointlist = FindAllChildren([point])
        #题型确定，执行知识点搜索
        style = request.session['question_style']
        questions = []
        if style == 'select':
            for point in pointlist:
                questions += point.choicequestions.all()
        elif style =='fill':
            for point in pointlist:
                questions += point.fillquestions.all()
        elif style == 'tf':
            for point in pointlist:
                questions += point.tfquestions.all()
        elif style == 'sa':
            for point in pointlist:
                questions += point.saquestions.all()
        #关键字确定,关键字搜索
        question_keyword =  request.session['question_keyword']
        if question_keyword:
            questions = questions.filter(question_text__contains = question_keyword)
        #分页
        paginator = Paginator(questions, 2) # Show 2 contacts per page
        page = request.GET.get('page')
        try:
            questions = paginator.page(page)
        except PageNotAnInteger:
            questions = paginator.page(1)
        except EmptyPage:
            questions = paginator.page(paginator.num_pages)
        #form
        form = SearchQuestionForm(initial = {'point':pointlist[0],
                                            'style':style,
                                            'question_keyword':request.session['question_keyword']})
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
            exam.user = request.user
            exam.save()
        return HttpResponseRedirect(reverse('data:SelectQuestion', args=(exam.id,)))
    else:
        form = AddExamForm(initial ={'count':100})
    return render(request,'data/AddExam.html',{'form':form})

def SelectQuestion(request,pk,point = None,style = 'select'):
    if request.method == 'POST':
        form = SearchQuestionForm(request.POST)
        if form.is_valid():
            style = form.cleaned_data['style']
            point = form.cleaned_data['point']
            return HttpResponseRedirect(reverse('data:SelectQuestion', args=(pk,point,style)))
        else:
            exam = Exam.objects.get(id = pk)
            if style == 'select':
                question = ChoiceQuestion.objects.get(id = request.POST['question_id'])
                if question not in exam.choicequestions.all():
                    temp = ChoiceQuestionDetail(exam = exam , choicequestion= question,mark = 0)
                    temp.save()
            elif style == 'fill':
                question = FillQuestion.objects.get(id = request.POST['question_id'])
                if question not in exam.fillquestions.all():
                    temp = FillQuestionDetail(exam = exam , choicequestion= question,mark = 0)
                    temp.save()
            elif style == 'tf':
                question = TfQuestion.objects.get(id = request.POST['question_id'])
                if question not in exam.tfquestions.all():
                    temp = TfQuestionDetail(exam = exam , tfquestion= question,mark = 0)
                    temp.save()
            elif style == 'sa':
                question = SAQuestion.objects.get(id = request.POST['question_id'])
                if question not in exam.saquestions.all():
                    temp = SAQuestionDetail(exam = exam , saquestion= question,mark = 0)
                    temp.save()       
    #select question
    #知识点读入
    if point:
        point = Point.objects.filter(name = point)
        pointlist = FindAllChildren(point)
    else:
        point = Point.objects.all()[0]
        pointlist = FindAllChildren([point])
    #题型确定
    questions = []
    if style == 'select':
        for point in pointlist:
            questions += point.choicequestions.all()
    elif style =='fill':
        if point == None:
            questions = FillQuestion.objects.all()
        else:
            for point in pointlist:
                questions += point.fillquestions.all()
    elif style =='tf':
        if point == None:
            questions = TfQuestion.objects.all()
        else:
            for point in pointlist:
                questions += point.tfquestions.all()
    elif style =='sa':
        if point == None:
            questions = SAQuestion.objects.all()
        else:
            for point in pointlist:
                questions += point.saquestions.all()
    #分页
    paginator = Paginator(questions, 2) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    #渲染
    exam = Exam.objects.get(id = pk)
    choicequestions = ChoiceQuestionDetail.objects.filter(exam = exam)
    fillquestions = FillQuestionDetail.objects.filter(exam = exam)
    tfquestions = TfQuestionDetail.objects.filter(exam = exam)
    saquestions = SAQuestionDetail.objects.filter(exam = exam)
    form = SearchQuestionForm(initial = {'point':pointlist[0],'style':style})
    context = {'questions': questions,
            'style':style,
            'SelectQuestion':True,
            'form':form,
            'exam':exam,
            'choicequestions':choicequestions,
            'fillquestions':fillquestions,
            'tfquestions':tfquestions,
            'saquestions':saquestions}
    return render(request,'data/Questionlist.html',context)

def SetMark(request,pk):
    exam = Exam.objects.get(id = pk)
    count = exam.count
    choicequestions = ChoiceQuestionDetail.objects.filter(exam = exam)
    fillquestions = FillQuestionDetail.objects.filter(exam = exam)
    tfquestions=TfQuestionDetail.objects.filter(exam = exam)
    saquestions=SAQuestionDetail.objects.filter(exam = exam)
    if request.method == 'POST':
        if 'submit' in request.POST:
            SUM = 0
            for question in choicequestions:
                pos =  'select' + str(question.id)
                question.mark = int(request.POST[pos])
                question.save()
                SUM += question.mark
            for question in fillquestions:
                pos =  'fill' + str(question.id)
                question.mark = int(request.POST[pos])
                question.save()
                SUM += question.mark
            for question in tfquestions:
                pos = 'tf'+str(question.id)
                question.mark = int(request.POST[pos])
                question.save()
                SUM += question.mark
            for question in saquestions:
                pos = 'sa'+str(question.id)
                question.mark = int(request.POST[pos])
                question.save()
                SUM += question.mark
            if count == SUM:
               return render(request,'data/Success.html')
            elif count < SUM:
                state = 'high'
            elif count > SUM:
                state = 'low'
        return render(request,'data/verify_SetMark.html',{'exam':exam,
                                                        'state':state,
                                                        'count':count,
                                                        'SUM':SUM})
    else:
        return render(request,'data/SetMark.html',{'exam':exam,
                                                'choicequestions':choicequestions,
                                                'fillquestions':fillquestions,
                                                'tfquestions':tfquestions,
                                                'saquestions':saquestions})
def ExamDetail(request,pk):
    exam = Exam.objects.get(id = pk)
    choicequestions = ChoiceQuestionDetail.objects.filter(exam = exam)
    fillquestions = FillQuestionDetail.objects.filter(exam = exam)
    tfquestions = TfQuestionDetail.objects.filter(exam = exam)
    saquestions = SAQuestionDetail.objects.filter(exam = exam)
    return render(request,'data/ExamDetail.html',{'exam':exam,
                                                'choicequestions':choicequestions,
                                                'fillquestions':fillquestions,
                                                'tfquestions':tfquestions,
                                                'saquestions':saquestions})

def ExamList(request):
    if request.method == 'POST':
        form = SearchExamForm(request.POST)
        if form.is_valid():
            request.session['exam_name'] = form.cleaned_data['name']
            request.session['exam_diffculty'] = form.cleaned_data['diffculty']
            request.session['exam_state'] = form.cleaned_data['state']
            if form.cleaned_data['subject']:
                request.session['exam_point'] = form.cleaned_data['subject'].name
        return HttpResponseRedirect(reverse('data:ExamList'))
    else:
        #筛选
        point = request.session['exam_point']
        diffculty = request.session['exam_diffculty']
        name = request.session['exam_name']
        state = request.session['exam_state']
        if point:
            point = Point.objects.get(name = point)
            exams = Exam.objects.filter(subject = point)
        else:
            exams = Exam.objects.all()
        if diffculty != 'all':
            exams = exams.filter(diffculty = diffculty)
        if name:
            exams = exams.filter(name__contains = name)
        if state:
            exams = exams.filter(state = state)
        if not request.user.has_perm('data.add_choicequestion'):
            exams = exams.filter(state = True)
        exams = exams.order_by("-date")
        #分页
        paginator = Paginator(exams, 7) # Show 10 contacts per page
        page = request.GET.get('page')
        try:
            exams = paginator.page(page)
        except PageNotAnInteger:
            exams = paginator.page(1)
        except EmptyPage:
            exams = paginator.page(paginator.num_pages)
        #form
        form = SearchExamForm(initial = {'name':name,
                                        'subject':point,
                                        'diffculty':diffculty,
                                        'state':state})
        return render(request,'data/ExamList.html',{'exams':exams,
                                                    'form':form})

def SetExamVisiable(request,pk):
    exam = Exam.objects.get(id = pk)
    exam.state = True
    exam.save()
    return render(request,'data/Success.html')
#exam_student
def AnswerExam(request,pk):
    exam = Exam.objects.get(id = pk)
    choicequestions = ChoiceQuestionDetail.objects.filter(exam = exam)
    fillquestions = FillQuestionDetail.objects.filter(exam = exam)
    tfquestions = TfQuestionDetail.objects.filter(exam = exam)
    saquestions = SAQuestionDetail.objects.filter(exam = exam)
    return render(request,'data/AnswerExam.html',{'exam':exam,
                                                'choicequestions':choicequestions,
                                                'fillquestions':fillquestions,
                                                'tfquestions':tfquestions,
                                                'saquestions':saquestions}) 
def verify_Answer(request,pk):
        exam = Exam.objects.get(id = pk)
        choicequestions = ChoiceQuestionDetail.objects.filter(exam = exam)
        fillquestions = FillQuestionDetail.objects.filter(exam = exam)
        tfquestions = TfQuestionDetail.objects.filter(exam = exam)
        saquestions = SAQuestionDetail.objects.filter(exam = exam)
        #检查是否有缺填题目
        SelectList = []
        SelectNull = []
        FillList = []
        FillNull = []
        TfList =[]
        TfNull =[]
        SAList = []
        SANull = []
        #统计选择题结果
        num = 1
        for question in choicequestions:
            pos = 'select' + str(question.id)
            #SelectList.append(request.POST[pos])
            if pos not in request.POST:
                SelectList.append('null')
                SelectNull.append(num)
            else:
                SelectList.append(request.POST[pos])
            num += 1
        request.session['SelectList']= SelectList
        #统计填空题结果
        num =  1
        for question in fillquestions:
            pos = 'fill' + str(question.id)
            if request.POST[pos] == u'':
                FillList.append('null')
                FillNull.append(num)
            else:
                FillList.append(request.POST[pos])
            num +=1
        request.session['FillList'] = FillList
        #统计判断题结果
        num = 1
        for question in tfquestions:
            pos = 'tf'+ str(question.id)
            if pos not in request.POST:
                TfList.append('null')
                TfNull.append(num)
            else:
                if request.POST[pos] == u'True':
                    TfList.append(True)
                elif request.POST[pos] ==u'False':
                    TfList.append(False)
            num +=1
        request.session['TfList'] = TfList 
        #统计简答题结果
        num = 1
        for question in saquestions:
            pos = 'sa'+ str(question.id)
            print request.POST[pos]
            if request.POST[pos] == u'':
                SAList.append('null')
                SANull.append(num)
            else:
                SAList.append(request.POST[pos])

            num +=1
        print SAList
        request.session['SAList'] = SAList 
        return render(request,'data/verify_Answer.html',{'SelectNull':SelectNull,
                                                        'FillNull':FillNull,
                                                        'TfNull':TfNull,
                                                        'SANull':SANull,
                                                        'exam':exam})

def ExamResult(request,pk):
        #提交考试做答结果
        exam = Exam.objects.get(id = pk)
        choicequestions = ChoiceQuestion.objects.filter(exam = exam)
        fillquestions = FillQuestion.objects.filter(exam = exam)
        tfquestions= TfQuestion.objects.filter(exam = exam)
        saquestions= SAQuestion.objects.filter(exam = exam)
        if 'test_exam_id' in request.session and request.session['test_exam_id'] == exam.id:
            test = Test.objects.get(id = request.session['test_id'])
            testlog = TestLog.objects.get(test= test,student = request.user)
            if testlog.state:
                return render(request,'data/Success.html')
            else:
                answer = Answer.objects.create(exam = exam,user = request.user,test = test)
                testlog.state = True
                testlog.answer = answer
                testlog.save()
        else:
            answer = Answer.objects.create(exam = exam,user = request.user)
        #初始化得分
        score = 0
        #提交选择题答案
        temp = 0#选择题总分
        pos = 0
        anslist = request.session['SelectList']
        for choicequestion in choicequestions:
            if anslist[pos] == choicequestion.ans:
                ans = ChoiceQuestionAns(answer = answer,
                                        choicequestion = choicequestion,
                                        ans = anslist[pos],
                                        state = True)
                choicequestiondetail= ChoiceQuestionDetail.objects.get(choicequestion = choicequestion,
                                                                    exam = exam)
                score +=  choicequestiondetail.mark
                temp += choicequestiondetail.mark
            else:
                ans = ChoiceQuestionAns(answer = answer,
                                        choicequestion = choicequestion,
                                        ans = anslist[pos],
                                        state = False)
            ans.save()
            pos += 1
        answer.select_score = temp
        answer.save()
        #提交填空题答案
        pos = 0
        temp = 0#填空题总分
        anslist = request.session['FillList']
        for fillquestion in fillquestions:
            if anslist[pos] == fillquestion.ans:
                ans = FillQuestionAns(answer = answer,
                                    fillquestion = fillquestion,
                                    ans = anslist[pos],
                                    state = True)
                fillquestiondetail =  FillQuestionDetail.objects.get(choicequestion = fillquestion,
                                                                    exam = exam)
                score += fillquestiondetail.mark
                temp += fillquestiondetail.mark
            else:
                ans = FillQuestionAns(answer = answer,
                                    fillquestion = fillquestion,
                                    ans = anslist[pos],
                                    state = False)
            ans.save() 
            pos += 1
        answer.fill_score = temp
        answer.save()
        #提交判断题
        pos = 0
        temp = 0#填空题总分答案
        anslist = request.session['TfList']
        for tfquestion in tfquestions:
            if anslist[pos] == tfquestion.ans:
                ans = TfQuestionAns(answer = answer,
                                    Tfquestion = tfquestion,
                                    ans = anslist[pos],
                                    state = True,
                                    )
                tfquestiondetail =  TfQuestionDetail.objects.get(tfquestion = tfquestion,
                                                                exam = exam)
                score += tfquestiondetail.mark
                temp = tfquestiondetail.mark
            elif anslist[pos]=='null':
                ans = TfQuestionAns(answer = answer,
                                    Tfquestion = tfquestion,
                                    ans = None,
                                    state = False)
            else:
                ans = TfQuestionAns(answer = answer,
                                    Tfquestion = tfquestion,
                                    ans = anslist[pos],
                                    state = False)
            ans.save()  
            pos += 1
        #answer.tf_score = temp
        #提交简答题
        pos = 0
        temp = 0#简答题总分答案
        anslist = request.session['SAList']
        for saquestion in saquestions:
            if anslist[pos]=='null':
                ans = SAQuestionAns(answer = answer,
                                    saquestion = saquestion,
                                    ans = None,
                                    state = False)
            else:
                #只要简答题答案不为空，就做待判处理
                saquestiondetail =  SAQuestionDetail.objects.get(saquestion = saquestion,
                                                                exam = exam)
                ans = SAQuestionAns(answer = answer,
                                    saquestion = saquestion,
                                    ans = anslist[pos],
                                    state = None,
                                    mark = saquestiondetail.mark)
                answer.state = False
                #登记待判试卷
                if 'test_exam_id' in request.session and request.session['test_exam_id'] == exam.id:
                    test.state = True
                    test.save()
                answer.save()
            ans.save()  
            pos += 1
        #answer.sa_score = temp
        answer.score = score
        answer.save()
        return HttpResponseRedirect(reverse('data:ResultDetail',args = (answer.id,)))
        
def ResultList(request):
    if request.method == 'POST':
        form = SearchAnswerForm(request.POST)
        if form.is_valid():
            request.session['answer_name'] = form.cleaned_data['name']
            request.session['answer_author'] = form.cleaned_data['author']
        return HttpResponseRedirect(reverse('data:ResultList'))
    else:
        #角色读入
        character = request.user.groups.all()[0].name
        if character == 'student':
            answers = Answer.objects.filter(user = request.user)
        elif character == 'teacher':
            answers = Answer.objects.all()

        #
        name = request.session['answer_name']
        author = request.session['answer_author']
        if author:
            authors = User.objects.filter(username__contains = author)
            answers = Answer.objects.filter(user__set = authors)
        if name:
            answers = answers.filter(exam__name__contains = name)
        answers = answers.order_by("-date")
        #分页
        paginator = Paginator(answers, 7) # Show 10 contacts per page
        page = request.GET.get('page')
        try:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
            answers = paginator.page(page)
        except PageNotAnInteger:
            answers = paginator.page(1)
        except EmptyPage:
            answers = paginator.page(paginator.num_pages)
        
        #form
        form = SearchAnswerForm(initial = {'name':name,
                                            'author':author})
        return render(request,'data/ResultList.html',{'answers':answers,
                                                    'form':form})
def ResultDetail(request,pk):
    answer = Answer.objects.get(id = pk)
    choicequestionans = ChoiceQuestionAns.objects.filter(answer = answer)
    fillquestionans = FillQuestionAns.objects.filter(answer = answer)
    tfquestionans=TfQuestionAns.objects.filter(answer=answer)
    saquestionans=SAQuestionAns.objects.filter(answer=answer)
    return render(request,'data/ResultDetail.html',{'answer':answer,
                                                    'choicequestionans':choicequestionans,
                                                    'fillquestionans':fillquestionans,
                                                    'tfquestionans':tfquestionans,
                                                    'saquestionans':saquestionans
                                                    })

def JudgeAnswer(request,pk):
    answer = Answer.objects.get(id = pk)
    saquestionans = SAQuestionAns.objects.filter(answer = answer)
    saquestions = SAQuestionDetail.objects.filter(exam = answer.exam)
    if request.method == 'POST':
        flag = True
        for item in saquestionans:
            pos = 'sa' + str(item.id)
            if request.POST[pos] and request.POST[pos] != u'':
                score = request.POST[pos]
                item.score = int(score)
                answer.score += item.score
                if item.score == item.mark:
                    item.state = True
                else:
                    item.state=  False
                item.save()
            else:
                flag = False
        answer.state = flag
        answer.save()
        return HttpResponseRedirect(reverse('data:ResultDetail',args = (pk,)))
    else:
        
        return render(request,'data/JudgeAnswer.html',{'answer':answer,
                                                    'saquestionans':saquestionans,
                                                    'saquestions':saquestions,})

#test
def NewTest(request):
    if request.method =="POST":
        form = NewTestForm(request.POST)
        if form.is_valid():
            test = Test.objects.create(name = form.cleaned_data['name'],
                                    Type = form.cleaned_data['Type'],
                                    user = request.user
                                    )
            return  HttpResponseRedirect(reverse('data:ChooseExam',args=(test.id,)))
    else:
        form = NewTestForm()
        return render(request,'data/NewTest.html',{'form':form})
def ChooseExam(request,pk):
    test = Test.objects.get(id = pk)
    if request.method == 'POST':
        form = SearchExamForm(request.POST)
        if form.is_valid():
            request.session['exam_name'] = form.cleaned_data['name']
            request.session['exam_diffculty'] = form.cleaned_data['diffculty']
            if form.cleaned_data['subject']:
                request.session['exam_point'] = form.cleaned_data['subject'].name
        else: 
            exam = Exam.objects.get(id = request.POST['exam']) 
            test.exam = exam
            test.save()
            teacher = Teacher.objects.get(user = request.user)
            students = teacher.students.all()
            #将学生添加到时间 完成情况为false
            for student in students:
                testlog = TestLog(test = test,student = student)
                testlog.save()
            return render(request,'data/Success.html')
        return HttpResponseRedirect(reverse('data:ChooseExam',args = (test.id,)))
    else:
        #筛选
        point = request.session['exam_point']
        diffculty = request.session['exam_diffculty']
        name = request.session['exam_name']
        if point:
            point = Point.objects.get(name = point)
            exams = Exam.objects.filter(subject = point)
        else:
            exams = Exam.objects.all()
        if diffculty != 'all':
            exams = exams.filter(diffculty = diffculty)
        if name:
            exams = exams.filter(name__contains = name)
        exams = exams.filter(state = False)
        exams = exams.order_by("-date")
        #分页
        paginator = Paginator(exams, 7) # Show 10 contacts per page
        page = request.GET.get('page')
        try:
            exams = paginator.page(page)
        except PageNotAnInteger:
            exams = paginator.page(1)
        except EmptyPage:
            exams = paginator.page(paginator.num_pages)
        #form
        form = SearchExamForm(initial = {'name':name,
                                        'subject':point,
                                        'diffculty':diffculty})
        return render(request,'data/ChooseExam.html',{'exams':exams,
                                                    'form':form})

def TestList(request):
    if request.method =='POST':
        form = TestSearchForm(request.POST)
        if form.is_valid():
            #搜索数据放入会话
            request.session['test_name'] = form.cleaned_data['name']
            request.session['test_type'] = form.cleaned_data['Type']
            request.session['user'] = form.cleaned_data['user']
        return HttpResponseRedirect(reverse('data:TestList'))
    else:
        #读入筛选数据
        name = request.session['test_name']
        Type = request.session['test_type']
        user = request.session['user']
        #作者
        if user:
            tests = Test.objects.filter(user__username__contains = user)
        else:
            tests = Test.objects.all()
        if name:
            tests = tests.filter(name__contains = name)
        if Type:
            tests = tests.filter(Type = Type)
        tests = tests.order_by("-date")
        form = TestSearchForm(initial = {'name':name,
                                        'user':user,
                                        'Type':Type})
        return render(request,'data/TestList.html',{'form':form,
                                                    'tests':tests})
def TestDetail(request,pk):
    test = Test.objects.get(id = pk)
    testlogs = TestLog.objects.filter(test = test)
    finish_student = testlogs.filter(state = True)
    unfinish_student = testlogs.filter(state =False)
    return render(request,'data/TestDetail.html',{'test':test,
                                                'testlogs':testlogs,
                                                'finish_student':finish_student,
                                                'unfinish_student':unfinish_student})

def TestLogList(request):
    testlogs = TestLog.objects.filter(student = request.user)
    unfinish = testlogs.filter(state = False)
    finish = testlogs.filter(state = True)
    return render(request,'data/TestLogList.html',{'finish':finish,
                                                'unfinish':unfinish})

def AnswerTest(request,pk):
    test = Test.objects.get(id = pk)
    exam = test.exam
    request.session['test_exam_id'] = exam.id
    request.session['test_id'] = test.id
    choicequestions = ChoiceQuestionDetail.objects.filter(exam = exam)
    fillquestions = FillQuestionDetail.objects.filter(exam = exam)
    tfquestions = TfQuestionDetail.objects.filter(exam = exam)
    saquestions = SAQuestionDetail.objects.filter(exam = exam)
    return render(request,'data/AnswerExam.html',{'exam':exam,
                                                'choicequestions':choicequestions,
                                                'fillquestions':fillquestions,
                                                'tfquestions':tfquestions,
                                                'saquestions':saquestions}) 
def TestReport(request,pk):
    #初始化数据
    test = Test.objects.get(id = pk)
    testlogs = TestLog.objects.filter(test = test)
    exam = test.exam
    #读入题目列表
    choicequestions =  exam.choicequestions.all()
    fillquestions = exam.fillquestions.all()
    tfquestions = exam.tfquestions.all()
    saquestions= exam.saquestions.all()
    choice_report=[]
    fill_report = []
    tf_report = []
    sa_report = []
    for i in range(0,len(choicequestions)):
        choice_report.append(0.0) 
    for i in range(0,len(fillquestions)):
        fill_report.append(0.0) 
    for i in range(0,len(tfquestions)):
        tf_report.append(0.0) 
    for i in range(0,len(saquestions)):
        sa_report.append(0.0) 
    #初始化总分
    score = 0.0
    for item in testlogs:
        #读入答案信息
        answer = item.answer
        #如果已经作答
        if answer:
            score+=item.answer.score#计算总分平均分
            #计算每题的平均分,正确率
            #选择
            pos = 0
            for question in choicequestions:
                choicequestionans =  ChoiceQuestionAns.objects.get(answer = answer,
                                                                choicequestion = question)
                if choicequestionans.state == True:
                    choice_report[pos] += 1
                pos += 1
            #填空
            pos = 0
            for question in fillquestions:
                fillquestionans =  FillQuestionAns.objects.get(answer = answer,
                                                                fillquestion = question)
                if fillquestionans.state == True:
                    fill_report[pos] += 1
                pos += 1
            #判断
            pos = 0
            for question in tfquestions:
                tfquestionans =  TfQuestionAns.objects.get(answer = answer,
                                                        Tfquestion = question)
                if tfquestionans.state == True:
                    tf_report[pos] += 1
                pos += 1
            #简答
            pos = 0
            for question in saquestions:
                saquestionans =  SAQuestionAns.objects.get(answer = answer,
                                                        saquestion = question)
                if saquestionans.state == True:
                    sa_report[pos] += 1
                pos += 1
            print sa_report
    
    for i in range(0,len(choicequestions)):
        choice_report[i] /= len(testlogs)
        choice_report[i] *=100
    for i in range(0,len(fillquestions)):
        fill_report[i] /= len(testlogs)
        fill_report[i] *=100
    for i in range(0,len(tfquestions)):
        tf_report[i] /= len(testlogs)
        tf_report[i] *=100
    for i in range(0,len(saquestions)):
        sa_report[i] /= len(testlogs)
        sa_report[i] *=100
    average = score/len(testlogs)
    return render(request,'data/TestReport.html',{'average':average,
                                                'testlogs':testlogs,
                                                'choice_report':choice_report,
                                                'fill_report':fill_report,
                                                'tf_report':tf_report,
                                                'sa_report':sa_report})
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
        #初始化数据
        #题库搜索
        request.session['question_keyword'] = None
        request.session['question_style'] = 'select'
        request.session['question_point'] = None
        #试卷搜索
        request.session['exam_name'] = None
        request.session['exam_diffculty'] = 'all'
        request.session['exam_point'] = None
        request.session['exam_state'] = None
        #考试答题记录搜索
        request.session['answer_name'] = None
        request.session['answer_author'] = None
        #事件筛选
        request.session['test_name'] = None
        request.session['test_type'] = None
        request.session['user'] = None
        #教师筛选
        request.session['teacher_name'] = None
        request.session['teacher_subject'] = None
        character = request.user.groups.all()[0].name
        if character == 'student':
            student = Student.objects.create(name = form.cleaned_data['username'],
                                            user = request.user,)
        elif character == 'teacher':
            teacher = Teacher.objects.create(name = form.cleaned_data['username'],
                                            user = request.user,)
        return HttpResponseRedirect(reverse('data:RegesteSuccess'))
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
                    #初始化数据
                    #题库搜索
                    request.session['question_keyword'] = None
                    request.session['question_style'] = 'select'
                    request.session['question_point'] = None
                    #试卷搜索
                    request.session['exam_name'] = None
                    request.session['exam_diffculty'] = 'all'
                    request.session['exam_point'] = None
                    request.session['exam_state'] = None
                    #考试答题记录搜索
                    request.session['answer_name'] = None
                    request.session['answer_author'] = None
                    #事件筛选
                    request.session['test_name'] = None
                    request.session['test_type'] = None
                    request.session['user'] = None
                    #教师筛选
                    request.session['teacher_name'] = None
                    request.session['teacher_subject'] = None
                    return HttpResponseRedirect(reverse('data:HomePage'))
                else:

                    message = 0
            else:
                message = 1
            return render(request,'data/LoginFiel.html',{'message':message})
    else:
        form = NewUserLoginForm()
    return  render(request,'data/Login.html',{'form':form})

def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('data:HomePage'))

def UserDetail(request,pk):
    if not request.user.is_authenticated():
        form = NewUserLoginForm()
        return HttpResponseRedirect(reverse('data:Login'))
    user = User.objects.get(id = pk)
    if user.groups.all()[0].name == 'student':
        print 'right'
        detail = Student.objects.get(user = user)
    elif user.groups.all()[0].name == 'teacher':
        print 'wrong'
        detail = Teacher.objects.get(user = user)
    context= {'detail':detail,'user':user}
    return render(request,'data/UserDetail.html',context)

def ChooseTeacher(request):
    if request.method == "POST":
        form = ChooseTeacherForm(request.POST)
        if form.is_valid() and 'submit' in request.POST: 
            request.session['teacher_name'] = form.cleaned_data['name']
            request.session['subject'] = form.cleaned_data['subject']
        elif 'teacher' in request.POST:
            teacher = Teacher.objects.get(id = request.POST['teacher'])
            teacher.students.add(request.user)
            teacher.save()
            return render(request,'data/Success.html')
        return HttpResponseRedirect(reverse('data:ChooseTeacher'))
    else:
        teachers = Teacher.objects.all()
        #读入数据
        name = request.session['teacher_name']
        subject = request.session['teacher_subject']
        #筛选
        if name:
            teachers = teachers.filter(name__contains =  name)
        if subject:
            teachers = teachers.filter(subject__contains =  subject)
        form = ChooseTeacherForm(initial = {'name':name,
                                            'subject':subject})
        return render(request,'data/ChooseTeacher.html',{'form':form,
                                                        'teachers':teachers})

def StudentList(request):
    teacher =  Teacher.objects.get(user = request.user)
    students = teacher.students.all()
    students = Student.objects.filter(user = students)
    return render(request,'data/StudentList.html',{'students':students})
#common views

def welcome(request):
    return render(request,'data/welcome.html')

def HomePage(request):
    if request.user.is_authenticated():
        character = request.user.groups.all()[0].name
        if character == 'student':
            #显示代做事件
            testlogs = TestLog.objects.filter(student = request.user,state = False)
        else:
            testlogs = None
        return render(request,'data/HomePage.html',{'character':character,
                                                    'testlogs':testlogs})
    else:
        return HttpResponseRedirect(reverse('data:Login'))