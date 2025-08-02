from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    # URLs de Administração
    path('admin/', views.AdminSaleViewSet.as_view(), name='admin-sale-list'),
    path('admin/<int:id>/', views.AdminSaleDetailView.as_view(), name='admin-sale-detail'),
    path('admin/list/', views.AdminSaleListView.as_view(), name='admin-sale-list-simple'),
] 