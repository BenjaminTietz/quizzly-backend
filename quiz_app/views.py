from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from .models import Quiz
from .serializers import QuestionSerializer, QuizSerializer
from rest_framework.response import Response
from rest_framework import status
from quiz_app.services.create_quiz import create_quiz_from_url


class QuizCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        url = request.data.get('url')
        if not url:
            return Response({"detail": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)

        quiz = create_quiz_from_url(user=request.user, url=url)
        serializer = QuizSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QuizListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        quizzes = Quiz.objects.all()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class QuizDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"detail": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuizSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class QuizQuestionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"detail": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

        questions = quiz.questions.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
