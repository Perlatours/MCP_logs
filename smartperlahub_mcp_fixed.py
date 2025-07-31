#!/usr/bin/env python3
"""
SmartPerlahub MCP Server - Versión corregida con esquemas MCP válidos
"""

import asyncio
import json
import sqlite3
import sys
import os
from typing import Any, Dict, List, Optional

class SmartPerlahubMCP:
    def __init__(self):
        self.db_path = os.getenv('DB_PATH', 'smartperlahub.db')
        
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database not found: {self.db_path}")
        
        self.server_info = {
            "name": "smartperlahub",
            "version": "1.0.0"
        }
        
        # Herramientas con esquemas MCP válidos
        self.tools = [
            {
                "name": "analizar_restricciones",
                "description": "Analizar restricciones de hoteles y patrones de exclusión",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "hotel_id": {
                            "type": "number",
                            "description": "ID específico del hotel"
                        },
                        "tipo": {
                            "type": "string", 
                            "description": "Tipo de restricción"
                        },
                        "limite": {
                            "type": "number",
                            "description": "Límite de resultados",
                            "default": 50
                        }
                    }
                }
            },
            {
                "name": "analizar_excepciones",
                "description": "Analizar excepciones del sistema",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "tipo": {
                            "type": "string",
                            "description": "Tipo de excepción"
                        },
                        "limite": {
                            "type": "number", 
                            "description": "Límite de resultados",
                            "default": 30
                        }
                    }
                }
            },
            {
                "name": "resumen_sistema",
                "description": "Resumen completo del sistema de auditoría",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "detallado": {
                            "type": "boolean",
                            "description": "Incluir detalles",
                            "default": True
                        }
                    }
                }
            },
            {
                "name": "analizar_hotel",
                "description": "Análisis específico de un hotel",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "hotel_id": {
                            "type": "number",
                            "description": "ID del hotel"
                        }
                    },
                    "required": ["hotel_id"]
                }
            },
            {
                "name": "problemas_criticos", 
                "description": "Mostrar problemas críticos identificados",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "incluir_sql": {
                            "type": "boolean",
                            "description": "Incluir soluciones SQL",
                            "default": True
                        }
                    }
                }
            },
            {
                "name": "consulta_sql",
                "description": "Ejecutar consulta SQL personalizada",
                "inputSchema": {
                    "type": "object", 
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Consulta SQL SELECT"
                        },
                        "limite": {
                            "type": "number",
                            "description": "Límite de resultados", 
                            "default": 100
                        }
                    },
                    "required": ["query"]
                }
            }
        ]
    
    def get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    async def handle_initialize(self, params):
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": self.server_info
        }
    
    async def handle_tools_list(self, params):
        return {"tools": self.tools}
    
    async def handle_tools_call(self, params):
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})
        
        try:
            if tool_name == "analizar_restricciones":
                return await self._analizar_restricciones(arguments)
            elif tool_name == "analizar_excepciones":
                return await self._analizar_excepciones(arguments)
            elif tool_name == "resumen_sistema":
                return await self._resumen_sistema(arguments)
            elif tool_name == "analizar_hotel":
                return await self._analizar_hotel(arguments)
            elif tool_name == "problemas_criticos":
                return await self._problemas_criticos(arguments)
            elif tool_name == "consulta_sql":
                return await self._consulta_sql(arguments)
            else:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Herramienta '{tool_name}' no encontrada"
                        }
                    ]
                }
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error: {str(e)}"
                    }
                ]
            }
    
    async def _analizar_restricciones(self, args):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT hotel_id, restriction_type, COUNT(*) as cantidad
        FROM restrictions 
        WHERE 1=1
        """
        params = []
        
        if args.get("hotel_id"):
            query += " AND hotel_id = ?"
            params.append(int(args["hotel_id"]))
        
        if args.get("tipo"):
            query += " AND restriction_type LIKE ?"
            params.append(f"%{args['tipo']}%")
        
        query += " GROUP BY hotel_id, restriction_type ORDER BY cantidad DESC LIMIT ?"
        params.append(int(args.get("limite", 50)))
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        cursor.execute("SELECT COUNT(*) FROM restrictions")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT hotel_id) FROM restrictions WHERE hotel_id IS NOT NULL")
        hoteles = cursor.fetchone()[0]
        
        conn.close()
        
        texto = f"ANÁLISIS DE RESTRICCIONES\n"
        texto += f"========================\n\n"
        texto += f"Total restricciones: {total:,}\n"
        texto += f"Hoteles afectados: {hoteles}\n\n"
        
        if results:
            texto += "TOP RESTRICCIONES:\n"
            for row in results[:10]:
                hotel_id = row["hotel_id"] or "N/A"
                tipo = row["restriction_type"]
                cantidad = row["cantidad"]
                texto += f"• Hotel {hotel_id}: {tipo} ({cantidad:,} veces)\n"
                
                if hotel_id == 22:
                    texto += f"  ⚠️ CRÍTICO: Hotel fantasma - NO EXISTE en inventario\n"
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": texto
                }
            ]
        }
    
    async def _analizar_excepciones(self, args):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT exception_type, COUNT(*) as cantidad
        FROM exceptions 
        WHERE 1=1
        """
        params = []
        
        if args.get("tipo"):
            query += " AND exception_type LIKE ?"
            params.append(f"%{args['tipo']}%")
        
        query += " GROUP BY exception_type ORDER BY cantidad DESC LIMIT ?"
        params.append(int(args.get("limite", 30)))
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        conn.close()
        
        texto = f"ANÁLISIS DE EXCEPCIONES\n"
        texto += f"======================\n\n"
        
        if results:
            for row in results:
                tipo = row["exception_type"]
                cantidad = row["cantidad"]
                
                tipo_short = tipo[:80] + "..." if len(tipo) > 80 else tipo
                texto += f"• {tipo_short}: {cantidad:,} veces\n"
                
                if "Room mapping failed" in tipo and "DBL|2P·CLASSIC" in tipo:
                    texto += f"  ⚠️ Hotel 5481 (Guitart Central Park) - Falta mapeo\n"
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": texto
                }
            ]
        }
    
    async def _resumen_sistema(self, args):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        tablas = ["restrictions", "exceptions", "client_searches", "provider_searches", "connector_searches", "logins"]
        conteos = {}
        
        for tabla in tablas:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            conteos[tabla] = cursor.fetchone()[0]
        
        cursor.execute("""
        SELECT hotel_id, COUNT(*) as cantidad
        FROM restrictions 
        WHERE hotel_id IS NOT NULL
        GROUP BY hotel_id 
        ORDER BY cantidad DESC 
        LIMIT 5
        """)
        top_hoteles = cursor.fetchall()
        
        conn.close()
        
        texto = f"RESUMEN DEL SISTEMA SMARTPERLAHUB\n"
        texto += f"=================================\n\n"
        texto += f"📊 ESTADÍSTICAS GENERALES:\n"
        texto += f"• Restricciones: {conteos['restrictions']:,}\n"
        texto += f"• Excepciones: {conteos['exceptions']:,}\n"
        texto += f"• Búsquedas cliente: {conteos['client_searches']:,}\n"
        texto += f"• Búsquedas proveedor: {conteos['provider_searches']:,}\n"
        texto += f"• Búsquedas conector: {conteos['connector_searches']:,}\n"
        texto += f"• Logins: {conteos['logins']:,}\n\n"
        
        total = sum(conteos.values())
        texto += f"TOTAL REGISTROS: {total:,}\n\n"
        
        if top_hoteles:
            texto += f"🏨 HOTELES MÁS PROBLEMÁTICOS:\n"
            for row in top_hoteles:
                hotel_id = row["hotel_id"]
                cantidad = row["cantidad"]
                texto += f"• Hotel {hotel_id}: {cantidad:,} restricciones\n"
                
                if hotel_id == 22:
                    texto += f"  🚨 CRÍTICO: Hotel fantasma\n"
                elif hotel_id == 5481:
                    texto += f"  ⚠️ Guitart Central Park - Room mapping error\n"
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": texto
                }
            ]
        }
    
    async def _analizar_hotel(self, args):
        hotel_id = int(args["hotel_id"])
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT restriction_type, COUNT(*) as cantidad
        FROM restrictions 
        WHERE hotel_id = ?
        GROUP BY restriction_type
        ORDER BY cantidad DESC
        """, (hotel_id,))
        restricciones = cursor.fetchall()
        
        cursor.execute("""
        SELECT exception_type, COUNT(*) as cantidad
        FROM exceptions 
        WHERE context_data LIKE ?
        GROUP BY exception_type
        ORDER BY cantidad DESC
        """, (f"%{hotel_id}%",))
        excepciones = cursor.fetchall()
        
        conn.close()
        
        texto = f"ANÁLISIS DEL HOTEL {hotel_id}\n"
        texto += f"==========================\n\n"
        
        if hotel_id == 22:
            texto += f"🚨 HOTEL FANTASMA DETECTADO\n"
            texto += f"Este hotel NO EXISTE en el inventario pero tiene restricciones activas.\n"
            texto += f"ACCIÓN REQUERIDA: Limpiar configuración inmediatamente.\n\n"
        elif hotel_id == 5481:
            texto += f"🏨 GUITART CENTRAL PARK AQUA RESORT\n"
            texto += f"Ubicación: Lloret de Mar, España\n"
            texto += f"Problema: Room mapping 'DBL|2P·CLASSIC' faltante\n\n"
        
        if restricciones:
            texto += f"📊 RESTRICCIONES:\n"
            for row in restricciones:
                tipo = row["restriction_type"]
                cantidad = row["cantidad"]
                texto += f"• {tipo}: {cantidad:,} veces\n"
        else:
            texto += f"✅ Sin restricciones registradas\n"
        
        if excepciones:
            texto += f"\n⚡ EXCEPCIONES:\n"
            for row in excepciones:
                tipo = row["exception_type"][:60] + "..." if len(row["exception_type"]) > 60 else row["exception_type"]
                cantidad = row["cantidad"]
                texto += f"• {tipo}: {cantidad:,} veces\n"
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": texto
                }
            ]
        }
    
    async def _problemas_criticos(self, args):
        incluir_sql = args.get("incluir_sql", True)
        
        texto = f"PROBLEMAS CRÍTICOS IDENTIFICADOS\n"
        texto += f"================================\n\n"
        
        texto += f"🚨 1. HOTEL 22 - HOTEL FANTASMA\n"
        texto += f"   Problema: 72,787 exclusiones de hotel inexistente\n"
        texto += f"   Impacto: 99.7% de todas las restricciones\n"
        texto += f"   Estado: CRÍTICO - Requiere acción inmediata\n"
        
        if incluir_sql:
            texto += f"   Solución SQL:\n"
            texto += f"   UPDATE partners.\"ProviderConnections\" \n"
            texto += f"   SET \"ExcludeHotelIds\" = REPLACE(\"ExcludeHotelIds\", '22,', '')\n"
            texto += f"   WHERE \"ExcludeHotelIds\" LIKE '%22%';\n"
        
        texto += f"\n🏨 2. HOTEL 5481 - ROOM MAPPING ERROR\n"
        texto += f"   Hotel: Guitart Central Park Aqua Resort\n"
        texto += f"   Problema: 4,374 errores mapeo 'DBL|2P·CLASSIC'\n"
        texto += f"   Impacto: 99.8% de todas las excepciones\n"
        texto += f"   Estado: URGENTE - Mapeo faltante\n"
        
        if incluir_sql:
            texto += f"   Solución SQL:\n"
            texto += f"   INSERT INTO mapping.\"RoomMappings\" \n"
            texto += f"   (\"IntegrationSystemId\", \"ExternalId\", \"RoomTypeId\")\n"
            texto += f"   VALUES (1, 'DBL|2P·CLASSIC', '[ID_ROOM_TYPE]');\n"
        
        texto += f"\n📊 3. PERFORMANCE ISSUES\n"
        texto += f"   Problema: Búsquedas de hasta 24.9 segundos\n"
        texto += f"   Causa: Posible stress testing\n"
        texto += f"   Estado: MONITOR - Implementar alertas\n\n"
        
        texto += f"PLAN DE ACCIÓN:\n"
        texto += f"• Inmediato (0-2h): Ejecutar SQL para Hotel 22 y 5481\n"
        texto += f"• Urgente (2-8h): Implementar monitoreo en tiempo real\n"
        texto += f"• Seguimiento: Migrar a PostgreSQL y dashboards\n"
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": texto
                }
            ]
        }
    
    async def _consulta_sql(self, args):
        query = args["query"].strip()
        limite = int(args.get("limite", 100))
        
        if not query.lower().strip().startswith("select"):
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Error: Solo se permiten consultas SELECT"
                    }
                ]
            }
        
        prohibidas = ["insert", "update", "delete", "drop", "create", "alter"]
        query_lower = query.lower()
        for palabra in prohibidas:
            if palabra in query_lower:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Error: Operación '{palabra}' no permitida"
                        }
                    ]
                }
        
        if "limit" not in query_lower:
            query += f" LIMIT {limite}"
        
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            conn.close()
            
            if not results:
                texto = "No se encontraron resultados."
            else:
                headers = list(results[0].keys())
                texto = f"RESULTADOS DE CONSULTA ({len(results)} filas):\n"
                texto += "=" * 50 + "\n\n"
                
                for i, row in enumerate(results):
                    texto += f"Fila {i+1}:\n"
                    for header in headers:
                        valor = row[header]
                        texto += f"  {header}: {valor}\n"
                    texto += "\n"
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": texto
                    }
                ]
            }
            
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error en consulta SQL: {str(e)}"
                    }
                ]
            }

# Protocolo MCP simplificado
async def main():
    """Servidor MCP usando stdio"""
    server = SmartPerlahubMCP()
    
    while True:
        try:
            # Leer línea de stdin
            line = sys.stdin.readline()
            if not line:
                break
            
            try:
                message = json.loads(line.strip())
            except json.JSONDecodeError:
                continue
            
            method = message.get("method", "")
            params = message.get("params", {})
            msg_id = message.get("id")
            
            # Procesar mensaje
            if method == "initialize":
                result = await server.handle_initialize(params)
            elif method == "tools/list":
                result = await server.handle_tools_list(params)
            elif method == "tools/call":
                result = await server.handle_tools_call(params)
            else:
                result = {"error": f"Unknown method: {method}"}
            
            # Responder
            response = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": result
            }
            
            print(json.dumps(response))
            sys.stdout.flush()
            
        except EOFError:
            break
        except Exception as e:
            # Error response
            error_response = {
                "jsonrpc": "2.0",
                "id": message.get("id") if 'message' in locals() else None,
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main())