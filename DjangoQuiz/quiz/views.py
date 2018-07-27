from django.contrib.auth.decorators import login_required


# Create your views here.

from pprint import pprint

from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, DeleteView

from quiz.models import Question, Score



class HomeTemplateView(TemplateView):
    template_name = 'home.html'


    # def categories(self):
    #     dst_cat=Question.objects.values_list('category').distinct()
    #     return dst_cat
    def get_context_data(self, **kwargs):
        context=super(HomeTemplateView,self).get_context_data(**kwargs)
        context['categories']=Question.objects.values_list('category').distinct()
        return context

def index(request):
    dst_cat=Question.objects.values_list('category').distinct()
    pprint(dst_cat)
    context={'dcat':dst_cat}

    return render(request,'quiz/index.html',context)

@login_required(login_url='/accounts/login/')
def playquiz(request):

    param = request.GET.get('category')
    pprint(param)
    categories = Question.objects.values_list('category').distinct()
    single_Question= Question.objects.filter(category=param)[:1]
    context = {'sq':single_Question,'categories':categories}
    return render(request,'quiz/play-quiz.html',context)


def playquiznext(request):

    user_selected_choice=request.POST.get('is_company')
    user_taken_time=request.POST.get('userTakenTime')
    from pprint import pprint
    print("----------Time Taken-------")
    print(user_taken_time)
    correct_ans= request.POST.get('correct_answer')
    qid=request.POST.get('question')
    pprint(user_selected_choice)
    pprint(correct_ans)
    pprint(qid)
    if user_selected_choice==correct_ans:
        s=Score(question_id=qid,score=5,user_id=request.user.id)
        s.save()
    else:
        s=Score(question_id=qid,score=0,user_id=request.user.id)
        s.save()
    question_already_played = Score.objects.values_list('question')
    pprint(question_already_played)
    question_not_yet_played= Question.objects.filter(category='Physics').exclude(id__in=question_already_played)[:1]
    pprint(question_not_yet_played)
    if question_not_yet_played:

        context = {'sq': question_not_yet_played}
        return render(request, 'quiz/play-quiz.html',context)
    else:
        scores=Score.objects.all()
        total= sum([sc.score for sc in scores])
        context = {'score':scores,'total':total}
        current_user = request.user.id
        Score.objects.filter(user_id=current_user).delete()
        return render(request,'quiz/result.html',context)

class QuestionList(generic.ListView):
    model=Question
    template_name = 'quiz/qlist.html'
    context_object_name = 'get_questions'

    def get_queryset(self):
        query_set=Question.objects.all()[:2]
        return query_set

class QuestionDetail(generic.DetailView):
    model = Question
    def get_context_data(self, **kwargs):
        context=super(QuestionDetail,self).get_context_data(**kwargs)
        context['test']='data'
        return context
class QuestionDelete(DeleteView):
        model = Question

        success_url=reverse_lazy('index')

class QuestionCreate(CreateView):
    model = Question
    fields = ['question_text','category']
    success_url = reverse_lazy('index')

class QuestionUpdate(UpdateView):
    model = Question
    fields = ['question_text','category']
    success_url = reverse_lazy('index')
