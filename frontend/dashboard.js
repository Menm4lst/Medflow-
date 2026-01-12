const API_URL = 'http://localhost:8000/api';

// Verificar sesión
function verificarSesion() {
    const sesionActiva = localStorage.getItem('sesionActiva');
    const nombreUsuario = localStorage.getItem('nombreUsuario');
    
    if (sesionActiva !== 'true') {
        window.location.href = 'index.html';
        return false;
    }
    
    // Actualizar nombre de usuario
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

// Cargar datos al iniciar
document.addEventListener('DOMContentLoaded', () => {
    if (verificarSesion()) {
        cargarEstadisticas();
        cargarAlertasRecientes();
    }
});

async function cargarEstadisticas() {
    try {
        const response = await fetch(`${API_URL}/dashboard/stats`);
        if (!response.ok) throw new Error('Error al cargar estadísticas');
        
        const stats = await response.json();
        
        document.getElementById('totalFacturas').textContent = stats.total_facturas;
        document.getElementById('pendientes').textContent = stats.facturas_pendientes;
        document.getElementById('vencidas').textContent = stats.facturas_vencidas;
        document.getElementById('pagadas').textContent = stats.facturas_pagadas;
        document.getElementById('montoPendiente').textContent = `$${formatearMonto(stats.monto_total_pendiente)}`;
        document.getElementById('montoVencido').textContent = `$${formatearMonto(stats.monto_total_vencido)}`;
    } catch (error) {
        console.error('Error:', error);
    }
}

async function cargarAlertasRecientes() {
    try {
        const response = await fetch(`${API_URL}/alertas/`);
        const alertas = await response.json();
        
        const alertsList = document.getElementById('alertsList');
        
        if (alertas.length === 0) {
            alertsList.innerHTML = '<div class="empty-state">✅ No hay alertas pendientes</div>';
            return;
        }
        
        // Mostrar solo las primeras 3 alertas
        const alertasRecientes = alertas.slice(0, 3);
        
        alertsList.innerHTML = alertasRecientes.map(alerta => `
            <div class="alert-item ${alerta.tipo === 'vencida' ? 'danger' : 'warning'}">
                <span class="alert-icon">${alerta.tipo === 'vencida' ? '🚨' : '⏰'}</span>
                <div class="alert-content">
                    <div class="alert-text">${alerta.mensaje}</div>
                    <div class="alert-time">Factura: ${alerta.numero_factura} | ${alerta.cliente}</div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error:', error);
    }
}

function formatearMonto(monto) {
    return new Intl.NumberFormat('es-AR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(monto);
}
