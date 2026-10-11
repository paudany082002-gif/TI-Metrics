import json
import os
from src.services.ip_service import consultar_ip

def generar_reporte_ips():
    """
    Orquestador principal para la generación del reporte de geolocalización IP.
    """
    print("   INICIANDO REPORTE DE ENRIQUECIMIENTO DE IPs")

    # Simulación de una IP obtenida de un archivo de logs local
    ip_objetivo = "24.48.0.1"

    # 1. Consulta de IP y aplicación del parser
    registros = consultar_ip(ip_objetivo)

    # 2. Procesamiento, métricas y reporte consolidado
    if registros:
        total_peticiones = len(registros)

        # Métricas defensivas de control de errores HTTP 500 (simuladas en base al éxito de la consulta)
        simulacion_errores_500 = 0
        porcentaje_errores_500 = (simulacion_errores_500 / total_peticiones) * 100 \
            if total_peticiones > 0 else 0.0

        # Detección de IPs críticas o anómalas (ej. país desconocido)
        ips_criticas = [reg['ip']
                        for reg in registros if reg['country'] == 'Unknown']

        # Estructura del diccionario para el archivo JSON de salida
        reporte_data = {
            "tipo_reporte": "Enriquecimiento de Geolocalización IP",
            "total_consultas": total_peticiones,
            "metricas": {
                "porcentaje_errores_http_500": f"{porcentaje_errores_500:.2f}%",
                "total_errores_500": simulacion_errores_500,
                "ips_criticas_o_anonimas": ips_criticas
            },
            "detalle_geolocalizacion": registros
        }

        # Creación segura de la carpeta data/ usando os.makedirs
        os.makedirs("../data", exist_ok=True)
        ruta_salida = "../data/reporte_ips_output.json"

        # Guardar el reporte en formato JSON
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            json.dump(reporte_data, f, indent=4, ensure_ascii=False)

        print(f"\n[Éxito] Reporte JSON generado correctamente en: {ruta_salida}")
        print(f"\n[Reporte Éxito] Se consolidó la información de red para el reporte.")
        print("-" * 50)

        for registro in registros:
            print(f"  Dirección IP: {registro['ip']}")
            print(f"  País: {registro['country']}")
            print(f"  Región: {registro['region']}")
            print(f"  Ciudad: {registro['city']}")
            print(f"  Coordenadas: Lat {registro['latitude']}, Lon {registro['longitude']}")
            print(f"  Proveedor (ISP): {registro['isp']}")
            print("-" * 50)
    else:
        print("[Aviso] No se pudieron procesar datos para el reporte de IPs.")


if __name__ == "__main__":
    generar_reporte_ips()