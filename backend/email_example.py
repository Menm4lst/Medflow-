"""
Ejemplo de uso del servicio de email mejorado
"""
import asyncio
from email_service import (
    enviar_email,
    generar_email_recordatorio,
    EmailValidationError,
    EmailSendError
)


async def ejemplo_basico():
    """Ejemplo de envío básico de email"""
    print("1. Envío básico de email...")
    
    try:
        resultado = await enviar_email(
            destinatario="cliente@ejemplo.com",
            asunto="Prueba de Email",
            cuerpo="Este es un mensaje de prueba.",
            modo_prueba=True  # Cambiar a False para enviar realmente
        )
        print(f"   ✓ Resultado: {resultado}")
    except EmailValidationError as e:
        print(f"   ✗ Error de validación: {e}")
    except EmailSendError as e:
        print(f"   ✗ Error de envío: {e}")


async def ejemplo_html():
    """Ejemplo de email con HTML"""
    print("\n2. Email con HTML personalizado...")
    
    html = """
    <html>
        <body>
            <h1>¡Hola!</h1>
            <p>Este es un <strong>email con HTML</strong>.</p>
        </body>
    </html>
    """
    
    try:
        resultado = await enviar_email(
            destinatario="cliente@ejemplo.com",
            asunto="Email con HTML",
            cuerpo=html,
            es_html=True,
            modo_prueba=True
        )
        print(f"   ✓ Resultado: {resultado}")
    except Exception as e:
        print(f"   ✗ Error: {e}")


async def ejemplo_con_adjuntos():
    """Ejemplo de email con adjuntos PDF"""
    print("\n3. Email con adjuntos...")
    
    # Simular contenido de un PDF
    contenido_pdf = b"%PDF-1.4 contenido simulado..."
    
    try:
        resultado = await enviar_email(
            destinatario="cliente@ejemplo.com",
            asunto="Factura Adjunta",
            cuerpo="Adjunto encontrará su factura.",
            adjuntos=[
                ("factura_001.pdf", contenido_pdf),
            ],
            modo_prueba=True
        )
        print(f"   ✓ Resultado: {resultado}")
    except Exception as e:
        print(f"   ✗ Error: {e}")


async def ejemplo_recordatorio():
    """Ejemplo de email de recordatorio con template"""
    print("\n4. Email de recordatorio (próximo a vencer)...")
    
    asunto, cuerpo = generar_email_recordatorio(
        numero_factura="FAC-2025-001",
        cliente="Juan Pérez",
        monto=15000.50,
        dias=5,  # Vence en 5 días
        html=True
    )
    
    try:
        resultado = await enviar_email(
            destinatario="cliente@ejemplo.com",
            asunto=asunto,
            cuerpo=cuerpo,
            es_html=True,
            modo_prueba=True
        )
        print(f"   ✓ Asunto: {asunto}")
        print(f"   ✓ Resultado: {resultado}")
    except Exception as e:
        print(f"   ✗ Error: {e}")


async def ejemplo_factura_vencida():
    """Ejemplo de email de factura vencida"""
    print("\n5. Email de factura vencida (urgente)...")
    
    asunto, cuerpo = generar_email_recordatorio(
        numero_factura="FAC-2024-999",
        cliente="María González",
        monto=28750.00,
        dias=-10,  # Vencida hace 10 días
        html=True
    )
    
    try:
        resultado = await enviar_email(
            destinatario="cliente@ejemplo.com",
            asunto=asunto,
            cuerpo=cuerpo,
            es_html=True,
            modo_prueba=True
        )
        print(f"   ✓ Asunto: {asunto}")
        print(f"   ✓ Resultado: {resultado}")
    except Exception as e:
        print(f"   ✗ Error: {e}")


async def ejemplo_validacion_email():
    """Ejemplo de validación de emails"""
    print("\n6. Validación de emails...")
    
    emails_prueba = [
        "valido@ejemplo.com",
        "invalido@",
        "sin-arroba.com",
        "otro.valido@dominio.co.ar"
    ]
    
    for email in emails_prueba:
        try:
            resultado = await enviar_email(
                destinatario=email,
                asunto="Prueba",
                cuerpo="Contenido",
                modo_prueba=True
            )
            print(f"   ✓ {email}: válido")
        except EmailValidationError:
            print(f"   ✗ {email}: inválido")


async def ejemplo_envio_masivo():
    """Ejemplo de envío masivo con rate limiting"""
    print("\n7. Envío masivo (rate limiting activo)...")
    
    destinatarios = [f"cliente{i}@ejemplo.com" for i in range(5)]
    
    for i, destinatario in enumerate(destinatarios, 1):
        try:
            print(f"   Enviando {i}/{len(destinatarios)}...")
            await enviar_email(
                destinatario=destinatario,
                asunto=f"Email masivo #{i}",
                cuerpo="Contenido del email",
                modo_prueba=True
            )
        except Exception as e:
            print(f"   ✗ Error con {destinatario}: {e}")


async def main():
    """Ejecutar todos los ejemplos"""
    print("=" * 60)
    print("EJEMPLOS DE USO - SERVICIO DE EMAIL MEJORADO")
    print("=" * 60)
    
    await ejemplo_basico()
    await ejemplo_html()
    await ejemplo_con_adjuntos()
    await ejemplo_recordatorio()
    await ejemplo_factura_vencida()
    await ejemplo_validacion_email()
    await ejemplo_envio_masivo()
    
    print("\n" + "=" * 60)
    print("EJEMPLOS COMPLETADOS")
    print("=" * 60)
    print("\nNota: Todos los ejemplos usan modo_prueba=True")
    print("Para enviar emails reales, cambia modo_prueba=False")
    print("y configura las credenciales SMTP en .env")


if __name__ == "__main__":
    asyncio.run(main())
