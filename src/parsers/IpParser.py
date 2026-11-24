class IpParser:
    def __init__(self,registros_unicos= None , registros_vistos = None):
        self.registros_unicos = registros_unicos if registros_unicos is not None else []
        self.registros_vistos = registros_vistos if registros_vistos is not None else set ()

    def parser_ip(self, raw_response):
        try:
            resultados = raw_response if isinstance(raw_response, list) else [raw_response]

            for item in resultados:
                if item.get('status') == 'fail':
                    continue
                ip_address = item.get('query')

                # Tupla inmutable como firma para evitar duplicados
                firma = (
                    ip_address,
                    item.get('country'),
                    item.get('city')
                )

                if firma not in self.registros_vistos:
                    self.registros_vistos.add(firma)

                    lat = item.get('lat')
                    lon = item.get('lon')

                    self.registros_unicos.append({
                        'ip': ip_address,
                        'country': item.get('country', 'Unknown'),
                        'region': item.get('regionName', 'Unknown'),
                        'city': item.get('city', 'Unknown'),
                        'latitude': float(lat) if lat is not None else 0.0,
                        'longitude': float(lon) if lon is not None else 0.0,
                        'isp': item.get('isp', 'Unknown')
                    })

            print(f"[IP Parser] Éxito: Se procesaron {len(self.registros_unicos)} registros de IP únicos.")
            return self.registros_unicos

        except Exception as e:
            print(f"[Error] Ocurrió un error al procesar la respuesta de IP: {e}")
            return self.registros_unicos