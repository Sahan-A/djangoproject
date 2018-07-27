from api.serializer import QuestionSerializer
from django.shortcuts import render

# Create your views here.
from quiz.models import Question
from rest_framework import generics


class QuestionList(generics.ListAPIView):
    queryset=Question.objects.all()
    serializer_class=QuestionSerializer


class QuestionDetail(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

