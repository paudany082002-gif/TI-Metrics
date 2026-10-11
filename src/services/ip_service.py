import requests
from src.parsers.ip_parser import parse_ip_geolocation


def consultar_ip(direccion_ip="24.48.0.1"):
    """
    Consulta la API pública de ip-api.com para enriquecer una dirección IP
    con datos geográficos, aplicando timeout y manejo de errores.
    """
    url = f"http://ip-api.com/json/{direccion_ip}"

    print(f"[IP Service] Consultando geolocalización para la IP: '{direccion_ip}'...")

    try:
        respuesta = requests.get(url, timeout=5)

        if respuesta.status_code == 200:
            print("[IP Service] ¡Conexión exitosa con la API de IPs!")
            datos_json = respuesta.json()

            # Pasamos los datos al parser de IPs
            datos_limpios = parse_ip_geolocation(datos_json)
            return datos_limpios
        else:
            print(f"[Error IP Service] La API respondió con el código: {respuesta.status_code}")
            return []

    except requests.exceptions.Timeout:
        print("[Error IP Service] La petición tardó demasiado (Timeout).")
        return []
    except requests.exceptions.RequestException as e:
        print(f"[Error IP Service] Error de red: {e}")
        return []


if __name__ == "__main__":
    print("--- Probando el servicio de respaldo de IPs ---")
    resultado = consultar_ip("24.48.0.1")
    if resultado:
        print("\nResultado limpio de la IP:")
        print(resultado[0])