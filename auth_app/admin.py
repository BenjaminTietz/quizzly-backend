from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = (
        ("User Info", {'fields': ('username', 'email', 'password')}),
        ("Permissions", {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ("Important dates", {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            "Create User",
            {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active'),
            },
        )
    )
