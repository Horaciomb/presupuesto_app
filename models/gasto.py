from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from .categoria import Categoria

@dataclass
class Gasto:
    concepto: str
    categoria: Categoria
    monto: float
    pagado: bool = False
    fecha: str = ""  # Cambiar a str vacío por defecto
    
    def __post_init__(self):
        if not self.fecha:
            self.fecha = datetime.now().strftime('%Y-%m-%d')
    
    def to_dict(self) -> dict:
        return {
            "concepto": self.concepto,
            "categoria": self.categoria.value,
            "monto": self.monto,
            "pagado": self.pagado,
            "fecha": self.fecha
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Gasto':
        return cls(
            concepto=data['concepto'],
            categoria=Categoria.from_string(data['categoria']),
            monto=float(data['monto']),
            pagado=data.get('pagado', False),
            fecha=data.get('fecha', '')
        )


@dataclass
class GastoFijo(Gasto):
    """Gasto fijo mensual"""
    pass


@dataclass
class GastoVariable(Gasto):
    """Gasto variable con frecuencia"""
    frecuencia_mensual: Optional[int] = None
    monto_por_salida: Optional[float] = None
    monto_gastado: float = 0.0
    saldo_pendiente: float = 0.0
    
    def __post_init__(self):
        super().__post_init__()
        if self.saldo_pendiente == 0:
            self.saldo_pendiente = self.monto
    
    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({
            "frecuencia_mensual": self.frecuencia_mensual,
            "monto_por_salida": self.monto_por_salida,
            "monto_gastado": self.monto_gastado,
            "saldo_pendiente": self.saldo_pendiente
        })
        return base
    
    @classmethod
    def from_dict(cls, data: dict) -> 'GastoVariable':
        return cls(
            concepto=data['concepto'],
            categoria=Categoria.from_string(data['categoria']),
            monto=float(data.get('monto_mensual', data.get('monto', 0))),
            frecuencia_mensual=data.get('frecuencia_mensual'),
            monto_por_salida=data.get('monto_por_salida'),
            monto_gastado=float(data.get('monto_gastado', 0)),
            saldo_pendiente=float(data.get('saldo_pendiente', data.get('monto_mensual', 0))),
            pagado=data.get('pagado', False),
            fecha=data.get('fecha', '')
        )


@dataclass
class GastoReal(Gasto):
    """Gasto real registrado durante el mes"""
    presupuestado: Optional[float] = None
    es_imprevisto: bool = False
    
    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({
            "presupuestado": self.presupuestado,
            "es_imprevisto": self.es_imprevisto
        })
        return base
    
    @classmethod
    def from_dict(cls, data: dict) -> 'GastoReal':
        return cls(
            concepto=data['concepto'],
            categoria=Categoria.from_string(data['categoria']),
            monto=float(data['monto']),
            fecha=data.get('fecha', ''),
            presupuestado=data.get('presupuestado'),
            es_imprevisto=data.get('es_imprevisto', False),
            pagado=data.get('pagado', True)
        )