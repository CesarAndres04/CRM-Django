# 📋 Instrucciones para Clonar y Ejecutar desde GitHub

## 🚀 Instalación Rápida

### 1. Clonar el Repositorio
```bash
git clone https://github.com/TU_USUARIO/CRM-Django.git
cd CRM-Django
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Aplicar Migraciones
```bash
python manage.py migrate
```

### 4. Generar Datos Ficticios
```bash
python manage.py generate_fake_data
```
⚠️ **Nota**: Este proceso puede tomar 5-10 minutos para generar 500,000 interacciones.

### 5. Iniciar el Servidor
```bash
python manage.py runserver
```

### 6. Acceder a la Aplicación
- **Dashboard**: http://127.0.0.1:8000/
- **Lista de Clientes**: http://127.0.0.1:8000/customers/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 🔐 Credenciales por Defecto

Después de ejecutar `generate_fake_data`:

**Admin:**
- Usuario: `admin`
- Contraseña: `admin123`

**Representantes:**
- Usuarios: `rep1`, `rep2`, `rep3`
- Contraseña: `password123`

## 📝 Requisitos del Sistema
- Python 3.8+
- pip

## ⚠️ Importante
La base de datos SQLite (`db.sqlite3`) NO está incluida en el repositorio. Debes generarla ejecutando los pasos 3 y 4.
