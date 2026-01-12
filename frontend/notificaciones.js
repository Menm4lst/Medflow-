const API_URL = 'http://localhost:8000/api';

let todasNotificaciones = [];
let filtroActual = 'all';

// Verificar sesión
function verificarSesion() {
    const sesionActiva = localStorage.getItem('sesionActiva');
    const nombreUsuario = localStorage.getItem('nombreUsuario');
    
    if (sesionActiva !== 'true') {
        window.location.href = 'index.html';
        return false;
    }
    
    const userNameElement = document.getElementById('userName');
    if (userNameElement && nombreUsuario) {
        userNameElement.textContent = nombreUsuario;
    }
    
    return true;
}

function cerrarSesion() {
    if (confirm('¿Estás seguro que deseas cerrar sesión?')) {
        localStorage.removeItem('sesionActiva');
        localStorage.removeItem('nombreUsuario');
        window.location.href = 'index.html';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (verificarSesion()) {
        cargarNotificaciones();
    }
});

async function cargarNotificaciones() {
    try {
        const response = await fetch(`${API_URL}/alertas/`);
        const alertas = await response.json();
        
        // Obtener notificaciones leídas del localStorage
        const leidas = JSON.parse(localStorage.getItem('notificacionesLeidas') || '[]');
        
        // Transformar alertas a notificaciones
        todasNotificaciones = alertas.map((alerta, index) => ({
            id: alerta.factura_id || index,
            tipo: alerta.tipo === 'vencida' ? 'urgent' : 'warning',
            titulo: alerta.mensaje,
            descripcion: `Factura: ${alerta.numero_factura} | Cliente: ${alerta.cliente} | Monto: $${formatearMonto(alerta.monto)}`,
            fecha: new Date().toISOString(),
            leida: leidas.includes(alerta.factura_id),
            facturaId: alerta.factura_id,
            numeroFactura: alerta.numero_factura
        }));
        
        // Agregar notificaciones de sistema
        agregarNotificacionesSistema();
        
        actualizarContadores();
        mostrarNotificaciones();
    } catch (error) {
        console.error('Error:', error);
    }
}

function agregarNotificacionesSistema() {
    const notificacionesSistema = [
        {
            id: 'sys-1',
            tipo: 'info',
            titulo: '✅ Sistema actualizado',
            descripcion: 'El sistema de gestión ha sido actualizado a la versión 2.0',
            fecha: new Date(Date.now() - 3600000).toISOString(),
            leida: false
        },
        {
            id: 'sys-2',
            tipo: 'info',
            titulo: '📧 Servicio de email mejorado',
            descripcion: 'Ahora puedes enviar recordatorios con templates HTML profesionales',
            fecha: new Date(Date.now() - 7200000).toISOString(),
            leida: false
        }
    ];
    
    todasNotificaciones = [...todasNotificaciones, ...notificacionesSistema];
}

function mostrarNotificaciones() {
    const container = document.getElementById('notificationsList');
    
    let notificacionesFiltradas = todasNotificaciones;
    
    if (filtroActual === 'urgent') {
        notificacionesFiltradas = todasNotificaciones.filter(n => n.tipo === 'urgent');
    } else if (filtroActual === 'warning') {
        notificacionesFiltradas = todasNotificaciones.filter(n => n.tipo === 'warning');
    } else if (filtroActual === 'info') {
        notificacionesFiltradas = todasNotificaciones.filter(n => n.tipo === 'info');
    } else if (filtroActual === 'read') {
        notificacionesFiltradas = todasNotificaciones.filter(n => n.leida);
    }
    
    if (notificacionesFiltradas.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📭</div>
                <h3>No hay notificaciones</h3>
                <p>No tienes notificaciones en esta categoría</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = notificacionesFiltradas.map(notif => `
        <div class="notification-card ${notif.tipo} ${notif.leida ? 'read' : 'unread'}" data-id="${notif.id}">
            <div class="notification-header">
                <div class="notification-badge ${notif.tipo}">
                    ${notif.tipo === 'urgent' ? '🚨 Urgente' : notif.tipo === 'warning' ? '⏰ Próxima' : 'ℹ️ Info'}
                </div>
                <div class="notification-time">${formatearTiempo(notif.fecha)}</div>
            </div>
            <div class="notification-body">
                <h3 class="notification-title">${notif.titulo}</h3>
                <p class="notification-desc">${notif.descripcion}</p>
            </div>
            <div class="notification-actions">
                ${!notif.leida ? `
                    <button class="btn-small btn-primary" onclick="marcarLeida('${notif.id}')">
                        ✓ Marcar como leída
                    </button>
                ` : ''}
                ${notif.facturaId ? `
                    <button class="btn-small btn-outline" onclick="enviarRecordatorio(${notif.facturaId})">
                        📧 Enviar Recordatorio
                    </button>
                ` : ''}
                <button class="btn-small btn-text" onclick="eliminarNotificacion('${notif.id}')">
                    🗑️ Eliminar
                </button>
            </div>
        </div>
    `).join('');
}

function actualizarContadores() {
    const all = todasNotificaciones.length;
    const urgent = todasNotificaciones.filter(n => n.tipo === 'urgent').length;
    const warning = todasNotificaciones.filter(n => n.tipo === 'warning').length;
    const info = todasNotificaciones.filter(n => n.tipo === 'info').length;
    const read = todasNotificaciones.filter(n => n.leida).length;
    
    document.getElementById('countAll').textContent = all;
    document.getElementById('countUrgent').textContent = urgent;
    document.getElementById('countWarning').textContent = warning;
    document.getElementById('countInfo').textContent = info;
    document.getElementById('countRead').textContent = read;
}

function filtrarNotificaciones(filtro) {
    filtroActual = filtro;
    
    // Actualizar botones activos
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-filter="${filtro}"]`).classList.add('active');
    
    mostrarNotificaciones();
}

function marcarLeida(id) {
    const notif = todasNotificaciones.find(n => n.id === id);
    if (notif) {
        notif.leida = true;
        
        // Guardar en localStorage
        const leidas = JSON.parse(localStorage.getItem('notificacionesLeidas') || '[]');
        if (notif.facturaId && !leidas.includes(notif.facturaId)) {
            leidas.push(notif.facturaId);
            localStorage.setItem('notificacionesLeidas', JSON.stringify(leidas));
        }
        
        actualizarContadores();
        mostrarNotificaciones();
    }
}

function marcarTodasLeidas() {
    todasNotificaciones.forEach(n => n.leida = true);
    
    // Guardar en localStorage
    const leidas = todasNotificaciones
        .filter(n => n.facturaId)
        .map(n => n.facturaId);
    localStorage.setItem('notificacionesLeidas', JSON.stringify(leidas));
    
    actualizarContadores();
    mostrarNotificaciones();
}

function eliminarNotificacion(id) {
    if (confirm('¿Eliminar esta notificación?')) {
        todasNotificaciones = todasNotificaciones.filter(n => n.id !== id);
        actualizarContadores();
        mostrarNotificaciones();
    }
}

async function enviarRecordatorio(facturaId) {
    try {
        const response = await fetch(`${API_URL}/emails/recordatorio/${facturaId}`, {
            method: 'POST'
        });
        
        if (response.ok) {
            alert('✅ Recordatorio enviado exitosamente');
            marcarLeida(String(facturaId));
        } else {
            alert('❌ Error al enviar el recordatorio');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('❌ Error al enviar el recordatorio');
    }
}

function formatearMonto(monto) {
    return new Intl.NumberFormat('es-AR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(monto);
}

function formatearTiempo(fecha) {
    const ahora = new Date();
    const fechaNotif = new Date(fecha);
    const diff = ahora - fechaNotif;
    
    const minutos = Math.floor(diff / 60000);
    const horas = Math.floor(diff / 3600000);
    const dias = Math.floor(diff / 86400000);
    
    if (minutos < 1) return 'Ahora';
    if (minutos < 60) return `Hace ${minutos} min`;
    if (horas < 24) return `Hace ${horas} h`;
    return `Hace ${dias} días`;
}
