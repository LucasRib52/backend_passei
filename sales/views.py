from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Sale
from .serializers import SaleSerializer, SaleListSerializer


# Create your views here.

# Views de Administração (API para /admin do frontend)
class AdminSaleViewSet(generics.ListCreateAPIView):
    """
    CRUD completo de vendas para o painel admin
    """
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'course']
    search_fields = ['student_name', 'email']
    ordering_fields = ['created_at', 'price', 'status']
    ordering = ['-created_at']


class AdminSaleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalhes, atualização e exclusão de venda para o painel admin
    """
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class AdminSaleListView(generics.ListAPIView):
    """
    Lista de vendas para o painel admin (versão simplificada)
    """
    queryset = Sale.objects.all()
    serializer_class = SaleListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'course']
    search_fields = ['student_name', 'email']
    ordering_fields = ['created_at', 'price', 'status']
    ordering = ['-created_at']
