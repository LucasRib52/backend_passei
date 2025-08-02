from rest_framework import serializers
from .models import Sale
from courses.serializers import CourseListSerializer


class SaleSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)
    
    class Meta:
        model = Sale
        fields = '__all__'


class SaleListSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = Sale
        fields = [
            'id', 'student_name', 'email', 'phone', 'course_title',
            'price', 'payment_method', 'status', 'created_at'
        ] 