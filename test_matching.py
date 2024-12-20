import sqlite3
from database_manager import DatabaseManager
from matching_algorithm import MatchingAlgorithm

def test_matching():
    # Inicializar managers
    db = DatabaseManager('expert_selector.db')
    matching = MatchingAlgorithm()
    
    try:
        # 1. Verificar y mostrar proyecto de prueba
        proyecto_id = 1  # Usaremos el proyecto con ID 1 para la prueba
        proyecto = db.obtener_proyecto_por_id(proyecto_id)
        
        print("\n=== Proyecto de prueba ===")
        print(f"ID: {proyecto['id']}")
        print(f"Empresa: {proyecto['nombre_empresa']}")
        print(f"Proyecto: {proyecto['nombre_proyecto']}")
        print(f"Idiomas requeridos: {proyecto['idiomas_requeridos']}")
        print(f"Habilidades requeridas: {proyecto['habilidades_requeridas']}")
        print(f"Ubicación: {proyecto['ubicacion']}")
        print(f"Salario mínimo: {proyecto['salario_minimo']}")
        
        # 2. Verificar candidatos disponibles
        candidatos = db.listar_candidatos()
        print(f"\n=== Candidatos disponibles: {len(candidatos)} ===")
        for candidato in candidatos[:3]:  # Mostrar solo los primeros 3 para no saturar
            print(f"\nID: {candidato['id']}")
            print(f"Nombre: {candidato['nombre']} {candidato['apellido']}")
            print(f"Idiomas: {candidato['idiomas']}")
            print(f"Habilidades: {candidato['habilidades']}")
        
        # 3. Generar coincidencias
        coincidencias = matching.generar_coincidencias(proyecto, candidatos)
        
        # 4. Guardar coincidencias
        db.guardar_coincidencias(proyecto_id, coincidencias)
        
        # 5. Verificar coincidencias guardadas
        coincidencias_guardadas = db.obtener_coincidencias(proyecto_id)
        print(f"\n=== Coincidencias generadas: {len(coincidencias_guardadas)} ===")
        
        # Mostrar las 3 mejores coincidencias
        for coincidencia in coincidencias_guardadas[:3]:
            print(f"\nCandidato ID: {coincidencia['id_candidato']}")
            print(f"Nombre: {coincidencia['nombre']} {coincidencia['apellido']}")
            print(f"Porcentaje de match: {coincidencia['porcentaje_match']}%")
            
            # Mostrar detalles si están disponibles
            if 'detalles' in coincidencia:
                detalles = coincidencia['detalles']
                if isinstance(detalles, dict):
                    print("Detalles del match:")
                    if 'idiomas_match' in detalles:
                        print(f"- Idiomas coincidentes: {detalles['idiomas_match']}")
                    if 'habilidades_match' in detalles:
                        print(f"- Habilidades coincidentes: {detalles['habilidades_match']}")
        
        return True
        
    except Exception as e:
        print(f"Error durante la prueba: {str(e)}")
        return False

if __name__ == "__main__":
    resultado = test_matching()
    print(f"\nResultado de la prueba: {'Éxito' if resultado else 'Falló'}")