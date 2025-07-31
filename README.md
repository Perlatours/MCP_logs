# 🚀 SmartPerlahub MCP - Sistema de Análisis de Auditoría

> **Análisis completo de logs de auditoría de PerlAhub con 87,425 registros procesados**  
> **Integración directa con Claude Desktop mediante protocolo MCP**

![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Database](https://img.shields.io/badge/Database-87k%20records-orange)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

---

## 🎯 **Descripción**

**SmartPerlahub MCP** es un sistema completo de análisis de logs de auditoría que permite:
- ✅ Análisis en **lenguaje natural** de 87,425 registros de auditoría
- ✅ Integración directa con **Claude Desktop**
- ✅ Identificación automática de **problemas críticos**
- ✅ Consultas SQL sin programación
- ✅ **2 problemas críticos ya identificados** con soluciones específicas

---

## 🚨 **Problemas Críticos Identificados**

### 1. **Hotel 22 - "Hotel Fantasma"** 
- **🔴 CRÍTICO**: 72,787 exclusiones de hotel **inexistente**
- **Causa**: Configuración obsoleta en sistema de proveedores
- **Impacto**: 99.7% de todas las restricciones
- **✅ Solución SQL incluida**

### 2. **Hotel 5481 - Guitart Central Park Aqua Resort**
- **🟠 URGENTE**: 4,374 errores de mapeo "DBL|2P·CLASSIC" 
- **Causa**: Mapeo de habitación faltante
- **Impacto**: 99.8% de todas las excepciones
- **✅ Solución específica incluida**

### 3. **Performance Issues**
- **🟡 MONITOR**: Búsquedas de hasta 24.9 segundos
- **Causa**: Posible stress testing en producción
- **✅ Plan de optimización incluido**

---

## ⚡ **Instalación Rápida**

### **Opción 1: Instalación Automática (Recomendada)**

```bash
# 1. Descargar repositorio
git clone https://github.com/TU_USUARIO/SmartPerlahub-MCP.git
cd SmartPerlahub-MCP

# 2. Ejecutar instalador automático
chmod +x INSTALL.sh
./INSTALL.sh

# 3. Reiniciar Claude Desktop

# 4. Probar
# En Claude Desktop: "Muestra el resumen del sistema"
```

### **Opción 2: Solo descarga directa**

1. **Descargar archivo completo**: `SmartPerlahub_MCP_Package_[timestamp].tar.gz`
2. **Extraer**: `tar -xzf SmartPerlahub_MCP_Package_*.tar.gz`
3. **Ejecutar**: `./INSTALL.sh` (Unix) o `INSTALL.bat` (Windows)

---

## 📊 **Datos del Sistema**

| Métrica | Valor |
|---------|-------|
| **Total Registros** | 87,425 |
| **Restricciones** | 72,787 (99.7% Hotel 22 fantasma) |
| **Excepciones** | 4,382 (99.8% Hotel 5481 room mapping) |
| **Búsquedas Cliente** | 5,000 (performance analizada) |
| **Búsquedas Proveedor** | 1,128 |
| **Búsquedas Conector** | 3,000 |
| **Eventos Login** | 1,128 |
| **Tamaño BD** | 210MB |
| **Fecha Logs** | 31 Julio 2025 |

---

## 🛠️ **Herramientas Disponibles en Claude Desktop**

| Comando Natural | Descripción |
|----------------|-------------|
| `"Muestra el resumen del sistema"` | 📊 Estadísticas generales del sistema |
| `"Analiza las restricciones de hoteles"` | 🚫 Patrones de exclusión y restricciones |
| `"Analiza las excepciones del sistema"` | ⚡ Errores más comunes y frecuentes |
| `"Analiza el hotel 22"` | 🚨 Investigación del hotel fantasma |
| `"Analiza el hotel 5481"` | 🏨 Problema de room mapping específico |
| `"Muestra los problemas críticos"` | 🎯 Issues principales con soluciones |
| `"Ejecuta: SELECT COUNT(*) FROM restrictions"` | 💻 Consultas SQL personalizadas |

---

## 📋 **Requisitos del Sistema**

- **Python 3.8+** (verificar: `python3 --version`)
- **Claude Desktop** instalado y funcionando
- **Sistema Operativo**: macOS, Linux, o Windows
- **Espacio**: ~250MB libres

---

## 🔧 **Configuración Manual (si instalador automático falla)**

### **macOS:**
```bash
# 1. Copiar archivos
mkdir ~/SmartPerlahub_MCP
cp smartperlahub.db smartperlahub_mcp_fixed.py ~/SmartPerlahub_MCP/

# 2. Configurar Claude Desktop
# Editar: ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "smartperlahub": {
      "command": "python3",
      "args": ["/Users/TU_USUARIO/SmartPerlahub_MCP/smartperlahub_mcp_fixed.py"],
      "env": {
        "DB_PATH": "/Users/TU_USUARIO/SmartPerlahub_MCP/smartperlahub.db"
      }
    }
  }
}
```

### **Linux:**
```bash
# 1. Copiar archivos
mkdir ~/SmartPerlahub_MCP
cp smartperlahub.db smartperlahub_mcp_fixed.py ~/SmartPerlahub_MCP/

# 2. Configurar Claude Desktop
# Editar: ~/.config/Claude/claude_desktop_config.json
# (Mismo contenido que macOS con rutas de Linux)
```

### **Windows:**
```cmd
REM 1. Copiar archivos a %USERPROFILE%\SmartPerlahub_MCP\
REM 2. Configurar Claude Desktop con rutas de Windows
```

---

## 🧪 **Comandos de Prueba**

Una vez instalado, prueba estos comandos en Claude Desktop:

```
"Muestra el resumen del sistema"
```
**Resultado esperado**: Debe mostrar 87,425 registros totales

```
"Analiza el hotel 22"
```
**Resultado esperado**: Debe mostrar "HOTEL FANTASMA DETECTADO"

```
"Muestra los problemas críticos"
```
**Resultado esperado**: Lista de 3 problemas con soluciones SQL

---

## 📁 **Estructura del Repositorio**

```
SmartPerlahub-MCP/
├── smartperlahub.db                    # Base de datos principal (210MB)
├── smartperlahub_mcp_fixed.py         # Servidor MCP
├── INSTALL.sh                          # Instalador Unix/macOS
├── INSTALL.bat                         # Instalador Windows  
├── README.md                           # Este archivo
├── README_SMARTPERLAHUB_MCP.md        # Manual técnico completo
├── REPORTE_FINAL_CRITICO.md           # Análisis ejecutivo
├── smartperlahub_report.json          # Estadísticas en JSON
└── SmartPerlahub_MCP_Package_*.tar.gz # Paquete completo
```

---

## 🚨 **Soluciones SQL para Problemas Críticos**

### **Hotel 22 - Limpiar configuración:**
```sql
-- EJECUTAR EN BASE DE DATOS DE PRODUCCIÓN
UPDATE partners."ProviderConnections" 
SET "ExcludeHotelIds" = REPLACE(REPLACE(REPLACE(
    "ExcludeHotelIds", '22,', ''), ',22', ''), '22', '')
WHERE "ExcludeHotelIds" LIKE '%22%';
```

### **Hotel 5481 - Crear mapeo faltante:**
```sql
-- 1. Buscar room type correcto:
SELECT * FROM inventory."RoomTypes" 
WHERE "Name" ILIKE '%doble%' OR "Code" ILIKE '%dbl%';

-- 2. Crear mapeo (usar ID correcto del paso 1):
INSERT INTO mapping."RoomMappings" 
("IntegrationSystemId", "ExternalId", "RoomTypeId", "RoomAmenityIds")
VALUES (1, 'DBL|2P·CLASSIC', '[ID_ROOM_TYPE_DOBLE]', '');
```

---

## 📈 **Performance Identificado**

### **Estadísticas de Búsquedas:**
- **Promedio**: 135ms
- **Máximo**: 24,953ms (24.9 segundos!) 
- **Mínimo**: 0ms
- **Pico de actividad**: 243 búsquedas/minuto

### **Recomendaciones:**
1. Implementar timeout en búsquedas > 10 segundos
2. Optimizar queries de proveedores
3. Crear ambiente separado para stress testing

---

## 🔍 **Análisis Disponibles**

### **Por Hotel:**
- Restricciones por hotel específico
- Excepciones relacionadas
- Análisis de conectividad

### **Por Tipo:**
- Patrones de restricciones
- Frecuencia de excepciones  
- Performance de búsquedas

### **Temporal:**
- Actividad por día/hora
- Picos de tráfico
- Tendencias de errores

---

## 🆘 **Troubleshooting**

### **Error: "MCP server not found"**
- Verificar que Python 3.8+ está instalado
- Verificar rutas en configuración Claude Desktop
- Reiniciar Claude Desktop completamente

### **Error: "Database not found"**
- Verificar que `smartperlahub.db` existe (~210MB)
- Verificar variable `DB_PATH` en configuración
- Verificar permisos de lectura del archivo

### **Error: "No data returned"**
- Ejecutar: `"Muestra el resumen del sistema"`
- Verificar que muestra 87,425 registros
- Si no, revisar integridad de base de datos

---

## 📞 **Soporte**

- **Documentación técnica**: `README_SMARTPERLAHUB_MCP.md`
- **Análisis ejecutivo**: `REPORTE_FINAL_CRITICO.md`
- **Estadísticas**: `smartperlahub_report.json`

---

## 📊 **Métricas de Verificación**

Para confirmar que la instalación fue exitosa:

1. **Claude Desktop** no debe mostrar errores JSON ✅
2. **Comando "resumen"** debe mostrar 87,425 registros ✅  
3. **Hotel 22** debe aparecer como "hotel fantasma" ✅
4. **Hotel 5481** debe mostrar errores de room mapping ✅

---

## ⚡ **Quick Start**

```bash
# Descarga rápida e instalación en 3 comandos:
git clone https://github.com/TU_USUARIO/SmartPerlahub-MCP.git
cd SmartPerlahub-MCP && chmod +x INSTALL.sh && ./INSTALL.sh
# Reiniciar Claude Desktop y probar: "Muestra el resumen del sistema"
```

---

## 🎯 **Resultado Final**

Una vez instalado, tendrás acceso directo en Claude Desktop a análisis completo de:
- ✅ **87,425 registros** de auditoría de PerlAhub
- ✅ **Problemas críticos** identificados con soluciones
- ✅ **Consultas en lenguaje natural** sin programación
- ✅ **Análisis de performance** y optimización
- ✅ **Herramientas de investigación** de hoteles específicos

**¡SmartPerlahub MCP: Tu auditoría de PerlAhub al alcance de una conversación!** 🚀