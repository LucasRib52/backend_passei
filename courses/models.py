from django.db import models
from django.contrib.auth.models import User
from professors.models import Professor


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    description = models.TextField(blank=True, null=True, verbose_name='Descrição')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slug')
    color = models.CharField(max_length=7, default='#3B82F6', verbose_name='Cor')
    is_active = models.BooleanField(default=True, verbose_name='Ativa')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criada em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizada em')
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Course(models.Model):
    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('inactive', 'Inativo'),
        ('draft', 'Rascunho'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descrição')
    detailed_description = models.TextField(blank=True, null=True, verbose_name='Descrição Detalhada')
    content = models.TextField(blank=True, null=True, verbose_name='Conteúdo do Curso')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Preço Original')
    
    # Preview do curso
    video_url = models.URLField(blank=True, null=True, verbose_name='URL do Vídeo de Apresentação')
    image_preview = models.URLField(blank=True, null=True, verbose_name='URL da Imagem de Preview')
    
    duration = models.CharField(max_length=50, verbose_name='Duração')
    students_count = models.IntegerField(default=0, verbose_name='Número de Alunos')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name='Avaliação')
    reviews_count = models.IntegerField(default=0, verbose_name='Número de Avaliações')
    
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, verbose_name='Professor')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoria', null=True, blank=True)
    benefits = models.TextField(verbose_name='Benefícios')
    requirements = models.TextField(verbose_name='Requisitos')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    # Integração externa
    themembers_link = models.URLField(blank=True, null=True, verbose_name='Link TheMembers')
    asaas_product_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='ID Produto ASAAS')
    
    # Badges/Tags do curso
    is_bestseller = models.BooleanField(default=False, verbose_name='Mais Vendido')
    is_complete = models.BooleanField(default=False, verbose_name='Completo')
    is_new = models.BooleanField(default=False, verbose_name='Novo')
    is_featured = models.BooleanField(default=False, verbose_name='Destaque')
    
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules', verbose_name='Curso')
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descrição')
    lessons_count = models.IntegerField(default=0, verbose_name='Número de Aulas')
    duration = models.CharField(max_length=50, verbose_name='Duração')
    order = models.IntegerField(default=0, verbose_name='Ordem')
    topics = models.TextField(blank=True, verbose_name='Tópicos')
    
    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons', verbose_name='Módulo')
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descrição')
    video_url = models.URLField(verbose_name='URL do Vídeo')
    duration = models.CharField(max_length=50, verbose_name='Duração')
    order = models.IntegerField(default=0, verbose_name='Ordem')
    is_free = models.BooleanField(default=False, verbose_name='É Gratuita')
    
    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.module.title} - {self.title}"
