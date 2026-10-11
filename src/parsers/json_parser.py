import json
import os

def parse_json_events(ruta_archivo):
    """
    Lee el archivo JSON de eventos, valida su estructura,
    elimina duplicados y devuelve una lista de diccionarios limpios.
    """
    eventos_unicos = []
    eventos_vistos = set()

    try:
        with open(ruta_archivo, mode='r', encoding='utf-8') as file:
            data = json.load(file)

            # Verificación de los datos parta ver si vienen en una lista o en una clave específica
            eventos = data if isinstance(data, list) else data.get('events', [])

            for event in eventos:
                # Creacion de una tupla inmutable para identificar cada evento de forma única
                eventos_firma = (
                    event.get('timestamp'),
                    event.get('event_id'),
                    event.get('level'),
                    event.get('message'),
                    event.get('ip')
                )

                # Si el evento no ha sido visto antes
                if eventos_firma not in eventos_vistos:
                    eventos_vistos.add(eventos_firma)
                    eventos_unicos.append({
                        'timestamp': event.get('timestamp'),
                        'event_id': event.get('event_id'),
                        'level': event.get('level'),
                        'ip': event.get('ip'),
                        'message': event.get('message', {})
                    })

        print(f"[JSON Parser] Éxito: Se procesaron {len(eventos_unicos)} eventos únicos.")
        return eventos_unicos

    except FileNotFoundError:
        print(f"[Error] El archivo JSON no fue encontrado en la ruta: {ruta_archivo}")
        return []
    except json.JSONDecodeError:
        print(f"[Error] El archivo no tiene un formato JSON válido: {ruta_archivo}")
        return []
    except Exception as e:
        print(f"[Error] Ocurrió un error inesperado al leer el JSON: {e}")
        return []


# Bloque para probar el parser
if __name__ == "__main__":
    ruta_json = "../../data/events.json"
    datos = parse_json_events(ruta_json)
    print("\nEjemplo del primer evento procesado:")
    if datos:
        print(datos[0])