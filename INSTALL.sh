#!/bin/bash

echo "🚀 INSTALADOR AUTOMÁTICO SMARTPERLAHUB MCP"
echo "=========================================="
echo ""
echo "Este script instalará SmartPerlahub MCP en tu sistema."
echo ""

# Verificar sistema operativo
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Cygwin;;
    MINGW*)     MACHINE=MinGw;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo "🖥️  Sistema detectado: $MACHINE"

# Verificar Python
echo "🐍 Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION encontrado"
else
    echo "❌ Python 3 no encontrado. Por favor instala Python 3.8 o superior."
    echo "   macOS: brew install python"
    echo "   Ubuntu: sudo apt install python3"
    echo "   Windows: Descargar de python.org"
    exit 1
fi

# Verificar dependencias
echo "📦 Instalando dependencias..."
pip3 install --user psycopg2-binary 2>/dev/null || echo "⚠️  psycopg2-binary opcional (para PostgreSQL)"

# Obtener directorio de instalación
INSTALL_DIR="$HOME/SmartPerlahub_MCP"
echo ""
echo "📁 Directorio de instalación: $INSTALL_DIR"
echo ""

# Crear directorio de instalación
mkdir -p "$INSTALL_DIR"

# Copiar archivos
echo "📋 Copiando archivos del sistema..."
cp smartperlahub.db "$INSTALL_DIR/"
cp smartperlahub_mcp_fixed.py "$INSTALL_DIR/"
cp *.md "$INSTALL_DIR/" 2>/dev/null || true
cp *.json "$INSTALL_DIR/" 2>/dev/null || true

echo "✅ Archivos copiados a $INSTALL_DIR"

# Configurar Claude Desktop según el sistema operativo
if [ "$MACHINE" = "Mac" ]; then
    echo ""
    echo "🔧 Configurando Claude Desktop para macOS..."
    
    CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
    CLAUDE_CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"
    
    # Crear directorio si no existe
    mkdir -p "$CLAUDE_CONFIG_DIR"
    
    # Backup de configuración existente
    if [ -f "$CLAUDE_CONFIG_FILE" ]; then
        cp "$CLAUDE_CONFIG_FILE" "$CLAUDE_CONFIG_FILE.backup.smartperlahub.$(date +%Y%m%d_%H%M%S)"
        echo "✅ Backup de configuración existente creado"
    fi
    
    # Crear nueva configuración
    cat > "$CLAUDE_CONFIG_FILE" << EOFCONFIG
{
  "mcpServers": {
    "smartperlahub": {
      "command": "python3",
      "args": ["$INSTALL_DIR/smartperlahub_mcp_fixed.py"],
      "env": {
        "DB_PATH": "$INSTALL_DIR/smartperlahub.db"
      }
    }
  }
}
EOFCONFIG
    
    echo "✅ Claude Desktop configurado"
    echo ""
    echo "🔄 PASOS FINALES:"
    echo "1. Reinicia Claude Desktop completamente"
    echo "2. Prueba con: 'Muestra el resumen del sistema'"
    
elif [ "$MACHINE" = "Linux" ]; then
    echo ""
    echo "🐧 Sistema Linux detectado"
    echo "📋 Configuración manual requerida para Claude Desktop:"
    echo ""
    echo "Archivo de config: ~/.config/Claude/claude_desktop_config.json"
    echo "Contenido:"
    echo '{'
    echo '  "mcpServers": {'
    echo '    "smartperlahub": {'
    echo '      "command": "python3",'
    echo "      \"args\": [\"$INSTALL_DIR/smartperlahub_mcp_fixed.py\"],"
    echo '      "env": {'
    echo "        \"DB_PATH\": \"$INSTALL_DIR/smartperlahub.db\""
    echo '      }'
    echo '    }'
    echo '  }'
    echo '}'
    
else
    echo ""
    echo "🖥️  Sistema $MACHINE - Configuración manual requerida"
    echo "📋 Consulta la documentación para tu sistema operativo"
fi

echo ""
echo "📊 RESUMEN DE INSTALACIÓN:"
echo "========================="
echo "• Base de datos: $INSTALL_DIR/smartperlahub.db ($(du -h "$INSTALL_DIR/smartperlahub.db" 2>/dev/null | cut -f1 || echo "~200MB"))"
echo "• Servidor MCP: $INSTALL_DIR/smartperlahub_mcp_fixed.py"
echo "• Documentación: $INSTALL_DIR/*.md"
echo "• Total registros: 87,425 (restricciones, excepciones, búsquedas, logins)"
echo ""
echo "🧪 COMANDOS DE PRUEBA EN CLAUDE DESKTOP:"
echo "• 'Muestra el resumen del sistema'"
echo "• 'Analiza el hotel 22'"
echo "• 'Muestra los problemas críticos'"
echo "• 'Analiza las restricciones de hoteles'"
echo ""
echo "✅ ¡INSTALACIÓN COMPLETADA!"
echo "🎯 SmartPerlahub MCP listo para analizar logs de auditoría"
