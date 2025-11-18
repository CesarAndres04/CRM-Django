from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Company, Customer, Interaction


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_sales_rep', 'is_staff']
    list_filter = ['is_sales_rep', 'is_staff', 'is_superuser']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Sales Info', {'fields': ('is_sales_rep',)}),
    )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'company', 'sales_rep', 'birth_date', 'created_at']
    list_filter = ['company', 'sales_rep']
    search_fields = ['first_name', 'last_name']
    date_hierarchy = 'created_at'


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ['customer', 'interaction_type', 'interaction_date', 'created_at']
    list_filter = ['interaction_type', 'interaction_date']
    search_fields = ['customer__first_name', 'customer__last_name', 'notes']
    date_hierarchy = 'interaction_date'

