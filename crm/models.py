from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime, timedelta


class User(AbstractUser):
    """
    Representantes de ventas (extiende el modelo User de Django)
    """
    is_sales_rep = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Sales Representative'
        verbose_name_plural = 'Sales Representatives'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.username


class Company(models.Model):
    """
    Compañías a las que pertenecen los clientes
    """
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Customer(models.Model):
    """
    Personas asociadas a una compañía y a un representante de ventas
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='customers'
    )
    sales_rep = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='customers'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['birth_date']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def birthday_formatted(self):
        """Retorna el cumpleaños en formato 'February 5'"""
        return self.birth_date.strftime("%B %-d")
    
    def get_last_interaction(self):
        """Obtiene la última interacción del cliente"""
        return self.interactions.order_by('-interaction_date').first()
    
    def get_last_interaction_display(self):
        """Retorna la última interacción formateada (ej: '1 day ago (Phone)')"""
        last_interaction = self.get_last_interaction()
        if not last_interaction:
            return "No interactions"
        
        # Calcular tiempo transcurrido
        now = timezone.now()
        delta = now - last_interaction.interaction_date
        
        if delta.days == 0:
            if delta.seconds < 3600:
                minutes = delta.seconds // 60
                time_str = f"{minutes} minute{'s' if minutes != 1 else ''} ago"
            else:
                hours = delta.seconds // 3600
                time_str = f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif delta.days == 1:
            time_str = "1 day ago"
        elif delta.days < 7:
            time_str = f"{delta.days} days ago"
        elif delta.days < 30:
            weeks = delta.days // 7
            time_str = f"{weeks} week{'s' if weeks != 1 else ''} ago"
        elif delta.days < 365:
            months = delta.days // 30
            time_str = f"{months} month{'s' if months != 1 else ''} ago"
        else:
            years = delta.days // 365
            time_str = f"{years} year{'s' if years != 1 else ''} ago"
        
        return f"{time_str} ({last_interaction.interaction_type})"
    
    def birthday_this_week(self):
        """Verifica si el cumpleaños es esta semana"""
        today = datetime.now().date()
        # Obtener el inicio y fin de la semana
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        # Crear fecha de cumpleaños para este año
        try:
            birthday_this_year = self.birth_date.replace(year=today.year)
        except ValueError:
            # Caso especial para 29 de febrero en años no bisiestos
            birthday_this_year = self.birth_date.replace(year=today.year, day=28)
        
        return start_of_week <= birthday_this_year <= end_of_week


class Interaction(models.Model):
    """
    Registros de llamadas, correos, etc., que tuvo un representante con un cliente
    """
    INTERACTION_TYPES = [
        ('Call', 'Phone Call'),
        ('Email', 'Email'),
        ('SMS', 'SMS'),
        ('WhatsApp', 'WhatsApp'),
        ('Facebook', 'Facebook'),
        ('LinkedIn', 'LinkedIn'),
        ('Meeting', 'In-Person Meeting'),
        ('Video Call', 'Video Call'),
    ]
    
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE, 
        related_name='interactions'
    )
    interaction_type = models.CharField(max_length=50, choices=INTERACTION_TYPES)
    interaction_date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Interaction'
        verbose_name_plural = 'Interactions'
        ordering = ['-interaction_date']
        indexes = [
            models.Index(fields=['-interaction_date']),
            models.Index(fields=['customer', '-interaction_date']),
        ]
    
    def __str__(self):
        return f"{self.interaction_type} - {self.customer.full_name} - {self.interaction_date.strftime('%Y-%m-%d %H:%M')}"

