from typing import Optional, Dict, Any
from models import PresupuestoMensual, GastoFijo, GastoVariable, GastoReal, Deuda, Categoria
from utils import FileManager

class GestorPresupuesto:
    def __init__(self, json_path: str = 'data/presupuesto.json'):
        self.file_manager = FileManager(json_path)
        self.presupuesto: Optional[PresupuestoMensual] = None
        self.cargar_presupuesto()
    
    def cargar_presupuesto(self):
        data = self.file_manager.cargar()
        if data:
            self.presupuesto = PresupuestoMensual.from_dict(data)
        else:
            self.crear_presupuesto_base()
    
    def crear_presupuesto_base(self):
        self.presupuesto = PresupuestoMensual(
            ingreso_mensual=5200.0,
            mes="Mes actual",
            ahorro_planeado=1000.0,
            fondo_imprevistos=300.0
        )
        self.guardar()
    
    def guardar(self):
        if self.presupuesto:
            self.file_manager.guardar(self.presupuesto.to_dict())
    
    def actualizar_ingreso(self, nuevo_ingreso: float, mes: Optional[str] = None, nota: Optional[str] = None):
        if self.presupuesto:
            self.presupuesto.ingreso_mensual = nuevo_ingreso
            if mes:
                self.presupuesto.mes = mes
            if nota:
                self.presupuesto.nota = nota
            self.guardar()
    
    def actualizar_ahorro(self, nuevo_ahorro: float):
        if self.presupuesto:
            self.presupuesto.ahorro_planeado = nuevo_ahorro
            self.guardar()
    
    def obtener_resumen(self) -> Dict[str, float]:
        if self.presupuesto:
            return {
                'ingreso': self.presupuesto.ingreso_mensual,
                'gastado': self.presupuesto.total_gastos_reales,
                'pendiente': self.presupuesto.total_gastos_pendientes,
                'disponible': self.presupuesto.disponible,
                'ahorro_planeado': self.presupuesto.ahorro_planeado,
                'ahorro_real': self.presupuesto.ahorro_real,
                'fondo_imprevistos': self.presupuesto.fondo_imprevistos,
                'fondo_restante': self.presupuesto.fondo_imprevistos_restante
            }
        return {}