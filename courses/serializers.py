from rest_framework import serializers
from .models import Course, Module, Lesson, Category
from professors.serializers import ProfessorSerializer
from professors.models import Professor
from django.utils.text import slugify


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    
    def create(self, validated_data):
        # Gerar slug automaticamente se não fornecido
        if 'slug' not in validated_data or not validated_data['slug']:
            validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Gerar slug automaticamente se nome foi alterado
        if 'name' in validated_data and validated_data['name'] != instance.name:
            validated_data['slug'] = slugify(validated_data['name'])
        return super().update(instance, validated_data)


class CategoryPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'color', 'is_active']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Module
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    professor = ProfessorSerializer(read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)
    category = CategoryPublicSerializer(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    original_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    
    class Meta:
        model = Course
        fields = '__all__'


class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    # Novo campo de conteúdo programático do curso (opcional)
    content = serializers.CharField(required=False, allow_blank=True, allow_null=True, help_text='Conteúdo do curso')
    # Tratar image_preview como URL em vez de arquivo
    image_preview = serializers.URLField(required=False, allow_blank=True, allow_null=True, help_text='URL da imagem de preview')
    """
    Serializer para criação e atualização de cursos
    Permite definir o professor por ID
    """
    professor = serializers.PrimaryKeyRelatedField(
        queryset=Professor.objects.all(),
        required=True
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        allow_null=True
    )
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    original_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    
    class Meta:
        model = Course
        fields = '__all__'


class CourseListSerializer(serializers.ModelSerializer):
    professor_name = serializers.CharField(source='professor.name', read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    original_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'price', 'original_price',
            'duration', 'students_count', 'rating', 'reviews_count',
            'professor_name', 'status', 'created_at'
        ]


class CoursePublicListSerializer(serializers.ModelSerializer):
    """
    Serializer para listagem pública de cursos
    Inclui o professor completo para o frontend
    """
    professor = ProfessorSerializer(read_only=True)
    category = CategoryPublicSerializer(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    original_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'detailed_description', 'price', 'original_price',
            'duration', 'students_count', 'rating', 'reviews_count',
            'professor', 'category', 'benefits', 'requirements', 'status', 'created_at',
            'video_url', 'image_preview', 'is_bestseller', 'is_complete', 'is_new', 'is_featured'
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    professor = ProfessorSerializer(read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    original_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    
    class Meta:
        model = Course
        fields = '__all__' 


class ModulePublicSerializer(serializers.ModelSerializer):
    """Serializer público de Módulo com lista de tópicos"""
    lessons = LessonSerializer(many=True, read_only=True)
    topics_list = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ['id', 'title', 'lessons_count', 'duration', 'order', 'topics_list']

    def get_topics_list(self, obj):
        if obj.topics:
            return [t.strip() for t in obj.topics.split(',')]
        return []

class CoursePublicDetailSerializer(serializers.ModelSerializer):
    """Serializer público de detalhes de curso"""
    professor = ProfessorSerializer(read_only=True)
    modules = ModulePublicSerializer(many=True, read_only=True)
    category = CategoryPublicSerializer(read_only=True)
    benefits_list = serializers.SerializerMethodField()
    requirements_list = serializers.SerializerMethodField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    original_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'detailed_description', 'content',
            'price', 'original_price', 'duration', 'students_count',
            'rating', 'reviews_count', 'professor', 'category',
            'benefits_list', 'requirements_list',
            'modules', 'video_url', 'image_preview', 'status', 'created_at',
            'is_bestseller', 'is_complete', 'is_new', 'is_featured'
        ]

    def get_benefits_list(self, obj):
        if obj.benefits:
            return [b.strip() for b in obj.benefits.split(',')]
        return []

    def get_requirements_list(self, obj):
        if obj.requirements:
            return [r.strip() for r in obj.requirements.split(',')]
        return [] 


class ModuleCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para criação/atualização de módulos (admin)"""
    class Meta:
        model = Module
        fields = ['id','title','description','lessons_count','duration','order','topics','course'] 