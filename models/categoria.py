from enum import Enum
from typing import List, Optional

class Categoria(Enum):
    VIVIENDA = "Vivienda"
    MOVILIDAD = "Movilidad"
    ALIMENTACION = "Alimentacion"
    OCIO = "Ocio"
    SUSCRIPCIONES = "Suscripciones"
    SERVICIOS = "Servicios"
    DEUDAS = "Deudas"
    OTROS = "Otros"
    
    @classmethod
    def from_string(cls, valor: str) -> 'Categoria':
        """Convierte string a Categoria, si no existe retorna OTROS"""
        for categoria in cls:
            if categoria.value.lower() == valor.lower():
                return categoria
        return cls.OTROS  # Siempre retorna una Categoria, nunca None
    
    @classmethod
    def listar(cls) -> List[str]:
        return [c.value for c in cls]