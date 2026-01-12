const API_URL = 'http://localhost:8000/api';

// Credenciales válidas
const VALID_CREDENTIALS = {
    username: 'admin',
    password: 'admin123'
};

// ============= AUTENTICACIÓN =============
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const toggleBtn = document.querySelector('.toggle-password');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleBtn.textContent = '👁️‍🗨️';
    } else {
        passwordInput.type = 'password';
        toggleBtn.textContent = '👁️';
    }
}

function cerrarSesion() {
    if (confirm('¿Estás seguro que deseas cerrar sesión?')) {
        localStorage.removeItem('sesionActiva');
        localStorage.removeItem('nombreUsuario');
        window.location.href = 'index.html';
    }
}

// ============= INICIALIZACIÓN =============
document.addEventListener('DOMContentLoaded', () => {
    // Configurar formulario de login si existe
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const errorDiv = document.getElementById('loginError');
            
            // Validar credenciales
            if (username === VALID_CREDENTIALS.username && password === VALID_CREDENTIALS.password) {
                // Login exitoso
                localStorage.setItem('sesionActiva', 'true');
                localStorage.setItem('nombreUsuario', username);
                
                // Redirigir al dashboard
                window.location.href = 'dashboard.html';
            } else {
                // Mostrar error
                errorDiv.style.display = 'block';
                document.getElementById('password').value = '';
                
                // Ocultar error después de 3 segundos
                setTimeout(() => {
                    errorDiv.style.display = 'none';
                }, 3000);
            }
        });
    }
});
