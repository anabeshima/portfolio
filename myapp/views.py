from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import Question, Choicce

def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_questions': latest_questions}
    return render(request, 'myapp/index.html',context)

def detail(request, question_id):
    question = Question.objects.get(pk=question_id)
    return render(request, 'myapp/detail.html',{'question':question})

def results(request, question_id):
    question = Question.objects.get(pk=question_id)
    return render(request, 'myapp/results.html',{'question':question})

def vote(request, question_id):
    question = Question.objects.get(pk=question_id)
    try:
        selected_choice = question.choise_set(pk=request.POST['choice'])
    except (KeyError, Choicce.DoesNotExist):
        return render(request,'myapp/detail.html',{
            'question':question,
            'error_message':"回答を選択していません"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('myapp:results',args=(question.id)))