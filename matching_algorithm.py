import sqlite3
from typing import List, Dict, Any
import json

class MatchingAlgorithm:
    def generar_coincidencias(self, proyecto_id, db_manager):
        """
        Genera coincidencias entre un proyecto y los candidatos disponibles
        
        :param proyecto_id: ID del proyecto a emparejar
        :param db_manager: Instancia de DatabaseManager para consultas
        :return: Lista de coincidencias
        """
        # Obtener detalles del proyecto
        proyecto = self._obtener_proyecto(proyecto_id, db_manager)
        
        # Obtener todos los candidatos
        candidatos = db_manager.listar_candidatos()
        
        # Lista para almacenar coincidencias
        coincidencias = []
        
        # Calcular coincidencias para cada candidato
        for candidato in candidatos:
            porcentaje_coincidencia = self._calcular_porcentaje_coincidencia(proyecto, candidato)
            
            # Solo incluir coincidencias que superen un umbral mínimo
            if porcentaje_coincidencia >= 50:  # Umbral personalizable
                detalles = {
                    'habilidades': self._obtener_habilidades_coincidentes(proyecto, candidato),
                    'idiomas': self._obtener_idiomas_coincidentes(proyecto, candidato)
                }
                
                coincidencia = {
                    'proyecto_id': proyecto_id,
                    'candidato_id': candidato['id'],
                    'nombre_candidato': f"{candidato['nombre']} {candidato['apellido']}",
                    'nombre_proyecto': proyecto['nombre_proyecto'],
                    'porcentaje_coincidencia': porcentaje_coincidencia,
                    'detalles': detalles
                }
                
                coincidencias.append(coincidencia)
        
        return coincidencias
    
    def _obtener_proyecto(self, proyecto_id, db_manager):
        """Obtiene los detalles de un proyecto específico"""
        proyectos = db_manager.listar_proyectos()
        return next((p for p in proyectos if p['id'] == proyecto_id), None)
    
    def _calcular_porcentaje_coincidencia(self, proyecto, candidato):
        """
        Calcula el porcentaje de coincidencia entre un proyecto y un candidato
        
        :param proyecto: Diccionario con detalles del proyecto
        :param candidato: Diccionario con detalles del candidato
        :return: Porcentaje de coincidencia (0-100)
        """
        # Dividir habilidades y convertir a conjuntos
        habilidades_proyecto = set(proyecto['habilidades_requeridas'].split(', '))
        habilidades_candidato = set(candidato['habilidades'].split(', '))
        
        # Dividir idiomas y convertir a conjuntos
        idiomas_proyecto = set(proyecto['idiomas_requeridos'].split(', '))
        idiomas_candidato = set(candidato['idiomas'].split(', '))
        
        # Calcular coincidencias
        habilidades_match = len(habilidades_proyecto.intersection(habilidades_candidato)) / len(habilidades_proyecto) * 100
        idiomas_match = len(idiomas_proyecto.intersection(idiomas_candidato)) / len(idiomas_proyecto) * 100
        
        # Ubicación
        ubicacion_match = 20 if proyecto['ubicacion'] == candidato['ubicacion'] else 0
        
        # Salario (aproximado)
        salario_proyecto = int(proyecto['salario_minimo'].split('-')[0])
        salario_candidato = int(candidato['preferencia_salarial'].split('-')[0])
        salario_match = max(0, 20 - abs(salario_proyecto - salario_candidato) / 100)
        
        # Calcular porcentaje total (peso diferente para cada factor)
        porcentaje_total = (
            habilidades_match * 0.4 +  # 40% para habilidades
            idiomas_match * 0.2 +       # 20% para idiomas
            ubicacion_match * 0.2 +     # 20% para ubicación
            salario_match * 0.2         # 20% para salario
        )
        
        return round(porcentaje_total, 2)
    
    def _obtener_habilidades_coincidentes(self, proyecto, candidato):
        """Obtiene las habilidades que coinciden entre proyecto y candidato"""
        habilidades_proyecto = set(proyecto['habilidades_requeridas'].split(', '))
        habilidades_candidato = set(candidato['habilidades'].split(', '))
        return list(habilidades_proyecto.intersection(habilidades_candidato))
    
    def _obtener_idiomas_coincidentes(self, proyecto, candidato):
        """Obtiene los idiomas que coinciden entre proyecto y candidato"""
        idiomas_proyecto = set(proyecto['idiomas_requeridos'].split(', '))
        idiomas_candidato = set(candidato['idiomas'].split(', '))
        return list(idiomas_proyecto.intersection(idiomas_candidato))