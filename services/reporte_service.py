from models import PresupuestoMensual
from .gestor_gastos import GestorGastos

class ReporteService:
    def __init__(self, presupuesto: PresupuestoMensual):
        self.presupuesto = presupuesto
        self.gestor_gastos = GestorGastos(presupuesto)
    
    def generar_reporte_completo(self) -> str:
        resumen = self._obtener_resumen()
        
        reporte = []
        reporte.append("="*60)
        reporte.append("REPORTE DE PRESUPUESTO MENSUAL")
        reporte.append(f"Mes: {self.presupuesto.mes}")
        if self.presupuesto.nota:
            reporte.append(f"Nota: {self.presupuesto.nota}")
        reporte.append("="*60)
        
        reporte.append(f"\n📊 INGRESO TOTAL: {self.presupuesto.ingreso_mensual:,.0f} Bs")
        
        # Gastos fijos
        reporte.append("\n📌 GASTOS FIJOS:")
        for gasto in self.presupuesto.gastos_fijos:
            estado = "✅" if gasto.pagado else "⏳"
            reporte.append(f"   {estado} {gasto.concepto}: {gasto.monto:,.0f} Bs ({gasto.categoria.value})")
        reporte.append(f"   TOTAL FIJOS: {self.presupuesto.total_gastos_fijos:,.0f} Bs")
        
        # Gastos variables
        reporte.append("\n🔄 GASTOS VARIABLES:")
        for gasto in self.presupuesto.gastos_variables:
            reporte.append(f"   • {gasto.concepto}: {gasto.monto:,.0f} Bs ({gasto.categoria.value})")
            if gasto.monto_gastado > 0:
                reporte.append(f"     └ Gastado: {gasto.monto_gastado:.2f} Bs | Restante: {gasto.saldo_pendiente:.2f} Bs")
        reporte.append(f"   TOTAL VARIABLES PLANEADOS: {self.presupuesto.total_gastos_variables_planeados:,.0f} Bs")
        
        # Deudas (solo una vez, no repetido)
        reporte.append("\n💸 DEUDAS:")
        for deuda in self.presupuesto.deudas:
            reporte.append(f"   • {deuda.concepto}: {deuda.cuota_mensual:,.0f} Bs (Restan {deuda.cuotas_restantes} cuotas)")
        reporte.append(f"   TOTAL DEUDAS MENSUAL: {self.presupuesto.total_deudas_mensual:,.0f} Bs")
        
        # Gastos reales
        if self.presupuesto.gastos_reales:
            reporte.append("\n📝 GASTOS REGISTRADOS:")
            for gasto in self.presupuesto.gastos_reales:
                imprevisto = "⚠️ " if gasto.es_imprevisto else "   "
                reporte.append(f"   {imprevisto}{gasto.fecha} - {gasto.concepto}: {gasto.monto:.2f} Bs")
        
        # Resumen financiero
        reporte.append(f"\n💰 AHORRO PLANEADO: {self.presupuesto.ahorro_planeado:,.0f} Bs")
        reporte.append(f"⚠️  FONDO IMPREVISTOS: {self.presupuesto.fondo_imprevistos:,.0f} Bs")
        reporte.append(f"   └ Gastado: {self.presupuesto.total_imprevistos_gastados:.2f} Bs")
        reporte.append(f"   └ Restante: {self.presupuesto.fondo_imprevistos_restante:.2f} Bs")
        
        reporte.append(f"\n📉 TOTAL GASTADO REAL: {self.presupuesto.total_gastos_reales:,.2f} Bs")
        reporte.append(f"📋 TOTAL POR GASTAR: {self.presupuesto.total_gastos_pendientes:,.2f} Bs")
        reporte.append(f"💰 DISPONIBLE: {resumen['disponible']:.2f} Bs")
        reporte.append(f"💪 AHORRO REAL DEL MES: {self.presupuesto.ahorro_real:.2f} Bs")
        
        if self.presupuesto.ahorro_real >= 0:
            reporte.append("\n✅ ESTADO: Presupuesto balanceado")
        else:
            reporte.append("\n⚠️ ESTADO: Presupuesto en déficit")
        
        reporte.append("="*60)
        
        return "\n".join(reporte)
    
    def _obtener_resumen(self) -> dict:
        return {
            'ingreso': self.presupuesto.ingreso_mensual,
            'gastado': self.presupuesto.total_gastos_reales,
            'pendiente': self.presupuesto.total_gastos_pendientes,
            'disponible': self.presupuesto.disponible
        }