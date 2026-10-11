# Registro de Prompts e Interacciones con IA

Este documento registra las interacciones realizadas con herramientas de inteligencia artificial durante el desarrollo del Hito 1, siguiendo los lineamientos académicos de transparencia.

## Registro de Prompt #1

- **Fecha:** 2026-10-05
- **Módulo/Función:** Estructura inicial del repositorio
- **Prompt Enviado:** "Explicación del proyecto TI-Metrics y guía de configuración inicial"
- **Respuesta de la IA:** Explicación del proyecto, cronograma para Hito 1 y estructura de carpetas.
- **Análisis Crítico:** Se revisó la estructura sugerida y cumple con las especificaciones del repositorio del curso.
- **Solución Final Aplicada:** Creación de carpetas base (src, data, docs, tests) y archivos principales.
- **Versión de Código Propuesta por la IA:**
```
  TI-Metrics/
  ├── data/
  ├── src/
  │   ├── parsers/
  │   └── services/
  ├── docs/
  └── tests/
```
  
## Registro de Prompt #2
- **Fecha:** 2026-10-06
- **Módulo/Función:** Parsers locales y limpieza de datos (CSV y JSON)
- **Prompt Enviado:** "¿Cómo puedo entender qué es un parser en Python, no entiendo como puede limpiar datos de registros locales usando tuplas y conjuntos para eliminar duplicados?"
- **Respuesta de la IA:** Propuesta de funciones en src/parsers/ utilizando comprensión de listas, diccionarios y set() para asegurar firmas de unicidad.
- **Análisis Crítico:** Permite un procesamiento eficiente de datos estructurados locales manteniendo buenas prácticas de tipado.
- **Solución Final Aplicada:** Implementación de csv_parser.py y json_parser.py con manejo de excepciones básicas.
- **Versión de Código Propuesta por la IA:**
```
          def limpiar_registros(datos):
              unicos = set()
              resultado = []
              for item in datos:
                  firma = (item.get('id'), item.get('fecha'))
                  if firma not in unicos:
                      unicos.add(firma)
                      resultado.append(item)
              return resultado
````
## Registro de Prompt #3

- **Fecha:** 2026-10-08
- **Módulo/Función:** Consumo de API REST (GBIF y Respaldo IP) y Manejo Defensivo
- **Prompt Enviado:** "Puedes verificar la estructura lógica de los servicios que hice para el servicio de gbif y del IP"
- **Respuesta de la IA:** Creación de módulos de servicio (gbif_service.py y ip_service.py) incorporando bloques try-except para requests.exceptions.Timeout y RequestException.
- **Análisis Crítico:** El manejo defensivo asegura que el sistema no falle ante caídas de la red o respuestas tardías de la API externa.
- **Solución Final Aplicada:** Integración exitosa de la API ambiental de GBIF y la API secundaria de geolocalización IP como plan de respaldo.
- **Versión de Código Propuesta por la IA:**
```
    import requests
    def consultar_servicio_seguro(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.Timeout:
        print("Error: Timeout en la conexión.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error de red: {e}")
        return None
  ```

##  Registro de Prompt #4
- **Fecha:** 2026-10-10
- **Módulo/Función:** Orquestación, Cálculo de Métricas y Exportación JSON
- **Prompt Enviado:** "Ayúdame a verificar el código de los orquestadores principales (archivos main) para calcular métricas de errores, detectar anomalías geográficas y generar los reportes JSON. Explícame qué es y para qué sirve la función os.makedirs."
- **Respuesta de la IA:** Estructuración de los scripts main_gbif.py y main_ip.py calculando el porcentaje de errores HTTP 500, identificando registros críticos y exportando los resultados a formato JSON.
- **Análisis Crítico:** Satisface por completo los requerimientos del Paso 4 de la rúbrica institucional sobre métricas clave y persistencia en JSON.
- **Solución Final Aplicada:** Creación de los orquestadores finales que generan tanto la salida por consola como los reportes estructurados en la carpeta data/.
- **Versión de Código Propuesta por la IA:**
```
       import json
       import os
       os.makedirs("../data", exist_ok=True)
       reporte_data = {
           "total_registros": len(registros),
           "metricas": {"porcentaje_errores_500": "0.00%"},
           "registros": registros
       }
       with open("../data/reporte_output.json", "w", encoding="utf-8") as f:
           json.dump(reporte_data, f, indent=4, ensure_ascii=False)
```
