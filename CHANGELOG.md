# 📝 Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.0.0] - 2026-01-12

### ✨ Agregado

#### Gestión de Clientes
- Sistema completo CRUD para clientes
- Modal para crear nuevos clientes
- Modal para ver detalles completos del cliente
- Modal para editar información del cliente
- Función para eliminar clientes con confirmación
- Visualización de facturas asociadas a cada cliente
- Validación de campos obligatorios

#### Gestión de Facturas
- Sistema completo CRUD para facturas
- Modal para crear nuevas facturas
- Modal para ver detalles completos de la factura
- Modal para editar facturas existentes
- Función para eliminar facturas con confirmación
- Selección de cliente desde lista desplegable
- Estados de factura: Pendiente, En seguimiento, Pagada, Vencida
- Historial de emails enviados por factura
- Validación de campos y fechas

#### Sistema de Emails
- Envío de recordatorios automáticos
- Templates HTML profesionales
- Registro de emails enviados
- Estado de envío (Enviado/Error)
- Integración con SMTP (Office365, Gmail, etc.)

#### Dashboard
- Estadísticas en tiempo real
- Tarjetas con métricas clave
- Total de facturas
- Facturas pendientes, vencidas y pagadas
- Montos totales pendientes y vencidos
- Lista de alertas recientes

#### Sistema de Alertas
- Alertas de facturas próximas a vencer (5 días)
- Alertas de facturas vencidas
- Actualización automática de estados
- Página dedicada de notificaciones
- Filtros por tipo de alerta

#### Interface de Usuario
- Diseño responsive para todos los dispositivos
- Sistema de navegación con sidebar
- Modales modernos con animaciones
- Badges de estado con colores
- Botones de acción con iconos
- Tablas responsivas
- Filtros por estado de factura
- Sistema de autenticación por sesión

#### Backend
- API RESTful completa con FastAPI
- Documentación automática con Swagger
- Base de datos SQLite (migrable a PostgreSQL)
- Modelos relacionales con SQLAlchemy
- Validación de datos con Pydantic
- Sistema de logs de emails
- Endpoints CRUD completos
- Manejo de errores HTTP

### 🔧 Configuración
- Archivo `.env` para configuración
- Script de inicio automático (`start.bat`)
- Instalación automática de dependencias
- Verificación de entorno virtual
- Servidor HTTP para frontend
- Configuración de CORS

### 📚 Documentación
- README.md completo con instrucciones
- QUICKSTART.md para inicio rápido
- EMAIL_SERVICE_README.md para configuración de email
- Comentarios en código
- Docstrings en funciones Python

### 🎨 Diseño
- Paleta de colores moderna
- Tipografía Inter
- Iconos emoji para mejor UX
- Animaciones suaves
- Estados hover en botones
- Transiciones CSS

### 🔒 Seguridad
- Validación de entrada de datos
- Sanitización de campos
- Manejo seguro de credenciales (.env)
- Exclusión de archivos sensibles (.gitignore)

## [0.1.0] - 2026-01-10

### 🎉 Inicial
- Estructura básica del proyecto
- Configuración inicial de backend
- Configuración inicial de frontend
- Modelos de base de datos
- API básica

---

## 🔖 Tipos de Cambios

- `Agregado` para nuevas funcionalidades
- `Cambiado` para cambios en funcionalidad existente
- `Deprecado` para funcionalidades que se eliminarán pronto
- `Eliminado` para funcionalidades eliminadas
- `Corregido` para correcciones de bugs
- `Seguridad` para vulnerabilidades

---

**Formato de versiones**: [MAJOR.MINOR.PATCH]

- **MAJOR**: Cambios incompatibles en la API
- **MINOR**: Nueva funcionalidad compatible hacia atrás
- **PATCH**: Corrección de bugs compatible hacia atrás
