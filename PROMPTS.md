# Registro de Prompts e Interacciones con IA

Este documento registra las interacciones realizadas con herramientas de inteligencia artificial durante el desarrollo del proyecto siguiendo los lineamientos requeridos.

## HITO 1 

### Registro de Prompt #1
- **Fecha:** 2026-10-05
- **Módulo/Función:** Estructura inicial del repositorio
- **Prompt Enviado:** "Explicación del proyecto TI-Metrics y guía de configuración inicial"
- **Respuesta de la IA:** Explicación del proyecto, cronograma para Hito 1 y estructura de carpetas.
- **Análisis Crítico:** La estructura propuesta separa correctamente la capa de datos crudos (data/) de la lógica de extracción y servicios (src/), pero faltaba incluir el archivo.gitignore y los inicializadores __init__.py para reconocer paquetes en Python.
- **Versión de Código Propuesta por la IA:**
```
  TI-Metrics/
  ├── data/
  ├── src/
  │   ├── parsers/to
  │   └── services/
  ├── docs/
  └── tests/
```
- **Solución Final Aplicada:**
```
TI-Metrics/
├── .gitignore
├── PROMPTS.md
├── requirements.txt
├── data/
│   ├── logs.csv
│   └── events.json
├── src/
│   ├── __init__.py
│   ├── parsers/
│   └── services/
├── docs/
└── tests/
    └── __init__.py
```
  
### Registro de Prompt #2
- **Fecha:** 2026-10-06
- **Módulo/Función:** Parsers locales y limpieza de datos (CSV y JSON)
- **Prompt Enviado:** "¿Cómo puedo entender qué es un parser en Python, no entiendo como puede limpiar datos de registros locales usando tuplas y conjuntos para eliminar duplicados?"
- **Respuesta de la IA:** Propuesta de funciones en src/parsers/ utilizando comprensión de listas, diccionarios y set() para asegurar firmas de unicidad.
- **Análisis Crítico:** El acceso directo mediante corchetes item ['ip'] provoca un KeyError si algún registro del archivo CSV o JSON viene corrupto o sin esa llave, además de no validar si el archivo existe antes de leerlo.
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
- **Solución Aplicada:** Implementación de csv_parser.py y json_parser.py con manejo de excepciones básicas.

### Registro de Prompt #3

- **Fecha:** 2026-10-08
- **Módulo/Función:** Consumo de API REST (GBIF y Respaldo IP) y Manejo Defensivo
- **Prompt Enviado:** "Puedes verificar la estructura lógica de los servicios que hice para el servicio de gbif y del IP"
- **Respuesta de la IA:** Creación de módulos de servicio (gbif_service.py e ip_service.py) incorporando bloques try-except para requests.exceptions.Timeout y RequestException.
- **Análisis Crítico:** El manejo defensivo asegura que el sistema no falle ante caídas de la red o respuestas tardías de la API externa.
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
- **Solución Final Aplicada:** Integración exitosa de la API ambiental de GBIF y la API secundaria de geolocalización IP como plan de respaldo.

###  Registro de Prompt #4
- **Fecha:** 2026-10-10
- **Módulo/Función:** Orquestación, Cálculo de Métricas y Exportación JSON
- **Prompt Enviado:** "Ayúdame a verificar el código de los orquestadores principales (archivos main) para calcular métricas de errores, detectar anomalías geográficas y generar los reportes JSON. Explícame qué es y para qué sirve la función os.makedirs."
- **Respuesta de la IA:** Estructuración de los scripts main_gbif.py y main_ip.py calculando el porcentaje de errores HTTP 500, identificando registros críticos y exportando los resultados a formato JSON.
- **Análisis Crítico:** Satisface por completo los requerimientos del Paso 4 de la rúbrica institucional sobre métricas clave y persistencia en JSON.
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
- **Solución Final Aplicada:** Creación de los orquestadores finales que generan tanto la salida por consola como los reportes estructurados en la carpeta data/.


## HITO 2 

### Registro de Prompt # 1
- **Fecha:** 2026-10-30
- **Módulo/Función:** csv_parser.py, json_parser.py, ip_parser.py, ip_service.py y orquestador de reporte (main)
- **Prompt Enviado:** "Revisión y validación del código del Hito 1: confirmación de message como str en events.json, revisión de ip_parser.py, prueba de https:// vs http:// (error 403) en ip_service.py, revisión del main y explicación de os.makedirs("../data", exist_ok=True)."
- **Respuesta de la IA:** Se validó que json_parser.py funciona sin cambios con message como str, que ip_parser.py deduplica con tupla y set() y convierte coordenadas a float (o 0.0), que ip_service.py debe mantener http:// porque https:// devuelve 403 en el plan gratuito, y que os.makedirs("../data", exist_ok=True) crea el directorio si no existe sin fallar si ya existe.
- **Análisis Crítico:** ip_parser.py captura excepciones generales y maneja respuestas vacías o fallidas (status == 'fail'), aunque casos como None o tipos no diccionario caen en except Exception. En ip_service.py, https:// no es viable en el plan gratuito por el 403. En el main, las rutas relativas (../data) dependen del directorio desde donde se ejecute el script y la métrica de errores 500 es simulada en el Hito 1.
- **Solución Final Aplicada:** Se mantuvieron csv_parser.py, json_parser.py, ip_parser.py y [http://ip-api.com/json/](http://ip-api.com/json/){direccion_ip} en ip_service.py sin cambios innecesarios, y se dejó el reporte del Hito 1 operativo a la espera de la retroalimentación docente.

### Registro de Prompt # 2
- **Fecha:** 2026-11-2
- **Módulo/Función:** Diseño UML Hito 2 (IpService, IpParser, Metricas, GeneradorReporte, ErrorHttp, ErrorCliente400, ErrorServidor500)
- **Prompt Enviado:**¿el diagrama UML del Hito 2 lo hacemos a mano para entenderlo mejor?, mandé fotos de mi flujo y mis clases hechas a mano, pedí armar el UML aplicando tus correcciones, consulté dónde ubicar el código 200 y acordamos dejarlo como atributo en IpService, pedí el UML completo con ese cambio y consulté cómo repartir las clases en archivos siguiendo la estructura CLI del proyecto (services, parsers, models, utils) para intentar programarlas yo primero
- **Respuesta de la IA:** Se reordenó el flujo para que IpService consulte primero, luego IpParser limpie/deduplique, después Metricas calcule indicadores y finalmente GeneradorReporte exporte el JSON; se retiró 200 de las clases de error y se incorporó como atributo de estado HTTP (codigo_estado) en IpService, manteniendo agregaciones, herencia en errores 400/500 y la organización en carpetas.
- **Análisis Crítico:** En el borrador inicial el flujo partía de ip_parser antes de consultar la API, se mezclaban variables de paso con métodos y el código 200 figuraba junto a errores cuando en HTTP representa respuesta exitosa. Además, conviene tener clara la diferencia entre clases que representan datos/errores y clases que ejecutan acciones o cálculos.
- **Solución Final Aplicada:** Se consolidó el diagrama UML completo del Hito 2 con codigo_estado en IpService, jerarquía ErrorHttp -> ErrorCliente400 / ErrorServidor500, relaciones de agregación y distribución modular en archivos/carpetas.

### Registro de Prompt # 3
- **Fecha:** 2026-11-7
- **Módulo/Función:** src/services/ip_service.py (IpService.__init__, IpService.consultar_ip)
- **Prompt Enviado:** Empecé a escribir IpService por mi cuenta y te fui mostrando mis intentos y dudas con los atributos, el método consultar_ip, la URL y el código de estado; cuando ya me enredé con el último intento te pedí que lo ajustaras tú, y luego te pregunté qué hacía url.rstrip("/") y si realmente era necesario.
- **Respuesta de la IA:** Se estructuró IpService con __init__(self, url: str = "[http://ip-api.com/json](http://ip-api.com/json)", timeout: int = 5, estado=None) y consultar_ip(self, ip: str) usando una variable local url_consulta para no sobrescribir self.url ni duplicar ip en el mensaje, guardando self.estado = respuesta.status_code y devolviendo respuesta.json() cuando self.estado == 200 (o [] en caso contrario o ante Timeout / RequestException). Se aclaró que url.rstrip("/") solo evita dobles barras si hay / final y no es estrictamente obligatorio si la URL base ya viene limpia.
- **Análisis Crítico:** En los primeros borradores se usó @property con parámetro ip, se intentó asignar self.url.ip = ip sobre un str, se pasó self.estado a requests.get, se evaluó self.estado antes de asignarlo desde respuesta.status_code y se sobrescribía self.url en cada consulta.
- **Solución Final Aplicada:** Se dejó la versión limpia de IpService con __init__ y consultar_ip(self, ip: str) validando self.estado == 200 y capturando excepciones de requests, lista para pasar a implementar IpParser.
- **Versión de Código Propuesta por la IA:**
```
import requests


class IpService:
    def __init__(
        self,
        url: str = "http://ip-api.com/json",
        timeout: int = 5,
        estado=None,
    ):
        self.url = url.rstrip("/")
        self.timeout = timeout
        self.estado = estado

    def consultar_ip(self, ip: str):
        url_consulta = f"{self.url}/{ip}"
        print(f"[IP Service] Consultando geolocalización para la IP: '{ip}'...")
        try:
            respuesta = requests.get(url_consulta, timeout=self.timeout)
            self.estado = respuesta.status_code

            if self.estado != 200:
                print(
                    f"[Error IP Service] La API respondió con el código: {self.estado}"
                )
                return []

            print("[IP Service] ¡Conexión exitosa con la API de IPs!")
            return respuesta.json()

        except requests.exceptions.Timeout:
            print("[Error IP Service] La petición tardó demasiado (Timeout).")
            return []
        except requests.exceptions.RequestException as e:
            print(f"[Error IP Service] Error de red: {e}")
            return []
```
### Registro de Prompt # 4
- **Fecha:** 2026-11-13
- **Módulo/Función:** src/parsers/ip_parser.py (IpParser.__init__, IpParser.parser_ip)
- **Prompt Enviado:** "Pasé a implementar la clase IpParser por mi cuenta siguiendo el diseño UML, te mostré mi primer borrador, ajusté la inicialización de los atributos mutables y lo que devuelve el except tras tus observaciones, y te confirmé si ya estaba listo antes de pasar a la siguiente clase."
- **Respuesta de la IA:** Se validó la estructura de IpParser con self.registros_unicos y self.registros_vistos, el soporte para dict o list, el filtro de status == 'fail', la deduplicación mediante tupla y set(), y la conversión segura de lat y lon a float (o 0.0), confirmando que quedó funcional para el Hito 2.
- **Análisis Crítico:** En el primer borrador registros_unicos y registros_vistos eran obligatorios en __init__ (lo cual conviene evitar en argumentos mutables por defecto o dejarlos opcionales con inicialización segura en None) y el bloque except devolvía [] en vez de self.registros_unicos, perdiendo coherencia con el estado acumulado de la instancia.
- **Solución Final Aplicada:** Se dejó IpParser con registros_unicos=None y registros_vistos=None inicializados de forma segura en __init__, parser_ip actualizando el estado de la instancia y devolviendo self.registros_unicos incluso ante excepciones.

### Registro de Prompt # 5
- **Fecha:** 2026-11-14
- **Módulo/Función:** src/models/Metricas.py (ErrorHttp, Error500)
- **Prompt Enviado:** "La ubicación para la importación me marca un error que hice mal"
- **Respuesta de la IA:**
```
from abc import ABC, abstractmethod
from src.services.IpService import IpService

class ErrorHttp(ABC):
    def __init__(self, codigo_estado: int, mensaje: str, ip_servicio: IpService):
        self.codigo_estado = codigo_estado
        self.mensaje = mensaje
        self.ip_servicio = ip_servicio

    @abstractmethod
    def simulacion_errores(self, ip: str | None = None):
        pass

    def consultar_ip(self, ip: str):
        return self.ip_servicio.consultar_ip(ip)


class Error500(ErrorHttp):
    def __init__(self, codigo_estado: int, mensaje: str, ip_servicio: IpService, porcentaje: float = 0.0):
        super().__init__(codigo_estado, mensaje, ip_servicio)
        self.porcentaje = porcentaje
        self.ip: str | None = None

    def consultar_ip(self, ip: str):
        self.ip = ip
        return self.ip_servicio.consultar_ip(self.ip)

    def simulacion_errores(self, ip: str | None = None) -> float:
        ip_objetivo = ip or self.ip or "24.48.0.1"
        self.ip = ip_objetivo
        registros = self.ip_servicio.consultar_ip(self.ip)
        if registros:
            total_peticiones = len(registros) if isinstance(registros, list) else (1 if isinstance(registros, dict) else 0)
            simulacion_errores_500 = 0
            self.porcentaje = (simulacion_errores_500 / total_peticiones) * 100 if total_peticiones > 0 else 0.0
        else:
            self.porcentaje = 0.0
        return self.porcentaje
```
- **Análisis Crítico:** Al intentar estructurar la clase de errores incluyendo los cálculos y porcentajes allí mismo, surgieron dudas sobre cómo organizar las responsabilidades, cómo importar IpService según la ubicación del archivo, cómo manejar self.ip y consultar_ip vía ip_servicio, y cómo contar registros según si ip-api.com devolvía dict o list. Dejar los cálculos dentro de la clase de error hacía que mezclara tareas.
- **Solución Final Aplicada:**
```
from abc import ABC, abstractmethod
from src.services.IpService import IpService

class ErrorHttp(ABC):

    def __init__(self, codigo: int, mensaje: str, ip_servicio: IpService | None = None):
        self.codigo = codigo
        self.mensaje = mensaje
        self.ip_servicio = ip_servicio

    def mostrar_error(self) -> str:
        return f"HTTP {self.codigo}: {self.mensaje}"

    @abstractmethod
    def detalle_error(self) -> str:
        pass

class Error400(ErrorHttp):

    def __init__(self, mensaje: str = "Solicitud o IP inválida del cliente", ip_servicio: IpService | None = None):
        super().__init__(400, mensaje, ip_servicio)

    def detalle_error(self) -> str:
        return f"Error de cliente ({self.codigo}): revisar parámetros o IP enviada -> {self.mensaje}"


class Error500(ErrorHttp):
    def __init__(self, mensaje: str = "Error interno del servidor", ip_servicio: IpService | None = None):
        super().__init__(500, mensaje, ip_servicio)

    def detalle_error(self) -> str:
        return f"Error de cliente ({self.codigo}): revisar parámetros o IP enviada -> {self.mensaje}"
```
### Registro de Prompt # 6
- **Fecha:** 2026-11-20
- **Módulo/Función:** src/models/Metricas.py (Errores, Metricas)
- **Prompt Enviado:** "Hola, volví, pero decidí cambiar la clase metricas y errores. Habíamos establecido que el error sea solo el 500 porque es un error de servidor aunque si deberíamos considerar por si nosotros como clientes cometemos un error. El problema tal como tenemos hecho está algo enredadas las dos."
- **Respuesta de la IA:** Coincido es mejor separar las clases y archivos porque así cada pieza cumple una sola responsabilidad y se ajusta mucho mejor al diseño UML que estructuramos. Al sacar los cálculos de las clases de error y llevarlos a una clase dedicada con un método abstracto y dos métodos concretos con indicadores distintos para error 400 y error 500, evitamos mezclar lógica de métricas dentro de los errores y dejamos cada capa con su propósito claro.
- **Análisis Crítico:** Mezclar los cálculos de métricas y los porcentajes dentro de las clases de error generaba confusión y acoplamiento innecesario. Al separar Errores.py y Metricas.py y definir un método abstracto junto con dos indicadores distintos para 400 y 500, el diseño UML queda más claro y cada clase mantiene su propósito.
- **Solución Final Aplicada:**
```
from abc import ABC, abstractmethod

class BaseMetricasError(ABC):
    def __init__(self, registros: list):
        self.registros = registros
        self.ips_criticas: list[str] = []

    @abstractmethod
    def resumen_metricas(self) -> dict:
        pass


class Metricas(BaseMetricasError):
    def __init__(self, registros: list, errores_500: int = 0):
        super().__init__(registros)
        self.errores_500 = errores_500

    def indicador_error_400(self) -> dict:
        """Indicador de calidad/validez de entrada (400): consultas o IPs inválidas."""
        total = len(self.registros)
        if total == 0:
            return {
                "tipo_indicador": "validez_peticion_400",
                "total_evaluados": 0,
                "fallos_400": 0,
                "tasa_rechazo_%": 0.0,
            }

        fallos_400 = 0
        for reg in self.registros:
            if not isinstance(reg, dict):
                fallos_400 += 1
                continue

            ip = reg.get("query") or reg.get("ip")
            ip_invalida = not isinstance(ip, str) or not ip.strip()
            fallo_consulta = reg.get("status") == "fail" or reg.get("codigo_estado") == 400

            if ip_invalida or fallo_consulta:
                fallos_400 += 1

        tasa_rechazo = round((fallos_400 / total) * 100, 2)
        return {
            "tipo_indicador": "validez_peticion_400",
            "total_evaluados": total,
            "fallos_400": fallos_400,
            "tasa_rechazo_%": tasa_rechazo,
        }

    def indicador_error_500(self) -> dict:
        """Indicador de estabilidad del servidor (500): impacto en registros e IPs críticas."""
        total = len(self.registros)
        criticas: list[str] = []
        fallos_detectados = self.errores_500

        for reg in self.registros:
            if isinstance(reg, dict):
                es_500 = reg.get("error_500") is True or reg.get("codigo_estado") == 500
                if es_500:
                    fallos_detectados += 1
                    ip = reg.get("query") or reg.get("ip")
                    if isinstance(ip, str) and ip.strip() and ip not in criticas:
                        criticas.append(ip)

        self.ips_criticas = criticas
        impacto_servidor = round((fallos_detectados / total) * 100, 2) if total > 0 else 0.0

        return {
            "tipo_indicador": "estabilidad_servidor_500",
            "total_evaluados": total,
            "fallos_500": fallos_detectados,
            "impacto_servidor_%": impacto_servidor,
            "ips_criticas": self.ips_criticas,
        }

    def resumen_metricas(self) -> dict:
        return {
            "indicador_400": self.indicador_error_400(),
            "indicador_500": self.indicador_error_500(),
        }
```
### Registro de Prompt # 7
- **Fecha:** 2026-11-23
- **Módulo/Función:** src/GeneradorReporte.py (Reporte, EstructuraDiccionario)
- **Prompt Enviado:** "si todo listo ahora vamos a la clase reporte que debe estar en utils no ?"
- **Respuesta de la IA:** Se estructuró la clase abstracta Reporte (con construir_payload como método abstracto) y la subclase EstructuraDiccionario (antes estructura_diccionario) recibiendo ruta_salida, ip, error, metricas y registros, simplificando las llamadas directas a resumen_metricas() y detalle_error() en lugar de helpers complejos con getattr o callable.
- **Análisis Crítico:** Al inicio se presentaron errores de referencias no resueltas en super().__init__ y de anotación de tipos al pasar None o una list en lugar de IpParser. Mantener la llamada directa a los métodos ya creados en Metricas y Errores evitó complejidad innecesaria y permitió alinear la estructura con la idea original del diseño.
- **Solución Final Aplicada:**
```
import json
from pathlib import Path
from abc import ABC, abstractmethod
from src.services.IpService import IpService
from src.parsers.IpParser import IpParser
from src.models.Errores import ErrorHttp
from src.models.Metricas import BaseMetricasError


class Reporte(ABC):
    def __init__(
        self,
        ruta_salida: str,
        ip: IpService,
        error: ErrorHttp | None,
        metricas: BaseMetricasError,
        registros: IpParser | list,
    ):
        self.ruta_salida = ruta_salida
        self.ip = ip
        self.error = error
        self.metricas = metricas
        self.registros = registros

    @abstractmethod
    def construir_payload(self) -> dict:
        pass


class EstructuraDiccionario(Reporte):
    def __init__(
        self,
        ruta_salida: str,
        ip: IpService,
        error: ErrorHttp | None,
        metricas: BaseMetricasError,
        registros: IpParser | list,
        data: dict | None = None,
    ):
        super().__init__(ruta_salida, ip, error, metricas, registros)
        self.data: dict = data if data is not None else {}

    def construir_payload(self) -> dict:
        lista_registros = (
            self.registros
            if isinstance(self.registros, list)
            else getattr(self.registros, "registros", [])
        )

        self.data = {
            "ruta_salida": self.ruta_salida,
            "servicio_ip": type(self.ip).__name__,
            "metricas": self.metricas.resumen_metricas(),
            "total_registros_adjuntos": len(lista_registros),
            "registros": lista_registros,
            "error": {
                "codigo": self.error.codigo,
                "mensaje": self.error.mensaje,
                "detalle": self.error.detalle_error(),
            }
            if self.error is not None
            else None,
        }
        return self.data

    def guardar_json(self, data: dict | None = None) -> None:
        payload = data if data is not None else (self.data if self.data else self.construir_payload())
        ruta = Path(self.ruta_salida)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with ruta.open("w", encoding="utf-8") as archivo:
            json.dump(payload, archivo, indent=2, ensure_ascii=False)
```
### Registro de Prompt # 8
- **Fecha:** 2026-11-24
- **Módulo/Función:** src/GeneradorReporte.py (main, ruta_salida)
- **Prompt Enviado:** "Hola, volví para completar el error de ayer" / "ok, ya borreo como ponemos el camino ?"
- **Respuesta de la IA:** Se resolvió el TypeError al instanciar Metricas pasando registros en el bloque de prueba __main__, se corrigió la secuencia de escape '\d' en la ruta y se calculó la ruta hacia data/reporte_ips_output.json en la raíz del proyecto usando Path(__file__).resolve().parents[1] para evitar que el archivo se generara dentro de src o sobrescribiera salidas anteriores.
- **Análisis Crítico:** Ejecutar el script sin pasar registros a Metricas bloqueaba la prueba inicial, y usar rutas relativas ambiguas desde src provocaba que los reportes se crearan dentro de subcarpetas de src en lugar de TI-Metrics/data. Resolver la ruta desde __file__ y limpiar las carpetas duplicadas garantizó que la salida quede en la carpeta data de la raíz del proyecto.
- **Solución Final Aplicada:**
```
if __name__ == "__main__":
    from src.models.Metricas import Metricas

    raiz_proyecto = Path(__file__).resolve().parents[1]
    ruta_reporte = raiz_proyecto / "data" / "reporte_ips_output.json"

    registros_prueba = [
        {"query": "8.8.8.8", "status": "success", "codigo_estado": 200},
        {"query": "", "status": "fail", "codigo_estado": 400},
    ]

    servicio_ip = IpService()
    parser_ip = IpParser()
    metricas_prueba = Metricas(registros=registros_prueba)
    error_prueba = None

    reporte = EstructuraDiccionario(
        ruta_salida=str(ruta_reporte),
        ip=servicio_ip,
        error=error_prueba,
        metricas=metricas_prueba,
        registros=registros_prueba,
    )

    reporte.construir_payload()
    reporte.guardar_json()
    print(f"Reporte generado correctamente en: {ruta_reporte}")
```
