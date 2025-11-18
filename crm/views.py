from django.shortcuts import render
from django.db.models import Q, Max, Prefetch
from datetime import datetime, timedelta
from .models import Customer, Interaction


def customer_list(request):
    """
    Vista principal del CRM que muestra la lista de clientes con filtros y ordenamiento
    """
    # Obtener todos los clientes con sus relaciones precargadas para optimizar
    customers = Customer.objects.select_related(
        'company', 'sales_rep'
    ).prefetch_related(
        Prefetch(
            'interactions',
            queryset=Interaction.objects.order_by('-interaction_date')[:1],
            to_attr='latest_interaction_list'
        )
    )
    
    # Filtro por nombre
    search_query = request.GET.get('search', '').strip()
    if search_query:
        customers = customers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(company__name__icontains=search_query)
        )
    
    # Filtro por cumpleaños
    birthday_filter = request.GET.get('birthday', '')
    if birthday_filter == 'this_week':
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        # Obtener mes y día del inicio y fin de la semana
        start_month = start_of_week.month
        start_day = start_of_week.day
        end_month = end_of_week.month
        end_day = end_of_week.day
        
        if start_month == end_month:
            # Misma semana del mes
            customers = customers.filter(
                birth_date__month=start_month,
                birth_date__day__gte=start_day,
                birth_date__day__lte=end_day
            )
        else:
            # La semana cruza dos meses
            customers = customers.filter(
                Q(birth_date__month=start_month, birth_date__day__gte=start_day) |
                Q(birth_date__month=end_month, birth_date__day__lte=end_day)
            )
    
    elif birthday_filter == 'this_month':
        current_month = datetime.now().month
        customers = customers.filter(birth_date__month=current_month)
    
    elif birthday_filter == 'today':
        today = datetime.now().date()
        customers = customers.filter(
            birth_date__month=today.month,
            birth_date__day=today.day
        )
    
    # Ordenamiento
    sort_by = request.GET.get('sort', 'name')
    
    if sort_by == 'name':
        customers = customers.order_by('last_name', 'first_name')
    elif sort_by == 'company':
        customers = customers.order_by('company__name', 'last_name', 'first_name')
    elif sort_by == 'birthday':
        # Ordenar por mes y día de cumpleaños
        customers = customers.order_by('birth_date__month', 'birth_date__day')
    elif sort_by == 'last_interaction':
        # Anotar con la fecha de última interacción y ordenar
        customers = customers.annotate(
            last_interaction_date=Max('interactions__interaction_date')
        ).order_by('-last_interaction_date')
    
    # Paginación básica (opcional, pero recomendado para 1000 clientes)
    from django.core.paginator import Paginator
    paginator = Paginator(customers, 50)  # 50 clientes por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'birthday_filter': birthday_filter,
        'sort_by': sort_by,
        'total_customers': customers.count(),
    }
    
    return render(request, 'crm/customer_list.html', context)


def dashboard(request):
    """
    Vista de dashboard con estadísticas generales
    """
    from .models import User, Company
    
    total_customers = Customer.objects.count()
    total_companies = Company.objects.count()
    total_sales_reps = User.objects.filter(is_sales_rep=True).count()
    total_interactions = Interaction.objects.count()
    
    # Cumpleaños de hoy
    today = datetime.now().date()
    birthdays_today = Customer.objects.filter(
        birth_date__month=today.month,
        birth_date__day=today.day
    ).select_related('company')
    
    # Cumpleaños esta semana
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    start_month = start_of_week.month
    start_day = start_of_week.day
    end_month = end_of_week.month
    end_day = end_of_week.day
    
    if start_month == end_month:
        birthdays_this_week = Customer.objects.filter(
            birth_date__month=start_month,
            birth_date__day__gte=start_day,
            birth_date__day__lte=end_day
        ).select_related('company').count()
    else:
        birthdays_this_week = Customer.objects.filter(
            Q(birth_date__month=start_month, birth_date__day__gte=start_day) |
            Q(birth_date__month=end_month, birth_date__day__lte=end_day)
        ).count()
    
    context = {
        'total_customers': total_customers,
        'total_companies': total_companies,
        'total_sales_reps': total_sales_reps,
        'total_interactions': total_interactions,
        'birthdays_today': birthdays_today,
        'birthdays_this_week': birthdays_this_week,
    }
    
    return render(request, 'crm/dashboard.html', context)

