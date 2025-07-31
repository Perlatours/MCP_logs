@echo off
echo.
echo 🚀 INSTALADOR SMARTPERLAHUB MCP PARA WINDOWS
echo ==========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no encontrado. Instala Python desde python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado

REM Crear directorio de instalación
set INSTALL_DIR=%USERPROFILE%\SmartPerlahub_MCP
mkdir "%INSTALL_DIR%" 2>nul

REM Copiar archivos
echo 📋 Copiando archivos...
copy smartperlahub.db "%INSTALL_DIR%\" >nul
copy smartperlahub_mcp_fixed.py "%INSTALL_DIR%\" >nul
copy *.md "%INSTALL_DIR%\" 2>nul

echo ✅ Archivos copiados a %INSTALL_DIR%

echo.
echo 🔧 CONFIGURACIÓN MANUAL REQUERIDA:
echo.
echo 1. Abrir Claude Desktop
echo 2. Configurar servidor MCP con ruta:
echo    %INSTALL_DIR%\smartperlahub_mcp_fixed.py
echo 3. Reiniciar Claude Desktop
echo 4. Probar con: "Muestra el resumen del sistema"
echo.

pause
