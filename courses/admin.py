from django.contrib import admin
from .models import Course, Module, Lesson, Category

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'professor', 'category', 'price', 'status', 'created_at']
    list_filter = ['status', 'category', 'professor', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'lessons_count', 'duration', 'order']
    list_filter = ['course', 'order']
    search_fields = ['title', 'description']
    ordering = ['course', 'order']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'duration', 'is_free', 'order']
    list_filter = ['module', 'is_free', 'order']
    search_fields = ['title', 'description']
    ordering = ['module', 'order']
