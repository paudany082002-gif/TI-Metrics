from abc import ABC, abstractmethod

class BaseMetricasError(ABC):
    def __init__(self, registros: list):
        self.registros = registros
        self.ips_criticas: list[str] = []

    @abstractmethod
    def resumen_metricas(self) -> dict:
        pass


class Metricas(BaseMetricasError):
    def __init__(self, registros: list, errores_500: int = 0):
        super().__init__(registros)
        self.errores_500 = errores_500

    def indicador_error_400(self)-> dict:
        """Indicador de calidad/validez de entrada (400): consultas o IPs inválidas."""
        total = len(self.registros)
        if total == 0:
            return {
                "tipo_indicador": "validez_peticion_400",
                "total_evaluados": 0,
                "fallos_400": 0,
                "tasa_rechazo_%": 0.0,
            }

        fallos_400 = 0
        for reg in self.registros:
            if not isinstance(reg, dict):
                fallos_400 += 1
                continue

            ip = reg.get("query") or reg.get("ip")
            ip_invalida = not isinstance(ip, str) or not ip.strip()
            fallo_consulta = reg.get("status") == "fail" or reg.get("codigo_estado") == 400

            if ip_invalida or fallo_consulta:
                fallos_400 += 1

        tasa_rechazo = round((fallos_400 / total) * 100, 2)
        return {
            "tipo_indicador": "validez_peticion_400",
            "total_evaluados": total,
            "fallos_400": fallos_400,
            "tasa_rechazo_%": tasa_rechazo,
        }

    def indicador_error_500(self) -> dict:
        """Indicador de estabilidad del servidor (500): impacto en registros e IPs críticas."""
        total = len(self.registros)
        criticas: list[str] = []
        fallos_detectados = self.errores_500

        for reg in self.registros:
            if isinstance(reg, dict):
                es_500 = reg.get("error_500") is True or reg.get("codigo_estado") == 500
                if es_500:
                    fallos_detectados += 1
                    ip = reg.get("query") or reg.get("ip")
                    if isinstance(ip, str) and ip.strip() and ip not in criticas:
                        criticas.append(ip)

        self.ips_criticas = criticas
        impacto_servidor = round((fallos_detectados / total) * 100, 2) if total > 0 else 0.0

        return {
            "tipo_indicador": "estabilidad_servidor_500",
            "total_evaluados": total,
            "fallos_500": fallos_detectados,
            "impacto_servidor_%": impacto_servidor,
            "ips_criticas": self.ips_criticas,
        }

    def resumen_metricas(self) -> dict:
        return {
            "indicador_400": self.indicador_error_400(),
            "indicador_500": self.indicador_error_500(),
        }