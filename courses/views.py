from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Course, Module, Lesson, Category
from .serializers import (
    CourseSerializer, CourseListSerializer, CourseDetailSerializer,
    CourseCreateUpdateSerializer, CoursePublicListSerializer, ModuleSerializer,
    ModulePublicSerializer, CoursePublicDetailSerializer, LessonSerializer,
    ModuleCreateUpdateSerializer, CategorySerializer, CategoryPublicSerializer
)


# Views Públicas (API)
class CourseListView(generics.ListAPIView):
    """
    Lista todos os cursos ativos
    """
    queryset = Course.objects.filter(status='active')
    serializer_class = CoursePublicListSerializer
    permission_classes = [AllowAny]  # Acesso público
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['professor', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'rating', 'students_count', 'created_at']
    ordering = ['-created_at']


class CourseDetailView(generics.RetrieveAPIView):
    """
    Detalhes de um curso específico
    """
    queryset = Course.objects.filter(status='active')
    serializer_class = CoursePublicDetailSerializer
    permission_classes = [AllowAny]  # Acesso público
    lookup_field = 'id'


# Views de Administração (API para /admin do frontend)
class AdminCourseViewSet(generics.ListCreateAPIView):
    """
    CRUD completo de cursos para o painel admin
    """
    queryset = Course.objects.all()
    serializer_class = CourseCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'professor']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price', 'rating']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CourseSerializer
        return CourseCreateUpdateSerializer


class AdminCourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalhes, atualização e exclusão de curso para o painel admin
    """
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CourseSerializer
        return CourseCreateUpdateSerializer


# Views para Módulos
class ModuleListView(generics.ListAPIView):
    """
    Lista módulos de um curso específico
    """
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return Module.objects.filter(course_id=course_id)


class ModuleDetailView(generics.RetrieveAPIView):
    """
    Detalhes de um módulo específico
    """
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    lookup_field = 'id'


# Views para Aulas
class LessonListView(generics.ListAPIView):
    """
    Lista aulas de um módulo específico
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        module_id = self.kwargs.get('module_id')
        return Lesson.objects.filter(module_id=module_id)


class LessonDetailView(generics.RetrieveAPIView):
    """
    Detalhes de uma aula específica
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_field = 'id'


# Views de Administração para Módulos (API para /admin do frontend)
class AdminModuleListCreateView(generics.ListCreateAPIView):
    """Listar e criar módulos para um curso no painel admin"""
    serializer_class = ModuleCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return Module.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs.get('course_id')
        serializer.save(course_id=course_id)

class AdminModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes de um módulo (GET, PUT, DELETE) no painel admin"""
    queryset = Module.objects.all()
    serializer_class = ModuleCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


# Views para Categorias
class CategoryListView(generics.ListAPIView):
    """
    Lista todas as categorias ativas
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategoryPublicSerializer
    permission_classes = [AllowAny]  # Acesso público
    ordering = ['name']
 
 
class AdminCategoryViewSet(generics.ListCreateAPIView):
    """
    CRUD completo de categorias para o painel admin
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    ordering = ['name']
 
 
class AdminCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalhes, atualização e exclusão de categoria para o painel admin
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
