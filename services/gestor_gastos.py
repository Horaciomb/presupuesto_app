from datetime import datetime
from typing import Optional, List, Dict, Any
from models import GastoReal, GastoVariable, Categoria, PresupuestoMensual

class GestorGastos:
    def __init__(self, presupuesto: PresupuestoMensual):
        self.presupuesto = presupuesto
    
    def registrar_gasto(self, concepto: str, categoria: str, monto: float, 
                        es_imprevisto: bool = False, fecha: Optional[str] = None) -> GastoReal:
        """Registra un gasto real"""
        
        # Si fecha es None, usar string vacío (se asignará en __post_init__)
        fecha_str = fecha if fecha is not None else ""
        
        cat = Categoria.from_string(categoria)
        
        nuevo_gasto = GastoReal(
            concepto=concepto,
            categoria=cat,
            monto=monto,
            fecha=fecha_str,
            es_imprevisto=es_imprevisto
        )
        
        # Buscar si existe un gasto variable similar para actualizar saldo pendiente
        self._actualizar_saldo_variable(concepto, monto)
        
        self.presupuesto.gastos_reales.append(nuevo_gasto)
        return nuevo_gasto
    
    def _actualizar_saldo_variable(self, concepto: str, monto: float):
        """Actualiza el saldo pendiente de un gasto variable"""
        for gasto in self.presupuesto.gastos_variables:
            if concepto.lower() in gasto.concepto.lower():
                gasto.monto_gastado += monto
                gasto.saldo_pendiente = max(0, gasto.monto - gasto.monto_gastado)
                if gasto.monto_gastado > gasto.monto:
                    excedente = gasto.monto_gastado - gasto.monto
                    print(f"⚠️  Excediste el presupuesto de '{concepto}' en {excedente:.2f} Bs")
                break
    
    def obtener_gastos_por_categoria(self) -> Dict[str, float]:
        """Obtiene gastos agrupados por categoría"""
        resultado: Dict[str, float] = {}
        for gasto in self.presupuesto.gastos_reales:
            cat = gasto.categoria.value
            resultado[cat] = resultado.get(cat, 0) + gasto.monto
        return resultado
    
    def obtener_gastos_imprevistos(self) -> List[GastoReal]:
        """Obtiene solo los gastos imprevistos"""
        return [g for g in self.presupuesto.gastos_reales if g.es_imprevisto]
    
    def obtener_gastos_por_dia(self) -> Dict[str, float]:
        """Obtiene gastos agrupados por día"""
        resultado: Dict[str, float] = {}
        for gasto in self.presupuesto.gastos_reales:
            fecha = gasto.fecha
            if fecha:
                resultado[fecha] = resultado.get(fecha, 0) + gasto.monto
        return resultado