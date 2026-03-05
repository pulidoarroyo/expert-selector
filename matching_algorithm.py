from urllib import response

import google.generativeai as genai

class MatchingAlgorithm:
    def __init__(self, gemini_api_key: str = None):
        """Inicializar pesos para diferentes criterios de coincidencia"""
        self.weights = {
            'idiomas': 0.15,
            'habilidades': 0.6,
            'ubicacion': 0.10,
            'salario': 0.15
        }

        if gemini_api_key:
            genai.configure(api_key=gemini_api_key)
            self.model = genai.GenerativeModel("gemini-2.5-flash")
            self.ia_activa = True
        else:
            self.model = None
            self.ia_activa = False

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
        return 0.5

    def calcular_match_salario(self, salario_minimo_proyecto, preferencia_salarial_candidato):
        """Calcula coincidencia de salario basada en preferencias del candidato"""
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

    def generar_justificacion(self, proyecto, candidato, scores: dict, score_total: float) -> str:
        """
        Genera un párrafo en lenguaje natural explicando por qué el candidato
        encaja o no con el proyecto. Solo se llama si la IA está activa.
        """
        if not self.ia_activa:
            return ""

        prompt = f"""Eres un consultor de recursos humanos especializado en tecnología.
Redacta un párrafo corto (máximo 5 oraciones) en español, dirigido a un reclutador,
explicando por qué el candidato es o no adecuado para el proyecto.
Sé objetivo, profesional y menciona tu punto de vista.  
Devuelve ÚNICAMENTE el párrafo, sin títulos ni formato adicional.

Proyecto: {proyecto.get('nombre', 'Sin nombre')}
Habilidades requeridas: {proyecto.get('habilidades_requeridas', [])}
Idiomas requeridos: {proyecto.get('idiomas_requeridos', [])}
Ubicación: {proyecto.get('ubicacion', 'No especificada')}
Salario mínimo: {proyecto.get('salario_minimo', 'No especificado')}

Candidato ID: {candidato.get('id', 'N/A')}
Habilidades: {candidato.get('habilidades', [])}
Idiomas: {candidato.get('idiomas', [])}
Ubicación: {candidato.get('ubicacion', 'No especificada')}
Preferencia salarial: {candidato.get('preferencia_salarial', 'No especificada')}

Puntuaciones:
- Habilidades: {round(scores['habilidades'] * 100, 1)}%
- Idiomas: {round(scores['idiomas'] * 100, 1)}%
- Ubicación: {round(scores['ubicacion'] * 100, 1)}%
- Salario: {round(scores['salario'] * 100, 1)}%
- Score total: {round(score_total * 100, 1)}%"""

        response = self.model.generate_content(prompt)
        
        return response.text.strip()

    def generar_coincidencias(self, proyecto, candidatos):
        """Genera coincidencias para un proyecto y una lista de candidatos"""
        coincidencias = []

        for candidato in candidatos:
            scores = {
                'idiomas': self.calcular_match_idiomas(
                    proyecto.get('idiomas_requeridos', []),
                    candidato.get('idiomas', [])
                ),
                'habilidades': self.calcular_match_habilidades(
                    proyecto.get('habilidades_requeridas', []),
                    candidato.get('habilidades', [])
                ),
                'ubicacion': self.calcular_match_ubicacion(
                    proyecto.get('ubicacion', ''),
                    candidato.get('ubicacion', '')
                ),
                'salario': self.calcular_match_salario(
                    proyecto.get('salario_minimo', ''),
                    candidato.get('preferencia_salarial', '')
                ),
            }

            score_total = sum(scores[k] * self.weights[k] for k in self.weights)

            coincidencia = {
                'id_candidato': candidato['id'],
                'porcentaje_match': round(score_total * 100, 2),
                'idiomas_match': list(set(proyecto.get('idiomas_requeridos', [])) &
                                    set(candidato.get('idiomas', []))),
                'habilidades_match': list(set(proyecto.get('habilidades_requeridas', [])) &
                                        set(candidato.get('habilidades', []))),
                'ubicacion_match': scores['ubicacion'] == 1.0,
                'salario_match': scores['salario'] == 1.0,
                'justificacion_ia': '',
                '_scores': scores,  # temporal para usar abajo
            }

            coincidencias.append(coincidencia)

        # Ordenar primero sin llamar a la IA
        coincidencias.sort(key=lambda x: x['porcentaje_match'], reverse=True)

        # Generar justificación solo para los top 5
        candidatos_dict = {c['id']: c for c in candidatos}
        for coincidencia in coincidencias[:3]:
            candidato = candidatos_dict[coincidencia['id_candidato']]
            scores = coincidencia.pop('_scores')
            coincidencia['justificacion_ia'] = self.generar_justificacion(
                proyecto, candidato, scores,
                coincidencia['porcentaje_match'] / 100
            )

        # Limpiar _scores de los que no entraron al top 5
        for coincidencia in coincidencias[5:]:
            coincidencia.pop('_scores', None)

        return coincidencias

    def obtener_mejores_coincidencias(self, coincidencias, limite=10):
        """Devuelve las mejores coincidencias hasta el límite especificado"""
        return coincidencias[:limite]