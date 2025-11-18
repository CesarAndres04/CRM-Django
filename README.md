# 🎯 Sistema CRM Django

Una aplicación completa de CRM (Customer Relationship Management) desarrollada con Django que gestiona clientes, compañías, representantes de ventas e interacciones.

## 📋 Características

- ✅ Gestión de 1000 clientes con datos completos
- ✅ Más de 500,000 interacciones registradas (500 por cliente)
- ✅ 3 representantes de ventas
- ✅ Compañías asociadas a clientes
- ✅ Dashboard con estadísticas en tiempo real
- ✅ Filtros avanzados por nombre, compañía y cumpleaños
- ✅ Ordenamiento por múltiples criterios
- ✅ Interfaz moderna y responsiva
- ✅ Paginación optimizada
- ✅ Panel de administración de Django

## 🗄️ Estructura de Base de Datos

### Users (Representantes de Ventas)
- ID
- Nombre de usuario
- Email (único)
- Nombre completo
- Contraseña cifrada
- Es administrador (booleano)
- Es representante de ventas (booleano)
- Fechas de creación/actualización

### Companies (Compañías)
- ID
- Nombre
- Fechas de creación/actualización

### Customers (Clientes)
- ID
- Nombre y apellido
- Fecha de nacimiento
- Relación con Company
- Relación con User (representante)
- Fechas de creación/actualización

### Interactions (Interacciones)
- ID
- Cliente asociado
- Tipo (Call, Email, SMS, WhatsApp, Facebook, LinkedIn, Meeting, Video Call)
- Fecha de interacción
- Notas (opcional)
- Fecha de creación

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Instalar Dependencias

Las dependencias ya están instaladas en el sistema:
- Django 4.2.26
- Faker (para generar datos ficticios)

Si necesitas reinstalarlas:
```bash
/usr/bin/python3 -m pip install django faker
```

### Paso 2: Verificar Migraciones

Las migraciones ya están aplicadas. Si necesitas reaplicarlas:
```bash
cd /Users/cesarandres/Documents/CRM:TEST
/usr/bin/python3 manage.py migrate
```

### Paso 3: Generar Datos Ficticios

**IMPORTANTE:** Este proceso puede tomar varios minutos debido a la generación de ~500,000 interacciones.

```bash
cd /Users/cesarandres/Documents/CRM:TEST
/usr/bin/python3 manage.py generate_fake_data
```

Opciones personalizables:
```bash
# Personalizar cantidad de datos
/usr/bin/python3 manage.py generate_fake_data --users 5 --customers 2000 --interactions-per-customer 300
```

**Nota:** El comando por defecto genera:
- 3 representantes de ventas (rep1, rep2, rep3)
- 1 superusuario (admin)
- 1000 clientes
- ~100 compañías
- 500,000 interacciones (500 por cliente)

### Paso 4: Iniciar el Servidor

```bash
cd /Users/cesarandres/Documents/CRM:TEST
/usr/bin/python3 manage.py runserver
```

El servidor estará disponible en: **http://127.0.0.1:8000**

## 🔐 Credenciales de Acceso

### Panel de Administración
- **URL:** http://127.0.0.1:8000/admin/
- **Usuario:** admin
- **Contraseña:** admin123

### Representantes de Ventas
- **Usuarios:** rep1, rep2, rep3
- **Contraseña:** password123

## 🖥️ Uso de la Aplicación

### Dashboard Principal
- **URL:** http://127.0.0.1:8000/
- Muestra estadísticas generales del CRM
- Lista de cumpleaños del día
- Contador de cumpleaños de la semana
- Acciones rápidas

### Lista de Clientes
- **URL:** http://127.0.0.1:8000/customers/

#### Filtros Disponibles:
1. **Búsqueda por texto:** Busca en nombres de clientes y compañías
2. **Filtro de cumpleaños:**
   - Hoy
   - Esta semana
   - Este mes

#### Ordenamiento:
- Por nombre (A-Z)
- Por compañía (A-Z)
- Por fecha de cumpleaños (mes y día)
- Por última interacción (más reciente primero)

### Información Mostrada:
- Nombre completo del cliente
- Compañía asociada
- Cumpleaños (formato: "February 5")
- Última interacción (ej: "2 days ago (Email)")
- Representante asignado

### Paginación
- 50 clientes por página
- Navegación entre páginas manteniendo filtros

## 📊 Panel de Administración Django

El panel de administración permite:
- Crear, editar y eliminar usuarios
- Gestionar compañías
- Administrar clientes
- Ver y filtrar interacciones
- Búsqueda avanzada

## 🎨 Características Técnicas

### Optimizaciones de Rendimiento
- **select_related()** para optimizar queries de relaciones 1-to-1 y ForeignKey
- **prefetch_related()** para cargar interacciones de forma eficiente
- **Índices de base de datos** en campos frecuentemente consultados
- **bulk_create()** para inserción masiva de datos
- **Paginación** para manejar grandes volúmenes de datos

### Modelos con Propiedades Útiles
- `Customer.birthday_formatted` - Cumpleaños en formato legible
- `Customer.get_last_interaction()` - Obtiene la última interacción
- `Customer.get_last_interaction_display()` - Formato "X days ago (Type)"
- `Customer.birthday_this_week()` - Verifica si cumpleaños es esta semana

### Frontend Moderno
- CSS3 con gradientes y sombras
- Diseño responsivo (móvil y escritorio)
- Interfaz tipo Material Design
- Transiciones y animaciones suaves

## 📁 Estructura del Proyecto

```
CRM:TEST/
├── crm/                          # Aplicación principal
│   ├── migrations/               # Migraciones de base de datos
│   ├── management/
│   │   └── commands/
│   │       └── generate_fake_data.py  # Comando para generar datos
│   ├── templates/
│   │   └── crm/
│   │       ├── base.html         # Template base
│   │       ├── dashboard.html    # Dashboard principal
│   │       └── customer_list.html # Lista de clientes
│   ├── admin.py                  # Configuración del admin
│   ├── models.py                 # Modelos de datos
│   ├── views.py                  # Vistas del CRM
│   └── urls.py                   # URLs de la app
├── crm_project/                  # Configuración del proyecto
│   ├── settings.py               # Configuración Django
│   └── urls.py                   # URLs principales
├── manage.py                     # Script de gestión Django
├── db.sqlite3                    # Base de datos SQLite
└── README.md                     # Este archivo
```

## 🔧 Comandos Útiles

### Ver estadísticas de la base de datos
```bash
/usr/bin/python3 manage.py shell
>>> from crm.models import User, Company, Customer, Interaction
>>> print(f"Users: {User.objects.count()}")
>>> print(f"Companies: {Company.objects.count()}")
>>> print(f"Customers: {Customer.objects.count()}")
>>> print(f"Interactions: {Interaction.objects.count()}")
```

### Limpiar base de datos y regenerar
```bash
# Eliminar base de datos
rm db.sqlite3

# Reaplicar migraciones
/usr/bin/python3 manage.py migrate

# Regenerar datos
/usr/bin/python3 manage.py generate_fake_data
```

### Crear más usuarios administradores
```bash
/usr/bin/python3 manage.py createsuperuser
```

## 📈 Próximas Mejoras Sugeridas

- [ ] Agregar autenticación obligatoria
- [ ] Implementar API REST con Django REST Framework
- [ ] Agregar gráficos con Chart.js o Plotly
- [ ] Exportar datos a CSV/Excel
- [ ] Implementar notificaciones de cumpleaños
- [ ] Agregar búsqueda full-text con PostgreSQL
- [ ] Dashboard personalizado por representante
- [ ] Reportes avanzados de interacciones

## 🐛 Solución de Problemas

### Error al generar datos
- Asegúrate de tener suficiente espacio en disco (la BD puede ocupar ~500MB)
- El proceso puede tomar 5-10 minutos

### Lentitud en la aplicación
- Verifica que los índices estén creados correctamente
- Considera usar PostgreSQL en lugar de SQLite para mejor rendimiento
- Ajusta el número de interacciones por cliente

### Error de importación
- Verifica que todas las dependencias estén instaladas
- Asegúrate de estar en el directorio correcto

## 📝 Notas Adicionales

- La aplicación usa SQLite por defecto (ideal para desarrollo)
- Para producción, se recomienda PostgreSQL o MySQL
- Los datos son completamente ficticios generados con Faker
- Las fechas de interacción están distribuidas en los últimos 2 años

## 👨‍💻 Desarrollo

Desarrollado con:
- Python 3.9.6
- Django 4.2.26
- Faker para datos ficticios
- SQLite como base de datos

---

**¡Listo para usar!** 🚀

Ejecuta los comandos de instalación y tendrás un CRM completamente funcional con medio millón de interacciones.
