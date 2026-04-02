from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from .gasto import GastoFijo, GastoVariable, GastoReal
from .deuda import Deuda

@dataclass
class PresupuestoMensual:
    ingreso_mensual: float
    mes: str
    gastos_fijos: List[GastoFijo] = field(default_factory=list)
    gastos_variables: List[GastoVariable] = field(default_factory=list)
    gastos_reales: List[GastoReal] = field(default_factory=list)
    deudas: List[Deuda] = field(default_factory=list)
    ahorro_planeado: float = 0.0
    fondo_imprevistos: float = 300.0
    nota: Optional[str] = None
    
    @property
    def total_gastos_fijos(self) -> float:
        return sum(g.monto for g in self.gastos_fijos if not g.pagado)
    
    @property
    def total_gastos_variables_planeados(self) -> float:
        return sum(g.monto for g in self.gastos_variables)
    
    @property
    def total_gastos_variables_pendientes(self) -> float:
        return sum(g.saldo_pendiente for g in self.gastos_variables)
    
    @property
    def total_deudas_mensual(self) -> float:
        return sum(d.cuota_mensual for d in self.deudas if not d.pagado)
    
    @property
    def total_gastos_reales(self) -> float:
        return sum(g.monto for g in self.gastos_reales)
    
    @property
    def total_imprevistos_gastados(self) -> float:
        return sum(g.monto for g in self.gastos_reales if g.es_imprevisto)
    
    @property
    def fondo_imprevistos_restante(self) -> float:
        return max(0, self.fondo_imprevistos - self.total_imprevistos_gastados)
    
    @property
    def total_gastos_pendientes(self) -> float:
        return (self.total_gastos_fijos + 
                self.total_gastos_variables_pendientes + 
                self.total_deudas_mensual)
    
    @property
    def ahorro_real(self) -> float:
        return (self.ingreso_mensual - 
                self.total_gastos_reales - 
                self.total_gastos_pendientes - 
                self.ahorro_planeado)
    
    @property
    def disponible(self) -> float:
        return self.ingreso_mensual - self.total_gastos_reales - self.total_gastos_pendientes
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "ingreso_mensual": self.ingreso_mensual,
            "mes": self.mes,
            "nota": self.nota,
            "gastos_fijos": [g.to_dict() for g in self.gastos_fijos],
            "gastos_variables": [g.to_dict() for g in self.gastos_variables],
            "gastos_reales": [g.to_dict() for g in self.gastos_reales],
            "deudas": [d.to_dict() for d in self.deudas],
            "ahorro_mensual": self.ahorro_planeado,
            "fondo_imprevistos": self.fondo_imprevistos
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PresupuestoMensual':
        # Convertir gastos_fijos asegurando tipo correcto
        gastos_fijos = []
        for g in data.get('gastos_fijos', []):
            gastos_fijos.append(GastoFijo.from_dict(g))
        
        # Convertir gastos_variables
        gastos_variables = []
        for g in data.get('gastos_variables', []):
            gastos_variables.append(GastoVariable.from_dict(g))
        
        # Convertir gastos_reales
        gastos_reales = []
        for g in data.get('gastos_reales', []):
            gastos_reales.append(GastoReal.from_dict(g))
        
        # Convertir deudas
        deudas = []
        for d in data.get('deudas', []):
            deudas.append(Deuda.from_dict(d))
        
        return cls(
            ingreso_mensual=float(data['ingreso_mensual']),
            mes=data.get('mes', 'Mes actual'),
            nota=data.get('nota'),
            gastos_fijos=gastos_fijos,
            gastos_variables=gastos_variables,
            gastos_reales=gastos_reales,
            deudas=deudas,
            ahorro_planeado=float(data.get('ahorro_mensual', 0)),
            fondo_imprevistos=float(data.get('fondo_imprevistos', 300))
        )