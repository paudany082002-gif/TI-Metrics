import json

def parse_gbif_occurrences(raw_response):
    """
    Procesa la respuesta JSON cruda de la API de GBIF,
    extrae los registros de ocurrencias, elimina duplicados y tipa los datos.
    """
    registros_unicos = []
    registros_vistos = set()

    try:
        # La API de GBIF suele devolver un diccionario con una clave 'results' que contiene la lista
        resultados = raw_response.get(
            'results', []) \
            if isinstance(raw_response, dict)\
            else raw_response

        for item in resultados:
            # Identificador único del registro en GBIF
            registro_id = item.get('key') or item.get('gbifID')

            # Creamos una tupla inmutable (firma) para evitar duplicados
            firma = (
                registro_id,
                item.get('scientificName'),
                item.get('eventDate'),
                item.get('decimalLatitude'),
                item.get('decimalLongitude')
            )

            # Si la firma no ha sido vista antes, se procesa y se guarda
            if firma not in registros_vistos:
                registros_vistos.add(firma)

                # Limpieza y tipado seguro de coordenadas
                latitud = item.get('decimalLatitude')
                longitud = item.get('decimalLongitude')

                registros_unicos.append({
                    'gbif_id': registro_id,
                    'scientific_name': item.get('scientificName', 'Unknown'),
                    'event_date': item.get('eventDate'),
                    'country': item.get('countryCode'),
                    'latitude': float(latitud) if latitud is not None else 0.0,
                    'longitude': float(longitud) if longitud is not None else 0.0,
                    'basis_of_record': item.get('basisOfRecord')
                })

        print(f"[GBIF Parser] Éxito: Se procesaron {len(registros_unicos)} registros ambientales únicos.")
        return registros_unicos

    except Exception as e:
        print(f"[Error] Ocurrió un error al procesar los datos de GBIF: {e}")
        return []


# Bloque de prueba simulando una respuesta de la API de GBIF
if __name__ == "__main__":
    ruta_json = "../../data/respuesta_simulada_de_gbif.json"

    try:
        with open(ruta_json, 'r', encoding='utf-8') as f:
            contenido_json = json.load(f)
            datos = parse_gbif_occurrences(contenido_json)
            print("\nEjemplo del primer evento procesado:")
            if datos:
                print(datos[0])
    except Exception as e:
        print(f"[Error al leer el archivo de prueba] {e}")