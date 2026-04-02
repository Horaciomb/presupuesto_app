import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from pathlib import Path
from models import PresupuestoMensual

class GraficoService:
    def __init__(self, presupuesto: PresupuestoMensual):
        self.presupuesto = presupuesto
        self.output_dir = Path('graficos')
        self.output_dir.mkdir(exist_ok=True)
        
        # Configurar estilo
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
    
    def generar_grafico_distribucion(self):
        """Genera gráfico de distribución de gastos"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Datos
        categorias = ['Gastos Fijos', 'Gastos Variables', 'Deudas', 'Ahorro', 'Imprevistos']
        valores = [
            self.presupuesto.total_gastos_fijos,
            self.presupuesto.total_gastos_variables_planeados,
            self.presupuesto.total_deudas_mensual,
            self.presupuesto.ahorro_planeado,
            self.presupuesto.fondo_imprevistos
        ]
        
        # Gráfico de barras
        bars = ax1.bar(categorias, valores, edgecolor='black', linewidth=1.5)
        ax1.set_title('Distribución de Gastos', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Monto (Bs)', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        
        for bar, valor in zip(bars, valores):
            if valor > 0:
                ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                        f'{valor:.0f}', ha='center', va='bottom', fontsize=10)
        
        # Gráfico de pastel (solo valores > 0)
        valores_filtrados = [v for v in valores if v > 0]
        categorias_filtradas = [c for c, v in zip(categorias, valores) if v > 0]
        
        ax2.pie(valores_filtrados, labels=categorias_filtradas, autopct='%1.1f%%')
        ax2.set_title('Distribución Porcentual', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        fecha = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.output_dir / f'distribucion_{fecha}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(filename)
    
    def generar_grafico_evolucion(self):
        """Genera gráfico de evolución de gastos"""
        if not self.presupuesto.gastos_reales:
            return None
        
        # Agrupar gastos por día
        gastos_por_dia = {}
        for gasto in self.presupuesto.gastos_reales:
            fecha = gasto.fecha
            gastos_por_dia[fecha] = gastos_por_dia.get(fecha, 0) + gasto.monto
        
        fechas = sorted(gastos_por_dia.keys())
        montos = [gastos_por_dia[f] for f in fechas]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(fechas, montos, marker='o', linewidth=2, markersize=8)
        ax.fill_between(fechas, montos, alpha=0.3)
        
        # Línea de ingreso diario promedio
        ingreso_diario = self.presupuesto.ingreso_mensual / 30
        ax.axhline(y=ingreso_diario, color='red', linestyle='--', 
                  linewidth=1.5, label=f'Ingreso diario promedio ({ingreso_diario:.0f} Bs)')
        
        ax.set_xlabel('Fecha', fontsize=12)
        ax.set_ylabel('Monto gastado (Bs)', fontsize=12)
        ax.set_title('Evolución de Gastos Diarios', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        fecha = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.output_dir / f'evolucion_{fecha}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(filename)