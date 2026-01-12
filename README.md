# 💰 FacturaFlow

Sistema completo de gestión de facturación y cobranzas con seguimiento automático, alertas y envío de emails.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📸 Screenshots

![Dashboard](https://via.placeholder.com/800x400?text=Dashboard+Screenshot)
![Facturas](https://via.placeholder.com/800x400?text=Facturas+Screenshot)

## 🚀 Características

### ✅ Gestión de Facturas
- ✨ Crear, editar y eliminar facturas
- 📊 Estados: Pendiente, En seguimiento, Pagada, Vencida
- 💵 Control de montos y fechas de vencimiento
- 📝 Descripción y notas adicionales

### 👥 Gestión de Clientes
- 📇 Base de datos de clientes
- 📧 Email y contacto
- 🏢 Información de empresa

### 🔔 Sistema de Alertas Automáticas
- ⚠️ Facturas próximas a vencer (5 días)
- 🔴 Facturas vencidas
- 📊 Dashboard con estadísticas en tiempo real

### 📧 Automatización de Emails
- 📨 Envío manual de recordatorios
- 🤖 Emails automáticos predefinidos
- 📋 Historial completo de emails enviados
- 📊 Registro de todas las comunicaciones

### 📊 Dashboard Visual
- 💹 Estadísticas globales
- 📈 Montos pendientes y vencidos
- 🎯 Vista por estados
- 🔍 Filtros avanzados

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para manejo de base de datos
- **SQLite** - Base de datos (fácil migración a PostgreSQL)
- **Pydantic** - Validación de datos
- **aiosmtplib** - Envío asíncrono de emails

### Frontend
- **HTML5 + CSS3** - Interfaz moderna y responsive
- **Vanilla JavaScript** - Sin dependencias adicionales
- **Fetch API** - Comunicación con el backend

## 📦 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar/Descargar el Proyecto
```bash
git clone https://github.com/tu-usuario/facturaflow.git
cd facturaflow
```

### Paso 2: Configurar el Backend

#### Crear entorno virtual (recomendado)
```bash
cd backend
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

#### Instalar dependencias
```bash
pip install -r requirements.txt
```

#### Configurar variables de entorno
1. Copiar el archivo de ejemplo:
```bash
copy .env.example .env
```

2. Editar `.env` con tus datos:
```env
# Configuración de Email (SMTP)
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
SMTP_USER=tu_email@outlook.com
SMTP_PASSWORD=tu_password
SMTP_FROM=tu_email@outlook.com
```

**Nota sobre el email:**
- Para Outlook/Hotmail: usa `smtp.office365.com`
- Para Gmail: usa `smtp.gmail.com` (requiere habilitar "Apps menos seguras" o usar App Password)
- Puerto 587 para TLS es el estándar

### Paso 3: Iniciar el Sistema

#### Opción A: Usar el script de inicio (Recomendado)
```bash
# Desde la raíz del proyecto
.\start.bat
```

#### Opción B: Inicio manual

**Terminal 1 - Backend:**
```bash
cd backend
# Activar entorno virtual
venv\Scripts\activate
# Iniciar servidor
python main.py
```

El backend estará disponible en: `http://localhost:8000`

**Terminal 2 - Frontend:**
```bash
cd frontend
# Iniciar servidor web simple
python -m http.server 3000
```

El frontend estará disponible en: `http://localhost:3000`

## 📖 Uso del Sistema

### 1️⃣ Primer Uso

1. Abrir el navegador en `http://localhost:3000`
2. Crear al menos un cliente desde "➕ Nuevo Cliente"
3. Crear facturas desde "📄 Nueva Factura"

### 2️⃣ Gestión de Facturas

**Crear Factura:**
- Click en "📄 Nueva Factura"
- Completar número, cliente, monto y fecha de vencimiento
- Agregar descripción opcional

**Estados de Factura:**
- 🔵 **Pendiente**: Recién creada, sin seguimiento
- 🟡 **En seguimiento**: Se enviaron recordatorios
- 🟢 **Pagada**: Cobro completado
- 🔴 **Vencida**: Pasó la fecha de vencimiento (automático)

**Acciones rápidas:**
- 📧 Enviar email personalizado
- ✓ Marcar como pagada
- 🗑️ Eliminar factura

### 3️⃣ Sistema de Alertas

El sistema muestra automáticamente:
- ⚠️ Facturas que vencen en 5 días o menos
- 🔴 Facturas vencidas

**Enviar Recordatorio Rápido:**
- Click en "📧 Enviar Recordatorio" en la alerta
- El sistema genera un email automático según el estado

### 4️⃣ Envío de Emails

**Email Personalizado:**
1. Click en 📧 junto a la factura
2. Editar asunto y cuerpo del mensaje
3. Enviar

**Email Automático:**
- Click en "📧 Enviar Recordatorio" en alertas
- Texto generado según días de vencimiento

**Historial:**
- Columna "Emails" muestra cantidad enviada
- Todos los emails quedan registrados en la base de datos

### 5️⃣ Dashboard y Estadísticas

El dashboard muestra:
- 📊 Total de facturas
- ⏰ Facturas pendientes
- ⚠️ Facturas vencidas
- ✅ Facturas pagadas
- 💵 Monto total pendiente de cobro
- 🔴 Monto total vencido

## 🔧 Configuración Avanzada

### Cambiar a PostgreSQL

1. Instalar PostgreSQL y crear base de datos

2. Actualizar `.env`:
```env
DATABASE_URL=postgresql://usuario:password@localhost/facturacion_db
```

3. Instalar driver:
```bash
pip install psycopg2-binary
```

### Configurar Gmail como SMTP

1. Habilitar verificación en 2 pasos en Gmail
2. Generar "Contraseña de Aplicación"
3. Actualizar `.env`:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu_email@gmail.com
SMTP_PASSWORD=tu_app_password_generado
```

### Personalizar Alertas

Editar `backend/main.py`, función `obtener_alertas()`:
```python
# Cambiar días de alerta (por defecto: 5)
models.Factura.fecha_vencimiento <= hoy + timedelta(days=3)  # 3 días
```

## 📁 Estructura del Proyecto

```
facturaflow/
├── backend/
│   ├── main.py              # API FastAPI
│   ├── models.py            # Modelos de base de datos
│   ├── schemas.py           # Schemas Pydantic
│   ├── database.py          # Configuración DB
│   ├── email_service.py     # Sistema de emails
│   ├── config.py            # Configuración
│   ├── requirements.txt     # Dependencias Python
│   ├── .env                 # Variables de entorno (crear)
│   └── .env.example         # Ejemplo de configuración
├── frontend/
│   ├── index.html           # UI principal
│   ├── styles.css           # Estilos
│   └── app.js               # Lógica del frontend
├── start.bat                # Script de inicio (Windows)
└── README.md                # Esta documentación
```

## 🔍 API Endpoints

### Clientes
- `GET /api/clientes/` - Listar todos
- `POST /api/clientes/` - Crear nuevo
- `GET /api/clientes/{id}` - Obtener uno
- `PUT /api/clientes/{id}` - Actualizar
- `DELETE /api/clientes/{id}` - Eliminar

### Facturas
- `GET /api/facturas/` - Listar todas (filtro: `?estado=Pendiente`)
- `POST /api/facturas/` - Crear nueva
- `GET /api/facturas/{id}` - Obtener una
- `PUT /api/facturas/{id}` - Actualizar
- `DELETE /api/facturas/{id}` - Eliminar

### Dashboard
- `GET /api/dashboard/stats` - Estadísticas generales
- `GET /api/alertas/` - Obtener alertas activas

### Emails
- `POST /api/emails/enviar` - Enviar email personalizado
- `POST /api/emails/recordatorio/{id}` - Enviar recordatorio automático
- `GET /api/emails/{factura_id}` - Historial de emails

### Documentación Interactiva
- `http://localhost:8000/docs` - Swagger UI
- `http://localhost:8000/redoc` - ReDoc

## 🐛 Solución de Problemas

### Error: "No se puede conectar al backend"
- Verificar que el backend esté corriendo en puerto 8000
- Revisar la consola del navegador (F12)
- Verificar que no haya firewall bloqueando

### Error: "No se pueden enviar emails"
- Verificar configuración SMTP en `.env`
- Para Outlook: verificar que la cuenta permita SMTP
- Para Gmail: usar "Contraseña de Aplicación"
- Revisar logs del backend

### Error: "Base de datos bloqueada"
- SQLite solo permite una escritura a la vez
- Reiniciar el servidor backend
- Considerar migrar a PostgreSQL para producción

### Frontend no carga datos
- Abrir consola del navegador (F12)
- Verificar que el backend responda: `http://localhost:8000`
- Revisar que CORS esté configurado correctamente

## 🚀 Mejoras Futuras

- [ ] Autenticación de usuarios
- [ ] Reportes en PDF
- [ ] Gráficos de estadísticas
- [ ] Envío masivo de recordatorios
- [ ] Integración con pasarelas de pago
- [ ] Notificaciones push
- [ ] Multi-empresa/multi-usuario
- [ ] API REST completa documentada
- [ ] Tests automatizados
- [ ] Deploy en cloud (Heroku, Railway, etc.)

## 📝 Licencia

Este proyecto es de uso libre para fines personales y comerciales.

## 👨‍💻 Soporte

Para dudas o problemas:
1. Revisar esta documentación
2. Verificar logs del backend
3. Consultar la documentación de FastAPI: https://fastapi.tiangolo.com/

---

**¡Gestiona tus facturas de forma inteligente! 💰✨**
