@echo off
chcp 65001 > nul
echo ========================================
echo   💰 FACTURAFLOW
echo ========================================
echo.

echo [1/3] Verificando entorno virtual...
if not exist "backend\venv" (
    echo ⚠️  No se encontró entorno virtual. Creando...
    cd backend
    python -m venv venv
    echo ✅ Entorno virtual creado
    cd ..
) else (
    echo ✅ Entorno virtual encontrado
)

echo.
echo [2/3] Activando entorno virtual...
call backend\venv\Scripts\activate.bat
echo ✅ Entorno activado

echo.
echo [3/3] Verificando dependencias...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Instalando dependencias...
    cd backend
    pip install -r requirements.txt
    cd ..
    echo ✅ Dependencias instaladas
) else (
    echo ✅ Dependencias ya instaladas
)

echo.
echo ========================================
echo   🚀 INICIANDO SERVIDORES
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo Docs API: http://localhost:8000/docs
echo.
echo 💡 Presiona Ctrl+C para detener los servidores
echo.

:: Iniciar backend en una ventana nueva
start "Backend - FastAPI" cmd /k "cd backend && venv\Scripts\activate && python main.py"

:: Esperar 3 segundos
timeout /t 3 /nobreak >nul

:: Iniciar frontend en otra ventana
start "Frontend - HTTP Server" cmd /k "cd frontend && python -m http.server 3000"

:: Esperar 2 segundos
timeout /t 2 /nobreak >nul

:: Abrir navegador
start http://localhost:3000

echo.
echo ✅ Sistema iniciado correctamente
echo.
echo Ventanas abiertas:
echo   - Backend (FastAPI) - Puerto 8000
echo   - Frontend (HTTP) - Puerto 3000
echo   - Navegador web
echo.
echo Para detener: Cierra las ventanas de los servidores
echo.
pause
