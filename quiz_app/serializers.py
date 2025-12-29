from rest_framework import serializers
from .models import Quiz, Question, QuestionOption


class QuestionSerializer(serializers.ModelSerializer):
    question_options = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            "id",
            "question_title",
            "question_options",
            "answer",
            "created_at",
            "updated_at",
        ]

    def get_question_options(self, obj):
        """
        Returns a list of option texts for the given question object.

        :param obj: A Question object
        :return: A list of strings representing the option texts
        :rtype: List[str]
        """
        return [opt.option_text for opt in obj.options.all()]

    def get_answer(self, obj):
        """
        Returns the correct answer for the given question object.

        If the correct answer is found, it is returned as a string.
        Otherwise, None is returned.

        :param obj: A Question object
        :return: The correct answer as a string, or None if not found
        :rtype: str | None
        """
        correct_option = obj.options.filter(is_correct=True).first()
        return correct_option.option_text if correct_option else None
    

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "description",
            "video_url",
            "created_at",
            "updated_at",
            "questions",
        ]