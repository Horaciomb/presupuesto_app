from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Deuda:
    concepto: str
    monto_total: float
    cuotas: int
    cuotas_pagadas: int = 0
    cuota_mensual: float = 0.0
    pagado: bool = False
    
    def __post_init__(self):
        if self.cuota_mensual == 0 and self.cuotas > 0:
            self.cuota_mensual = self.monto_total / self.cuotas
    
    @property
    def cuotas_restantes(self) -> int:
        return self.cuotas - self.cuotas_pagadas
    
    @property
    def saldo_restante(self) -> float:
        return self.cuota_mensual * self.cuotas_restantes
    
    def pagar_cuota(self) -> bool:
        if self.cuotas_restantes > 0:
            self.cuotas_pagadas += 1
            if self.cuotas_restantes == 0:
                self.pagado = True
            return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "concepto": self.concepto,
            "monto_total": self.monto_total,
            "cuotas": self.cuotas,
            "cuotas_pagadas": self.cuotas_pagadas,
            "cuota_mensual": self.cuota_mensual,
            "cuotas_restantes": self.cuotas_restantes,
            "pagado": self.pagado
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Deuda':
        return cls(
            concepto=data['concepto'],
            monto_total=float(data['monto_total']),
            cuotas=int(data['cuotas']),
            cuotas_pagadas=int(data.get('cuotas_pagadas', 0)),
            cuota_mensual=float(data.get('cuota_mensual', 0)),
            pagado=data.get('pagado', False)
        )