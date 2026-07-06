from django.contrib import admin
from .models import Profile, TeacherMaterial, StudentPost, DailyTest


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'student_class', 'points', 'is_approved')
    list_editable = ('is_approved', 'points')
    list_filter = ('is_approved', 'student_class')
    search_fields = ('user__username', 'full_name')
    ordering = ('-points',)


@admin.register(TeacherMaterial)
class TeacherMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)
    ordering = ('-uploaded_at',)


@admin.register(StudentPost)
class StudentPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'author__username')
    ordering = ('-created_at',)


@admin.register(DailyTest)
class DailyTestAdmin(admin.ModelAdmin):
    list_display = ('question', 'correct_answer', 'author', 'created_at')
    list_filter = ('correct_answer', 'created_at')
    search_fields = ('question',)
    ordering = ('-created_at',)
