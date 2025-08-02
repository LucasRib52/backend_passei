from rest_framework import serializers
from .models import Professor


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'


class ProfessorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = [
            'id', 'name', 'specialties', 'approvals_count', 
            'rating', 'image', 'created_at'
        ]


class ProfessorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__' 