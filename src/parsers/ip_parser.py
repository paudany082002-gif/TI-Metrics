def parse_ip_geolocation(raw_response):
    """
    Procesa la respuesta JSON de la API de geolocalización de IPs,
    limpia los datos y asegura el tipado correcto.
    """
    registros_unicos = []
    registros_vistos = set()

    try:
        # ip-api.com puede devolver un solo diccionario o una lista
        resultados = raw_response if isinstance(raw_response, list) else [raw_response]

        for item in resultados:
            # Validar que la consulta fue exitosa según la API
            if item.get('status') == 'fail':
                continue

            ip_address = item.get('query')

            # Tupla inmutable como firma para evitar duplicados
            firma = (
                ip_address,
                item.get('country'),
                item.get('city')
            )

            if firma not in registros_vistos:
                registros_vistos.add(firma)

                lat = item.get('lat')
                lon = item.get('lon')

                registros_unicos.append({
                    'ip': ip_address,
                    'country': item.get('country', 'Unknown'),
                    'region': item.get('regionName', 'Unknown'),
                    'city': item.get('city', 'Unknown'),
                    'latitude': float(lat) if lat is not None else 0.0,
                    'longitude': float(lon) if lon is not None else 0.0,
                    'isp': item.get('isp', 'Unknown')
                })

        print(f"[IP Parser] Éxito: Se procesaron {len(registros_unicos)} registros de IP únicos.")
        return registros_unicos

    except Exception as e:
        print(f"[Error] Ocurrió un error al procesar la respuesta de IP: {e}")
        return []