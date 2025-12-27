from rest_framework import serializers
from .models import Question, Quiz


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'text']


class QuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description']