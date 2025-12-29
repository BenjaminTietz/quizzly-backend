from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from quiz_app.models import Quiz, Question, QuestionOption


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 1
    fields = ("option_text", "is_correct")
    ordering = ("id",)


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    fields = ("question_title",)
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "created_at", "updated_at")
    list_filter = ("owner", "created_at")
    search_fields = ("title", "description", "owner__username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    inlines = [QuestionInline]

    fieldsets = (
        ("Quiz Info", {
            "fields": ("title", "description", "video_url")
        }),
        ("Owner", {
            "fields": ("owner",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz_owner", "question_title", "quiz", "created_at")
    list_filter = ("quiz__owner", "quiz")
    search_fields = ("question_title", "quiz__title", "quiz__owner__username")
    ordering = ("quiz__owner__username", "quiz__title", "id")

    inlines = [QuestionOptionInline]

    def quiz_owner(self, obj):
        return obj.quiz.owner.username
    quiz_owner.short_description = "Owner"


# -----------------------------
# Admin: User
# -----------------------------

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_staff", "is_active", "is_superuser")
    list_filter = ("is_staff", "is_active", "is_superuser", "groups")
    search_fields = ("username", "email")
    ordering = ("username",)

    readonly_fields = ("last_login", "date_joined")

    fieldsets = (
        ("User Info", {
            "fields": ("username", "email", "password")
        }),
        ("Permissions", {
            "fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")
        }),
        ("Important Dates", {
            "fields": ("last_login", "date_joined")
        }),
    )

    add_fieldsets = (
        ("Create User", {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "is_staff", "is_active"),
        }),
    )