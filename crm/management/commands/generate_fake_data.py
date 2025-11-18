from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from datetime import timedelta
from crm.models import User, Company, Customer, Interaction


class Command(BaseCommand):
    help = 'Genera datos ficticios para el CRM: 3 representantes, 1000 clientes, y ~500,000 interacciones'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=3,
            help='Número de representantes de ventas a crear (default: 3)'
        )
        parser.add_argument(
            '--customers',
            type=int,
            default=1000,
            help='Número de clientes a crear (default: 1000)'
        )
        parser.add_argument(
            '--interactions-per-customer',
            type=int,
            default=500,
            help='Número de interacciones por cliente (default: 500)'
        )

    def handle(self, *args, **options):
        fake = Faker()
        
        num_users = options['users']
        num_customers = options['customers']
        interactions_per_customer = options['interactions_per_customer']
        
        self.stdout.write(self.style.SUCCESS('🚀 Iniciando generación de datos ficticios...'))
        
        # Limpiar datos existentes (opcional, comenta si quieres mantener datos)
        self.stdout.write('Limpiando datos existentes...')
        Interaction.objects.all().delete()
        Customer.objects.all().delete()
        Company.objects.all().delete()
        User.objects.all().delete()
        
        # 1. Crear representantes de ventas
        self.stdout.write(f'Creando {num_users} representantes de ventas...')
        users = []
        for i in range(num_users):
            user = User.objects.create_user(
                username=f'rep{i+1}',
                email=fake.email(),
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                is_sales_rep=True
            )
            users.append(user)
            self.stdout.write(f'  ✓ Creado: {user.get_full_name()}')
        
        # Crear un superusuario para el admin
        self.stdout.write('Creando superusuario admin...')
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@crm.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        self.stdout.write(f'  ✓ Superusuario creado: admin / admin123')
        
        # 2. Crear compañías
        self.stdout.write(f'Creando compañías...')
        companies = []
        num_companies = min(100, num_customers // 5)  # Aproximadamente 5 clientes por compañía
        
        # Usar un set para asegurar nombres únicos
        company_names = set()
        while len(company_names) < num_companies:
            company_names.add(fake.company())
        
        for company_name in company_names:
            company = Company.objects.create(name=company_name)
            companies.append(company)
        
        self.stdout.write(f'  ✓ Creadas {len(companies)} compañías')
        
        # 3. Crear clientes
        self.stdout.write(f'Creando {num_customers} clientes...')
        customers = []
        batch_size = 100
        for i in range(0, num_customers, batch_size):
            batch = []
            end = min(i + batch_size, num_customers)
            for j in range(i, end):
                customer = Customer(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    birth_date=fake.date_of_birth(minimum_age=18, maximum_age=80),
                    company=random.choice(companies),
                    sales_rep=random.choice(users)
                )
                batch.append(customer)
            
            Customer.objects.bulk_create(batch)
            customers.extend(batch)
            self.stdout.write(f'  ✓ Creados {end}/{num_customers} clientes')
        
        # Refrescar los clientes desde la base de datos para tener IDs
        customers = list(Customer.objects.all())
        
        # 4. Crear interacciones (esto tomará más tiempo)
        self.stdout.write(f'Creando ~{num_customers * interactions_per_customer:,} interacciones...')
        interaction_types = [choice[0] for choice in Interaction.INTERACTION_TYPES]
        
        total_interactions = 0
        batch_size = 1000
        interactions_batch = []
        
        for idx, customer in enumerate(customers):
            # Generar interacciones para este cliente
            for j in range(interactions_per_customer):
                # Fecha aleatoria en los últimos 2 años
                days_ago = random.randint(0, 730)
                interaction_date = timezone.now() - timedelta(days=days_ago)
                
                interaction = Interaction(
                    customer=customer,
                    interaction_type=random.choice(interaction_types),
                    interaction_date=interaction_date,
                    notes=fake.sentence() if random.random() > 0.7 else ''
                )
                interactions_batch.append(interaction)
                total_interactions += 1
                
                # Insertar en lotes para optimizar
                if len(interactions_batch) >= batch_size:
                    Interaction.objects.bulk_create(interactions_batch)
                    interactions_batch = []
                    self.stdout.write(f'  ✓ Creadas {total_interactions:,} interacciones...')
            
            # Mostrar progreso por cliente
            if (idx + 1) % 50 == 0:
                self.stdout.write(f'  ✓ Procesados {idx + 1}/{num_customers} clientes')
        
        # Insertar las interacciones restantes
        if interactions_batch:
            Interaction.objects.bulk_create(interactions_batch)
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Datos generados exitosamente!'))
        self.stdout.write(self.style.SUCCESS(f'  - {User.objects.count()} usuarios (incluyendo admin)'))
        self.stdout.write(self.style.SUCCESS(f'  - {Company.objects.count()} compañías'))
        self.stdout.write(self.style.SUCCESS(f'  - {Customer.objects.count()} clientes'))
        self.stdout.write(self.style.SUCCESS(f'  - {Interaction.objects.count():,} interacciones'))
        self.stdout.write(self.style.SUCCESS(f'\n🔐 Credenciales de acceso:'))
        self.stdout.write(self.style.SUCCESS(f'  Admin: admin / admin123'))
        self.stdout.write(self.style.SUCCESS(f'  Representantes: rep1, rep2, rep3 / password123'))
