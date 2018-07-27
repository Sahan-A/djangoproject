from api import views
from django.urls import path

urlpatterns=[
    path('',views.QuestionList.as_view()),
    path('<int:pk>',views.QuestionDetail.as_view()),
]