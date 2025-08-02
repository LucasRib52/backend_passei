from django.db import models
from courses.models import Course


class Sale(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('paid', 'Pago'),
        ('cancelled', 'Cancelado'),
        ('refunded', 'Reembolsado'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('pix', 'PIX'),
        ('credit_card', 'Cartão de Crédito'),
        ('bank_slip', 'Boleto'),
        ('transfer', 'Transferência'),
    ]
    
    student_name = models.CharField(max_length=200, verbose_name='Nome do Aluno')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Telefone')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Curso')
    
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='Método de Pagamento')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Status')
    
    # Integração externa
    asaas_payment_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='ID Pagamento ASAAS')
    themembers_access_granted = models.BooleanField(default=False, verbose_name='Acesso TheMembers Concedido')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student_name} - {self.course.title}"
