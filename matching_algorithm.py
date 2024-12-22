from typing import List, Dict, Any

class MatchingAlgorithm:
    def __init__(self):
        """Inicializar pesos para diferentes criterios de coincidencia"""
        self.weights = {
            'idiomas': 0.3,        # 30% de peso para coincidencias de idioma
            'habilidades': 0.4,    # 40% de peso para coincidencias de habilidades
            'ubicacion': 0.15,     # 15% de peso para la ubicación
            'salario': 0.15        # 15% de peso para expectativas salariales
        }
        
    def calcular_match_idiomas(self, idiomas_requeridos, idiomas_candidato):
        """Calcular porcentaje de coincidencia de idiomas"""
        if not idiomas_requeridos or not idiomas_candidato:
            return 0
            
        idiomas_requeridos = set(idiomas_requeridos)
        idiomas_candidato = set(idiomas_candidato)
        
        if not idiomas_requeridos:
            return 1.0
            
        matches = idiomas_requeridos.intersection(idiomas_candidato)
        return len(matches) / len(idiomas_requeridos)
        
    def calcular_match_habilidades(self, habilidades_requeridas, habilidades_candidato):
        """Calcular porcentaje de coincidencia de habilidades"""
        if not habilidades_requeridas or not habilidades_candidato:
            return 0
            
        habilidades_requeridas = set(habilidades_requeridas)
        habilidades_candidato = set(habilidades_candidato)
        
        if not habilidades_requeridas:
            return 1.0
            
        matches = habilidades_requeridas.intersection(habilidades_candidato)
        return len(matches) / len(habilidades_requeridas)

    def calcular_match_ubicacion(self, ubicacion_proyecto, ubicacion_candidato):
        """Calcular coincidencia de ubicación"""
        if not ubicacion_proyecto or not ubicacion_candidato:
            return 0
            
        if ubicacion_proyecto.lower() == ubicacion_candidato.lower():
            return 1.0
        return 0.5  # Trabajar de forma remota es posible pero no ideal
        
    def calcular_match_salario(self, salario_minimo_proyecto, preferencia_salarial_candidato):
        """Calculate salary match"""
        if not salario_minimo_proyecto or not preferencia_salarial_candidato:
            return 0
            
        def extract_min_salary(salary_range):
            try:
                if isinstance(salary_range, (int, float)):
                    return float(salary_range)
                return float(salary_range.split('-')[0])
            except (ValueError, IndexError, AttributeError):
                if isinstance(salary_range, str) and salary_range.endswith('+'):
                    return float(salary_range[:-1])
                return 0
                
        min_proyecto = extract_min_salary(salario_minimo_proyecto)
        min_candidato = extract_min_salary(preferencia_salarial_candidato)
        
        if min_candidato >= min_proyecto:
            return 1.0
        
        ratio = min_candidato / min_proyecto if min_proyecto > 0 else 0
        return max(0, min(1, ratio))
        
    def generar_coincidencias(self, proyecto, candidatos):
        """Generate matches between a project and candidates"""
        coincidencias = []
        
        for candidato in candidatos:
            # Calcular coincidencias para cada candidato
            match_idiomas = self.calcular_match_idiomas(
                proyecto.get('idiomas_requeridos', []),
                candidato.get('idiomas', [])
            )
            
            match_habilidades = self.calcular_match_habilidades(
                proyecto.get('habilidades_requeridas', []),
                candidato.get('habilidades', [])
            )
            
            match_ubicacion = self.calcular_match_ubicacion(
                proyecto.get('ubicacion', ''),
                candidato.get('ubicacion', '')
            )
            
            match_salario = self.calcular_match_salario(
                proyecto.get('salario_minimo', ''),
                candidato.get('preferencia_salarial', '')
            )
            
            # Calcular puntaje total basado en pesos
            score_total = (
                match_idiomas * self.weights['idiomas'] +
                match_habilidades * self.weights['habilidades'] +
                match_ubicacion * self.weights['ubicacion'] +
                match_salario * self.weights['salario']
            )
            
            # Crear objeto de coincidencia
            coincidencia = {
                'id_candidato': candidato['id'],
                'porcentaje_match': round(score_total * 100, 2),
                'idiomas_match': list(set(proyecto.get('idiomas_requeridos', [])) & 
                                    set(candidato.get('idiomas', []))),
                'habilidades_match': list(set(proyecto.get('habilidades_requeridas', [])) & 
                                        set(candidato.get('habilidades', []))),
                'ubicacion_match': match_ubicacion == 1.0,
                'salario_match': match_salario == 1.0
            }
            
            coincidencias.append(coincidencia)
        
        # Ordenar coincidencias por puntaje de coincidencia
        coincidencias.sort(key=lambda x: x['porcentaje_match'], reverse=True)
        
        return coincidencias

    def obtener_mejores_coincidencias(self, coincidencias, limite=10):
        """Return top N matches"""
        return coincidencias[:limite]