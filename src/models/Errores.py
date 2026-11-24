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


