import requests

class IpService:
    def __init__(self, url:str = "http://ip-api.com/json/"  ,  timeout:int = 5, estado = None):
        self.url = url
        self.timeout = timeout
        self.estado = estado

    def consultar_ip (self, ip:str):
        url_consulta = f"{self.url}/{ip}"
        print(f"[IP Service] Consultando geolocalización para la IP: ' {ip} '...")
        try:
            respuesta = requests.get(url_consulta, timeout = self.timeout)
            self.estado = respuesta.status_code
            if self.estado != 200:
                print(f"[Error IP Service] La API respondió con el código: {self.estado}")
                return []
            else:
                print("[IP Service] ¡Conexión exitosa con la API de IPs!")
                return respuesta.json()

        except requests.exceptions.Timeout:
            print("[Error IP Service] La petición tardó demasiado (Timeout).")
            return []
        except requests.exceptions.RequestException as e:
            print(f"[Error IP Service] Error de red: {e}")
            return []


