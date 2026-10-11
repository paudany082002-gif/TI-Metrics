import requests
from src.parsers.gbif_parser import parse_gbif_occurrences


def obtener_datos_gbif(nombre_especie="Tremarctos ornatus", limite=5):
    """
    Se conecta a la API REST pública de GBIF para buscar registros de ocurrencias
    de una especie, utilizando la librería requests con manejo de errores y timeout.
    """
    url = "https://api.gbif.org/v1/occurrence/search"

    # Parámetros de búsqueda para la API
    parametros = {
        "scientificName": nombre_especie,
        "limit": limite
    }

    print(f"[GBIF Service] Consultando la API para la especie: '{nombre_especie}'...")

    try:
        # Hacemos la petición HTTP GET con un timeout de 5 segundos por seguridad
        respuesta = requests.get(url, params=parametros, timeout=5)

        # Verificamos si la petición fue exitosa (código HTTP 200)
        if respuesta.status_code == 200:
            print("[GBIF Service] ¡Conexión exitosa con la API de GBIF!")
            # Convertimos la respuesta cruda a JSON (diccionario de Python)
            datos_json = respuesta.json()

            # Le pasamos los datos crudos a nuestro parser para limpiarlos y estructurarlos
            registros_limpios = parse_gbif_occurrences(datos_json)
            return registros_limpios
        else:
            print(f"[Error GBIF Service] La API respondió con el código de estado: {respuesta.status_code}")
            return []

    except requests.exceptions.Timeout:
        print("[Error GBIF Service] La petición tardó demasiado tiempo en responder (Timeout).")
        return []
    except requests.exceptions.RequestException as e:
        print(f"[Error GBIF Service] Ocurrió un error de red: {e}")
        return []


# Bloque de prueba para ejecutar el servicio directamente
if __name__ == "__main__":
    print("--- Probando el consumo de la API real de GBIF ---")
    resultados = obtener_datos_gbif(nombre_especie="Tremarctos ornatus", limite=3)

    if resultados:
        print(f"\nSe obtuvieron y procesaron {len(resultados)} registros reales de la API.")
        print("Primer registro limpio:")
        print(resultados[0])
    else:
        print("No se pudieron obtener registros.")