import csv

def parse_csv_logs(ruta_archivo):
    """
    Lee el archivo CSV de logs, elimina registros duplicados
    usando un conjunto (set) y devuelve una lista de diccionarios limpios.
    """
    logs_unicos = []
    logs_vistos = set()
    try:
        with open(ruta_archivo, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Creación de  tupla inmutable para identificar cada fila de forma única
                log_firma = (
                    row['timestamp'],
                    row['ip'],
                    row['status_code'],
                    row['method'],
                    row['endpoint']
                )

                # Si la fila no ha sido vista antes
                if log_firma not in logs_vistos:
                    logs_vistos.add(log_firma)
                    logs_unicos.append({
                        'timestamp': row['timestamp'],
                        'ip': row['ip'],
                        'status_code': int(row['status_code']),
                        'method': row['method'],
                        'endpoint': row['endpoint'],
                        'cpu_usage': float(row['cpu_usage']),
                        'memory_usage': float(row['memory_usage'])
                    })

        print(f"[CSV Parser] Éxito: Se procesaron {len(logs_unicos)} registros únicos.")
        return logs_unicos

    except FileNotFoundError:
        print(f"[Error] El archivo no fue encontrado en la ruta: {ruta_archivo}")
        return []
    except Exception as e:
        print(f"[Error] Ocurrió un error inesperado al leer el CSV: {e}")
        return []


# Bloque para probar el parser directamente
if __name__ == "__main__":
    datos = parse_csv_logs("../../data/logs.csv")  # <--- Se especifico la ruta de archivo  para entrar a data
    print("\nEjemplo del primer registro procesado:")
    if datos:
        print(datos[0])