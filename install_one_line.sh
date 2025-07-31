#!/bin/bash

# 🚀 SMARTPERLAHUB MCP - INSTALADOR UNA LÍNEA
# Descarga, instala y configura todo automáticamente

echo "🚀 SMARTPERLAHUB MCP - INSTALACIÓN AUTOMÁTICA"
echo "=============================================="

# Verificar requisitos
echo "📋 Verificando requisitos..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no encontrado. Instalar desde: https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION encontrado"

# Verificar Claude Desktop
CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
if [ ! -d "$CLAUDE_CONFIG_DIR" ]; then
    echo "❌ Claude Desktop no encontrado. Instalar desde: https://claude.ai/download"
    exit 1
fi
echo "✅ Claude Desktop encontrado"

# Crear directorio temporal
TEMP_DIR=$(mktemp -d)
echo "📁 Directorio temporal: $TEMP_DIR"

# Descargar repositorio
echo "⬇️ Descargando SmartPerlahub MCP..."
cd "$TEMP_DIR"

# Intentar con curl primero (más común en macOS)
if command -v curl &> /dev/null; then
    curl -L -o MCP_logs.zip https://github.com/Perlatours/MCP_logs/archive/refs/heads/main.zip
    if [ $? -eq 0 ]; then
        echo "✅ Descarga exitosa con curl"
        unzip -q MCP_logs.zip
        cd MCP_logs-main
    else
        echo "❌ Error descargando con curl"
        exit 1
    fi
elif command -v wget &> /dev/null; then
    wget -O MCP_logs.zip https://github.com/Perlatours/MCP_logs/archive/refs/heads/main.zip
    unzip -q MCP_logs.zip
    cd MCP_logs-main
    echo "✅ Descarga exitosa con wget"
elif command -v git &> /dev/null; then
    git clone https://github.com/Perlatours/MCP_logs.git
    cd MCP_logs
    echo "✅ Descarga exitosa con git"
else
    echo "❌ No se encontró curl, wget o git para descargar"
    exit 1
fi

# Ejecutar instalador
echo "🛠️ Ejecutando instalador..."
chmod +x INSTALL.sh
./INSTALL.sh

# Verificar instalación
echo "🔍 Verificando instalación..."
if [ -f "$HOME/SmartPerlahub_MCP/smartperlahub.db" ]; then
    DB_SIZE=$(ls -lh "$HOME/SmartPerlahub_MCP/smartperlahub.db" | awk '{print $5}')
    echo "✅ Base de datos instalada: $DB_SIZE"
else
    echo "❌ Error: Base de datos no encontrada"
    exit 1
fi

if [ -f "$HOME/SmartPerlahub_MCP/smartperlahub_mcp_fixed.py" ]; then
    echo "✅ Servidor MCP instalado"
else
    echo "❌ Error: Servidor MCP no encontrado"
    exit 1
fi

if [ -f "$CLAUDE_CONFIG_DIR/claude_desktop_config.json" ]; then
    echo "✅ Claude Desktop configurado"
else
    echo "❌ Error: Configuración Claude Desktop no encontrada"
    exit 1
fi

# Limpiar archivos temporales
echo "🧹 Limpiando archivos temporales..."
rm -rf "$TEMP_DIR"

echo ""
echo "🎉 ¡INSTALACIÓN COMPLETA!"
echo "========================"
echo ""
echo "📋 SIGUIENTE PASO:"
echo "1. 🔄 Reiniciar Claude Desktop (Cmd + Q, luego reabrir)"
echo "2. ✅ Probar: 'Muestra el resumen del sistema'"
echo "3. 🎯 Debe mostrar: '87,425 registros totales'"
echo ""
echo "🛠️ Comandos de prueba:"
echo "- 'Analiza el hotel 22'"
echo "- 'Muestra los problemas críticos'"
echo "- 'Analiza las restricciones'"
echo ""
echo "📊 Sistema listo con 87,425 registros de auditoría"
echo "🚨 2 problemas críticos identificados con soluciones"
echo ""
echo "¡Disfruta SmartPerlahub MCP! 🚀"
