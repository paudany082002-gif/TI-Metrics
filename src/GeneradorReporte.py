import json
from pathlib import Path
from src.services.IpService import IpService
from src.parsers.IpParser import IpParser
from src.models.Errores import ErrorHttp
from src.models.Metricas import BaseMetricasError
from abc import ABC, abstractmethod

class Reporte (ABC):
    def __init__ (self, ruta_salida: str, ip:IpService, error: ErrorHttp,
                           metricas: BaseMetricasError, registros:IpParser ):
        self.ruta_salida = ruta_salida
        self.ip = ip
        self.error = error
        self.metricas = metricas
        self.registros = registros
    @abstractmethod
    def construir_payload (self):
        pass

class EstructuraDiccionario (Reporte):
    def __init__ (self, ruta_salida: str, ip:IpService, error: ErrorHttp,
                           metricas: BaseMetricasError, registros:IpParser,data: dict| None = None):
        super().__init__(ruta_salida, ip, error, metricas, registros)
        self.data: dict = data if data is not None else {}

    def construir_payload(self) -> dict:
        lista_registros = (
            self.registros
            if isinstance(self.registros, list)
            else getattr(self.registros, "registros", [])
        )

        self.data = {
            "ruta_salida": self.ruta_salida,
            "servicio_ip": type(self.ip).__name__,
            "metricas": self.metricas.resumen_metricas(),
            "total_registros_adjuntos": len(lista_registros),
            "registros": lista_registros,
            "error": {
                "codigo": self.error.codigo,
                "mensaje": self.error.mensaje,
                "detalle": self.error.detalle_error(),
            }
            if self.error is not None
            else None,
        }
        return self.data

    def guardar_json(self, data: dict | None = None) -> None:
        payload = data if data is not None else (self.data if self.data else self.construir_payload())
        ruta = Path(self.ruta_salida)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with ruta.open("w", encoding="utf-8") as archivo:
            json.dump(payload, archivo, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    from src.models.Metricas import Metricas
    from src.models.Errores import Error400

    servicio_ip = IpService()
    parser_ip = IpParser()
    metricas = Metricas()
    error = None  # O usa Error400("Bad Request", "...") si quieres probar un error

    reporte = EstructuraDiccionario(
        ruta_salida="data/reporte_ips_output.json",
        ip=servicio_ip,
        error=error,
        metricas=metricas,
        registros=parser_ip,
    )

    reporte.construir_payload()
    reporte.guardar_json()
    print("Reporte generado correctamente.")


