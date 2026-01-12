# GUÍA RÁPIDA DE USO

## 🚀 Inicio Rápido

### 1. Primera vez
```bash
.\start.bat
```
El script automáticamente:
- ✅ Crea el entorno virtual
- ✅ Instala dependencias
- ✅ Inicia backend y frontend
- ✅ Abre el navegador

### 2. Configurar Email (IMPORTANTE)
Editar `backend\.env`:
```env
SMTP_USER=tu_email@outlook.com
SMTP_PASSWORD=tu_password
SMTP_FROM=tu_email@outlook.com
```

### 3. Usar el Sistema

#### Crear Cliente
1. Click "➕ Nuevo Cliente"
2. Completar nombre y email (obligatorio)
3. Guardar

#### Crear Factura
1. Click "📄 Nueva Factura"
2. Número de factura único
3. Seleccionar cliente
4. Monto y fecha de vencimiento
5. Crear

#### Enviar Recordatorio
- **Rápido**: Click "📧 Enviar Recordatorio" en alertas
- **Personalizado**: Click 📧 en la tabla de facturas

#### Marcar como Pagada
- Click ✓ en la factura correspondiente

## 📊 Dashboard

El sistema muestra automáticamente:
- Total de facturas
- Facturas pendientes, vencidas y pagadas
- Montos pendientes y vencidos
- Alertas de vencimientos

## 🔔 Alertas Automáticas

- ⚠️ **5 días antes**: Factura próxima a vencer
- 🔴 **Vencida**: Actualización automática del estado

## 📧 Sistema de Emails

### Para Outlook/Hotmail:
- Host: `smtp.office365.com`
- Puerto: `587`
- Usar tu email y contraseña normal

### Para Gmail:
- Host: `smtp.gmail.com`
- Puerto: `587`
- Requiere "Contraseña de Aplicación" (no tu contraseña normal)

**Generar App Password en Gmail:**
1. Ir a cuenta.google.com
2. Seguridad → Verificación en 2 pasos (activar)
3. Contraseñas de aplicación
4. Generar nueva contraseña
5. Copiar en `.env`

## 🗂️ Estados de Factura

| Estado | Descripción | Color |
|--------|-------------|-------|
| Pendiente | Recién creada | Azul |
| En seguimiento | Con emails enviados | Naranja |
| Pagada | Cobrada | Verde |
| Vencida | Pasó fecha vencimiento | Rojo |

## ⌨️ Atajos Útiles

- `Ctrl + R` - Recargar datos
- Click en número de factura - Ver detalles
- Click en emails - Ver historial

## 🔧 Comandos Manuales

### Iniciar Backend
```bash
cd backend
venv\Scripts\activate
python main.py
```

### Iniciar Frontend
```bash
cd frontend
python -m http.server 3000
```

## 📱 URLs Importantes

- Frontend: http://localhost:3000
- API Backend: http://localhost:8000
- Documentación API: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🐛 Problemas Comunes

### No funciona el email
1. Verificar `.env` con credenciales correctas
2. Para Gmail: usar App Password
3. Para Outlook: verificar que SMTP esté habilitado

### Error "puerto ocupado"
- Backend (8000): Cerrar otras apps en ese puerto
- Frontend (3000): Usar otro puerto: `python -m http.server 3001`

### Base de datos corrupta
1. Cerrar el backend
2. Eliminar `backend\facturas.db`
3. Reiniciar (se crea automáticamente)

## 💡 Tips

1. **Backup regular**: Copia `backend\facturas.db`
2. **Prueba emails**: Envía un test a ti mismo primero
3. **Filtros**: Usa el selector de estados para ver grupos
4. **Historial**: Revisa la columna "Emails enviados"

## 📞 Necesitas Ayuda?

1. Lee el README.md completo
2. Revisa los logs del backend
3. Consulta http://localhost:8000/docs

---

**¡Listo para facturar! 💰**
