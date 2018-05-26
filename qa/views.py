from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from qa.models import *
from django.core import serializers
import json
import markdown2
import bleach

def index(request):
    context = {}
    context['questions'] = Question.objects.all()
    return render(request, 'index.html', context)

def askquestion(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            question = request.POST.get('question')
            posted_by = request.POST.get('posted_by')
            q = Question(question_title=title, question_text=question, posted_by=posted_by)
            q.save()
            return redirect(viewquestion, q.qid, q.slug)
        except Exception as e:
            return render(request, 'ask-question.html', { 'error': 'Something is wrong with the form!' })
    else:
        return render(request, 'ask-question.html', {})

def viewquestion(request, qid, qslug):
    context = {}
    question = Question.objects.get(qid=qid, slug=qslug)

    # assuming obj is a model instance
    question_json = json.loads(serializers.serialize('json', [ question ]))[0]['fields']
    question_json['date_posted'] = question.date_posted
    question_json['qid'] = question.qid
    question_json['question_text'] = bleach.clean(markdown2.markdown(question_json['question_text']), tags=['p', 'pre','code', 'sup', 'strong', 'hr', 'sub', 'a'])
    context['question'] = question_json
    context['answers'] = []
    answers = Answer.objects.filter(qid=qid)
    for answer in answers:
        answer.answer_text = bleach.clean(markdown2.markdown(answer.answer_text), tags=['p', 'pre','code', 'sup', 'strong', 'hr', 'sub', 'a'])
        context['answers'].append(answer)
    return render(request, 'view-question.html', context)

@csrf_exempt
def ajaxanswerquestion(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            answer = json_data['answer']
            posted_by = json_data['posted_by']
            qid = json_data['qid']
            a = Answer(answer_text=answer, posted_by=posted_by, qid=Question.objects.get(qid=qid))
            a.save()
            return JsonResponse({'Success': 'Answer posted successfully.'})
        except Exception as e:
            print(e)
            return JsonResponse({'Error': 'Something went wrong when posting your answer.'})
            #return render(request, 'ask-question.html', { 'error': 'Something is wrong with the form!' })
