from services import GestorPresupuesto, ReporteService, GraficoService
from services.gestor_gastos import GestorGastos
from models import Categoria


def main():
    print("🚀 Sistema de Gestión de Presupuesto v2.0")
    print("="*50)
    
    # Inicializar gestor principal
    gestor = GestorPresupuesto()
    
    if gestor.presupuesto is None:
        print("❌ Error al cargar presupuesto")
        return
    
    # Inicializar servicios
    reporte_service = ReporteService(gestor.presupuesto)
    grafico_service = GraficoService(gestor.presupuesto)
    gastos_service = GestorGastos(gestor.presupuesto)
    
    while True:
        print("\n📋 MENÚ PRINCIPAL")
        print("="*40)
        print("1. Ver reporte completo")
        print("2. Registrar gasto")
        print("3. Ver resumen rápido")
        print("4. Generar gráficos")
        print("5. Actualizar ingreso (mes atípico)")
        print("6. Actualizar ahorro mensual")
        print("7. Salir")
        print("="*40)
        
        opcion = input("\nSelecciona una opción (1-7): ").strip()
        
        if opcion == '1':
            print(reporte_service.generar_reporte_completo())
            
        elif opcion == '2':
            print("\n📝 REGISTRAR GASTO")
            concepto = input("Concepto: ")
            # Categoria.listar() ya retorna strings, no necesitas .value
            categorias_disponibles = Categoria.listar()
            print("Categorías disponibles:", ", ".join(categorias_disponibles))
            categoria = input("Categoría: ")
            try:
                monto = float(input("Monto (Bs): "))
                es_imprevisto = input("¿Es imprevisto? (s/n): ").lower() == 's'
                
                gasto = gastos_service.registrar_gasto(concepto, categoria, monto, es_imprevisto)
                gestor.guardar()
                print(f"✅ Gasto registrado: {gasto.concepto} - {gasto.monto:.2f} Bs")
                
                # Mostrar resumen después de registrar
                resumen = gestor.obtener_resumen()
                if resumen:
                    print(f"\n📊 Resumen actual: Te quedan {resumen['disponible']:.2f} Bs disponibles")
                
            except ValueError:
                print("❌ Monto inválido")
                
        elif opcion == '3':
            resumen = gestor.obtener_resumen()
            if resumen:
                print("\n📊 RESUMEN RÁPIDO")
                print("-"*30)
                print(f"Ingreso: {resumen['ingreso']:,.0f} Bs")
                print(f"Gastado: {resumen['gastado']:.2f} Bs")
                print(f"Por gastar: {resumen['pendiente']:.2f} Bs")
                print(f"Disponible: {resumen['disponible']:.2f} Bs")
                print(f"Ahorro planeado: {resumen['ahorro_planeado']:.0f} Bs")
                print(f"Fondo imprevistos restante: {resumen['fondo_restante']:.2f} Bs")
            else:
                print("❌ No se pudo obtener el resumen")
            
        elif opcion == '4':
            print("\n🎨 Generando gráficos...")
            dist_file = grafico_service.generar_grafico_distribucion()
            if dist_file:
                print(f"✅ Gráfico de distribución: {dist_file}")
            
            evol_file = grafico_service.generar_grafico_evolucion()
            if evol_file:
                print(f"✅ Gráfico de evolución: {evol_file}")
            else:
                print("⚠️ No hay suficientes gastos para gráfico de evolución")
                
        elif opcion == '5':
            try:
                nuevo_ingreso = float(input("Ingreso de este mes (Bs): "))
                mes = input("Nombre del mes (opcional): ").strip()
                nota = input("Nota (ej: sueldo prorrateado): ").strip()
                gestor.actualizar_ingreso(
                    nuevo_ingreso, 
                    mes if mes else None, 
                    nota if nota else None
                )
                print(f"✅ Ingreso actualizado a {nuevo_ingreso:,.0f} Bs")
            except ValueError:
                print("❌ Monto inválido")
                
        elif opcion == '6':
            try:
                nuevo_ahorro = float(input("Nuevo ahorro mensual (Bs): "))
                gestor.actualizar_ahorro(nuevo_ahorro)
                print(f"✅ Ahorro actualizado a {nuevo_ahorro:,.0f} Bs")
            except ValueError:
                print("❌ Monto inválido")
                
        elif opcion == '7':
            print("👋 ¡Hasta luego!")
            break
            
        else:
            print("❌ Opción no válida")


if __name__ == "__main__":
    main()