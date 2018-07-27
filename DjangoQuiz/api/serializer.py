from quiz import models
from rest_framework import serializers


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        fields=('id','question_text','category')
        model=models.Question