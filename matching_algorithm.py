import sqlite3
from typing import List, Dict, Any
import json

class MatchingAlgorithm:
    def __init__(self):
        """Initialize weights for different matching criteria"""
        self.weights = {
            'idiomas': 0.3,        # 30% weight for language matches
            'habilidades': 0.4,    # 40% weight for skill matches
            'ubicacion': 0.15,     # 15% weight for location
            'salario': 0.15        # 15% weight for salary expectations
        }
        
    def calcular_match_idiomas(self, idiomas_requeridos, idiomas_candidato):
        """Calculate language match percentage"""
        if not idiomas_requeridos or not idiomas_candidato:
            return 0
            
        idiomas_requeridos = set(idiomas_requeridos)
        idiomas_candidato = set(idiomas_candidato)
        
        if not idiomas_requeridos:
            return 1.0
            
        matches = idiomas_requeridos.intersection(idiomas_candidato)
        return len(matches) / len(idiomas_requeridos)
        
    def calcular_match_habilidades(self, habilidades_requeridas, habilidades_candidato):
        """Calculate skills match percentage"""
        if not habilidades_requeridas or not habilidades_candidato:
            return 0
            
        habilidades_requeridas = set(habilidades_requeridas)
        habilidades_candidato = set(habilidades_candidato)
        
        if not habilidades_requeridas:
            return 1.0
            
        matches = habilidades_requeridas.intersection(habilidades_candidato)
        return len(matches) / len(habilidades_requeridas)

    def calcular_match_ubicacion(self, ubicacion_proyecto, ubicacion_candidato):
        """Calculate location match"""
        if not ubicacion_proyecto or not ubicacion_candidato:
            return 0
            
        if ubicacion_proyecto.lower() == ubicacion_candidato.lower():
            return 1.0
        return 0.5  # Assuming remote work is possible but not ideal
        
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
            # Calculate individual matches
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
            
            # Calculate total score
            score_total = (
                match_idiomas * self.weights['idiomas'] +
                match_habilidades * self.weights['habilidades'] +
                match_ubicacion * self.weights['ubicacion'] +
                match_salario * self.weights['salario']
            )
            
            # Create match record with required fields for database
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
        
        # Sort matches by score
        coincidencias.sort(key=lambda x: x['porcentaje_match'], reverse=True)
        
        return coincidencias

    def obtener_mejores_coincidencias(self, coincidencias, limite=10):
        """Return top N matches"""
        return coincidencias[:limite]