# 📧 Servicio de Email Mejorado

## Características Implementadas

### ✅ 1. Logging Profesional
- Sistema de logging estructurado con niveles (INFO, WARNING, ERROR)
- Formato detallado con timestamps
- Trazabilidad completa de cada operación

### ✅ 2. Templates HTML
- Emails profesionales con diseño responsive
- Estilos CSS integrados
- Templates dinámicos con Jinja2
- Colores diferenciados por urgencia (azul/rojo)

### ✅ 3. Validación de Emails
- Validación de formato con `email-validator`
- Errores claros y específicos
- Prevención de envíos a direcciones inválidas

### ✅ 4. Reintentos Automáticos
- Hasta 3 intentos por defecto (configurable)
- Backoff exponencial (2^intento segundos)
- Manejo de errores SMTP transitorios

### ✅ 5. Soporte para Adjuntos
- Adjuntar archivos PDF de facturas
- Múltiples archivos en un solo email
- Formato MIME correcto

### ✅ 6. Rate Limiting
- Máximo 30 emails por minuto (configurable)
- Previene bloqueos por spam
- Espera automática cuando se alcanza el límite

### ✅ 7. Modo de Prueba
- Parámetro `modo_prueba=True` para testing
- No envía emails reales
- Log detallado de lo que se enviaría

### ✅ 8. Manejo de Errores
- Excepciones personalizadas:
  - `EmailServiceError` (base)
  - `EmailValidationError` (email inválido)
  - `EmailSendError` (fallo al enviar)
- Información detallada de errores

## Uso

### Ejemplo Básico

```python
from email_service import enviar_email

# Enviar email simple
await enviar_email(
    destinatario="cliente@ejemplo.com",
    asunto="Notificación",
    cuerpo="Contenido del mensaje",
    modo_prueba=True  # Cambiar a False para enviar realmente
)
```

### Email con Template HTML

```python
from email_service import generar_email_recordatorio, enviar_email

# Generar recordatorio con template HTML profesional
asunto, cuerpo = generar_email_recordatorio(
    numero_factura="FAC-2025-001",
    cliente="Juan Pérez",
    monto=15000.50,
    dias=5,  # Vence en 5 días (positivo) o vencida hace X días (negativo)
    html=True
)

await enviar_email(
    destinatario="cliente@ejemplo.com",
    asunto=asunto,
    cuerpo=cuerpo,
    es_html=True
)
```

### Email con Adjuntos

```python
# Leer PDF
with open("factura.pdf", "rb") as f:
    contenido_pdf = f.read()

# Enviar con adjunto
await enviar_email(
    destinatario="cliente@ejemplo.com",
    asunto="Su Factura",
    cuerpo="Adjunto encontrará su factura.",
    adjuntos=[
        ("factura_001.pdf", contenido_pdf),
        ("recibo.pdf", contenido_recibo)  # Múltiples adjuntos
    ]
)
```

### Envío Masivo con Rate Limiting

```python
destinatarios = ["cliente1@ejemplo.com", "cliente2@ejemplo.com", ...]

for destinatario in destinatarios:
    try:
        # El rate limiting se aplica automáticamente
        await enviar_email(
            destinatario=destinatario,
            asunto="Newsletter",
            cuerpo="Contenido"
        )
    except EmailSendError as e:
        print(f"Error con {destinatario}: {e}")
```

### Manejo de Errores

```python
from email_service import (
    enviar_email,
    EmailValidationError,
    EmailSendError,
    EmailServiceError
)

try:
    await enviar_email(
        destinatario="invalido@",
        asunto="Test",
        cuerpo="Contenido"
    )
except EmailValidationError as e:
    print(f"Email inválido: {e}")
except EmailSendError as e:
    print(f"Fallo al enviar: {e}")
except EmailServiceError as e:
    print(f"Error del servicio: {e}")
```

## Configuración

### Variables de Entorno (.env)

```env
# SMTP Configuration
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
SMTP_USER=tu-email@dominio.com
SMTP_PASSWORD=tu-password
SMTP_FROM=noreply@tuempresa.com

# App
APP_NAME=FacturaFlow
```

### Parámetros Configurables

```python
# En email_service.py
MAX_EMAILS_PER_MINUTE = 30  # Rate limiting

# En enviar_email()
max_reintentos: int = 3  # Número de reintentos
timeout: int = 30  # Timeout de conexión en segundos
```

## Template HTML

El template HTML incluye:

- 📱 Diseño responsive
- 🎨 Colores según urgencia (azul: recordatorio, rojo: urgente)
- 📊 Tabla con detalles de la factura
- 🔘 Botón de llamada a la acción
- 📧 Footer profesional con disclaimer

### Personalización del Template

Puedes modificar el template HTML en la función `generar_email_recordatorio()`:

```python
# Cambiar colores
color_urgencia = "#2196F3"  # Azul
color_urgencia = "#F44336"  # Rojo

# Modificar estilos
# Edita la sección <style> en el template
```

## Testing

### Ejecutar Ejemplos

```bash
cd backend
python email_example.py
```

### Modo Prueba

```python
# No envía emails reales, solo muestra logs
await enviar_email(
    destinatario="test@ejemplo.com",
    asunto="Test",
    cuerpo="Prueba",
    modo_prueba=True  # ← Activa modo prueba
)
```

## Logs

El servicio genera logs detallados:

```
2026-01-03 10:30:45 - email_service - INFO - Enviando email a cliente@ejemplo.com (intento 1/3)
2026-01-03 10:30:46 - email_service - INFO - Adjuntado archivo: factura_001.pdf
2026-01-03 10:30:47 - email_service - INFO - ✓ Email enviado exitosamente a cliente@ejemplo.com
```

## Mejores Prácticas

1. **Siempre usa modo prueba** para desarrollo
2. **Valida emails** antes de procesamiento masivo
3. **Monitorea logs** para detectar problemas
4. **Configura rate limiting** según tu proveedor SMTP
5. **Usa HTML** para emails profesionales
6. **Incluye adjuntos** solo cuando sea necesario
7. **Maneja excepciones** específicamente

## Solución de Problemas

### Email no se envía

1. Verifica configuración SMTP en `.env`
2. Revisa logs para errores específicos
3. Prueba credenciales con modo_prueba=False
4. Verifica firewall/antivirus

### Rate Limiting muy restrictivo

```python
# Ajustar en email_service.py
MAX_EMAILS_PER_MINUTE = 60  # Aumentar límite
```

### Timeout en envío

```python
await enviar_email(
    ...,
    max_reintentos=5  # Más reintentos
)
```

## Próximas Mejoras Posibles

- [ ] Templates desde archivos externos
- [ ] Cola de envío con Celery
- [ ] Estadísticas de envío
- [ ] Webhooks para eventos
- [ ] Soporte para múltiples proveedores SMTP
- [ ] Tracking de apertura de emails
- [ ] Desuscripción automática
- [ ] A/B Testing de templates
