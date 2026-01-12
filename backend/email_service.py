import aiosmtplib
import asyncio
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email_validator import validate_email, EmailNotValidError
from jinja2 import Template
from pathlib import Path
from config import get_settings
from typing import Optional, List
from datetime import datetime
import time

# Configurar logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

settings = get_settings()

# Rate limiting global
_last_email_time = 0
_email_count = 0
_reset_time = 0
MAX_EMAILS_PER_MINUTE = 30


class EmailServiceError(Exception):
    """Excepción base para errores del servicio de email"""
    pass


class EmailValidationError(EmailServiceError):
    """Error de validación de email"""
    pass


class EmailSendError(EmailServiceError):
    """Error al enviar email"""
    pass


def validar_email(email: str) -> bool:
    """
    Valida el formato de un email
    
    Args:
        email: Dirección de email a validar
        
    Returns:
        True si es válido
        
    Raises:
        EmailValidationError: Si el email no es válido
    """
    try:
        validate_email(email, check_deliverability=False)
        return True
    except EmailNotValidError as e:
        logger.error(f"Email inválido '{email}': {str(e)}")
        raise EmailValidationError(f"Email inválido: {str(e)}")


async def _apply_rate_limit():
    """Aplica rate limiting para evitar bloqueos por spam"""
    global _last_email_time, _email_count, _reset_time
    
    current_time = time.time()
    
    # Resetear contador cada minuto
    if current_time - _reset_time > 60:
        _email_count = 0
        _reset_time = current_time
    
    # Si se alcanzó el límite, esperar
    if _email_count >= MAX_EMAILS_PER_MINUTE:
        wait_time = 60 - (current_time - _reset_time)
        if wait_time > 0:
            logger.warning(f"Rate limit alcanzado. Esperando {wait_time:.1f}s")
            await asyncio.sleep(wait_time)
            _email_count = 0
            _reset_time = time.time()
    
    _email_count += 1
    _last_email_time = current_time


async def enviar_email(
    destinatario: str,
    asunto: str,
    cuerpo: str,
    es_html: bool = False,
    adjuntos: Optional[List[tuple[str, bytes]]] = None,
    max_reintentos: int = 3,
    modo_prueba: bool = False
) -> bool:
    """
    Envía un email usando SMTP con reintentos automáticos
    
    Args:
        destinatario: Email del destinatario
        asunto: Asunto del email
        cuerpo: Contenido del email
        es_html: Si el cuerpo es HTML
        adjuntos: Lista de tuplas (nombre_archivo, contenido_bytes)
        max_reintentos: Número máximo de intentos
        modo_prueba: Si es True, no envía el email realmente
        
    Returns:
        True si se envió exitosamente
        
    Raises:
        EmailValidationError: Si el email no es válido
        EmailSendError: Si falla el envío después de todos los reintentos
    """
    # Validar configuración
    if not settings.smtp_user or not settings.smtp_password:
        logger.error("Configuración SMTP no establecida")
        raise EmailServiceError("Configuración de email incompleta")
    
    # Validar email
    validar_email(destinatario)
    
    # Modo prueba
    if modo_prueba:
        logger.info(f"[MODO PRUEBA] Email a {destinatario}: {asunto}")
        logger.debug(f"[MODO PRUEBA] Cuerpo: {cuerpo[:100]}...")
        return True
    
    # Aplicar rate limiting
    await _apply_rate_limit()
    
    # Construir mensaje
    message = MIMEMultipart("alternative")
    message["From"] = settings.smtp_from
    message["To"] = destinatario
    message["Subject"] = asunto
    message["Date"] = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")
    
    # Agregar el cuerpo
    mime_type = "html" if es_html else "plain"
    message.attach(MIMEText(cuerpo, mime_type, "utf-8"))
    
    # Agregar adjuntos si existen
    if adjuntos:
        for nombre, contenido in adjuntos:
            adjunto = MIMEApplication(contenido)
            adjunto.add_header('Content-Disposition', 'attachment', filename=nombre)
            message.attach(adjunto)
            logger.info(f"Adjuntado archivo: {nombre}")
    
    # Reintentos con backoff exponencial
    for intento in range(max_reintentos):
        try:
            logger.info(f"Enviando email a {destinatario} (intento {intento + 1}/{max_reintentos})")
            
            await aiosmtplib.send(
                message,
                hostname=settings.smtp_host,
                port=settings.smtp_port,
                username=settings.smtp_user,
                password=settings.smtp_password,
                start_tls=True,
                timeout=30
            )
            
            logger.info(f"✓ Email enviado exitosamente a {destinatario}")
            return True
            
        except aiosmtplib.SMTPException as e:
            logger.warning(f"Error SMTP en intento {intento + 1}: {str(e)}")
            if intento < max_reintentos - 1:
                # Backoff exponencial: 2^intento segundos
                espera = 2 ** intento
                logger.info(f"Reintentando en {espera}s...")
                await asyncio.sleep(espera)
            else:
                logger.error(f"✗ Falló envío a {destinatario} después de {max_reintentos} intentos")
                raise EmailSendError(f"Error al enviar email después de {max_reintentos} intentos: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error inesperado al enviar email: {str(e)}", exc_info=True)
            raise EmailSendError(f"Error inesperado: {str(e)}")
    
    return False


def generar_email_recordatorio(
    numero_factura: str,
    cliente: str,
    monto: float,
    dias: int,
    html: bool = True
) -> tuple[str, str]:
    """
    Genera el asunto y cuerpo para un email de recordatorio
    
    Args:
        numero_factura: Número de la factura
        cliente: Nombre del cliente
        monto: Monto de la factura
        dias: Días hasta vencimiento (positivo) o desde vencimiento (negativo)
        html: Si True, genera HTML; si False, texto plano
        
    Returns:
        Tupla (asunto, cuerpo)
    """
    if dias > 0:
        asunto = f"Recordatorio: Factura {numero_factura} vence en {dias} días"
        urgencia = "recordatorio"
        mensaje_principal = f"vence en {dias} días"
        mensaje_secundario = "Por favor, proceda con el pago a la brevedad posible."
        color_urgencia = "#2196F3"  # Azul
    else:
        dias_vencida = abs(dias)
        asunto = f"URGENTE: Factura {numero_factura} vencida hace {dias_vencida} días"
        urgencia = "urgente"
        mensaje_principal = f"está vencida desde hace {dias_vencida} días"
        mensaje_secundario = "Por favor, regularice su situación a la brevedad."
        color_urgencia = "#F44336"  # Rojo
    
    if html:
        # Template HTML profesional
        template = Template("""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }
        .container {
            background-color: #ffffff;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            padding-bottom: 20px;
            border-bottom: 3px solid {{ color_urgencia }};
            margin-bottom: 30px;
        }
        .header h1 {
            color: {{ color_urgencia }};
            margin: 0;
            font-size: 24px;
        }
        .badge {
            display: inline-block;
            padding: 5px 15px;
            background-color: {{ color_urgencia }};
            color: white;
            border-radius: 20px;
            font-size: 12px;
            text-transform: uppercase;
            margin-top: 10px;
        }
        .content {
            margin: 20px 0;
        }
        .invoice-details {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .invoice-details table {
            width: 100%;
            border-collapse: collapse;
        }
        .invoice-details td {
            padding: 10px 0;
            border-bottom: 1px solid #dee2e6;
        }
        .invoice-details td:first-child {
            font-weight: bold;
            color: #666;
        }
        .invoice-details td:last-child {
            text-align: right;
        }
        .amount {
            font-size: 28px;
            font-weight: bold;
            color: {{ color_urgencia }};
        }
        .footer {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #dee2e6;
            text-align: center;
            color: #666;
            font-size: 14px;
        }
        .cta {
            text-align: center;
            margin: 30px 0;
        }
        .cta-button {
            display: inline-block;
            padding: 12px 30px;
            background-color: {{ color_urgencia }};
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ app_name }}</h1>
            <span class="badge">{{ urgencia }}</span>
        </div>
        
        <div class="content">
            <p>Estimado/a <strong>{{ cliente }}</strong>,</p>
            
            <p>Le {{ 'recordamos' if dias > 0 else 'informamos' }} que la factura <strong>{{ numero_factura }}</strong> {{ mensaje_principal }}.</p>
            
            <div class="invoice-details">
                <table>
                    <tr>
                        <td>Factura N°:</td>
                        <td><strong>{{ numero_factura }}</strong></td>
                    </tr>
                    <tr>
                        <td>Monto:</td>
                        <td><span class="amount">${{ "%.2f"|format(monto) }}</span></td>
                    </tr>
                    <tr>
                        <td>Estado:</td>
                        <td><strong>{{ mensaje_principal }}</strong></td>
                    </tr>
                </table>
            </div>
            
            <p>{{ mensaje_secundario }}</p>
            
            <div class="cta">
                <a href="#" class="cta-button">Ver Detalles</a>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>Equipo de Facturación - {{ app_name }}</strong></p>
            <p style="font-size: 12px; color: #999;">
                Este es un correo automático, por favor no responda a este mensaje.
            </p>
        </div>
    </div>
</body>
</html>
        """)
        
        cuerpo = template.render(
            numero_factura=numero_factura,
            cliente=cliente,
            monto=monto,
            dias=dias,
            urgencia=urgencia.upper(),
            mensaje_principal=mensaje_principal,
            mensaje_secundario=mensaje_secundario,
            color_urgencia=color_urgencia,
            app_name=settings.app_name
        )
    else:
        # Texto plano
        cuerpo = f"""
Estimado/a {cliente},

Le {'recordamos' if dias > 0 else 'informamos'} que la factura {numero_factura} por un monto de ${monto:,.2f} {mensaje_principal}.

{mensaje_secundario}

Detalles de la factura:
- Número: {numero_factura}
- Monto: ${monto:,.2f}
- Estado: {mensaje_principal}

Saludos cordiales,
Equipo de Facturación - {settings.app_name}

---
Este es un correo automático, por favor no responda a este mensaje.
        """
    
    return asunto, cuerpo
