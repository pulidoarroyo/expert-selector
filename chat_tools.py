from database_manager import DatabaseManager
from matching_algorithm import MatchingAlgorithm


def make_chat_tools(db_manager: DatabaseManager, matching_algorithm: MatchingAlgorithm):
    def _calcular_scores(proyecto: dict, candidato: dict):
        scores = {
            "idiomas": matching_algorithm.calcular_match_idiomas(
                proyecto.get("idiomas_requeridos", []),
                candidato.get("idiomas", []),
            ),
            "habilidades": matching_algorithm.calcular_match_habilidades(
                proyecto.get("habilidades_requeridas", []),
                candidato.get("habilidades", []),
            ),
            "ubicacion": matching_algorithm.calcular_match_ubicacion(
                proyecto.get("ubicacion", ""),
                candidato.get("ubicacion", ""),
            ),
            "salario": matching_algorithm.calcular_match_salario(
                proyecto.get("salario_minimo", ""),
                candidato.get("preferencia_salarial", ""),
            ),
        }

        score_total = sum(
            scores[key] * matching_algorithm.weights[key]
            for key in matching_algorithm.weights
        )

        return scores, score_total

    def _validar_matching():
        if matching_algorithm is None:
            return "MatchingAlgorithm no disponible"
        return None

    def list_candidatos():
        """Lista candidatos registrados.

        Args:
            None
        """
        candidatos = db_manager.listar_candidatos()
        return [
            {
                "id": c.get("id"),
                "nombre": c.get("nombre"),
                "apellido": c.get("apellido"),
                "ubicacion": c.get("ubicacion"),
                "idiomas": c.get("idiomas"),
                "habilidades": c.get("habilidades"),
                "preferencia_salarial": c.get("preferencia_salarial"),
            }
            for c in candidatos
        ]

    def list_proyectos():
        """Lista proyectos registrados.

        Args:
            None
        """
        proyectos = db_manager.listar_proyectos()
        return [
            {
                "id": p.get("id"),
                "nombre_empresa": p.get("nombre_empresa"),
                "nombre_proyecto": p.get("nombre_proyecto"),
                "descripcion": p.get("descripcion"),
                "ubicacion": p.get("ubicacion"),
                "idiomas_requeridos": p.get("idiomas_requeridos"),
                "habilidades_requeridas": p.get("habilidades_requeridas"),
                "salario_minimo": p.get("salario_minimo"),
            }
            for p in proyectos
        ]

    def get_candidato(id: int):
        """Obtiene un candidato por ID.

        Args:
            id: ID del candidato.
        """
        return db_manager.obtener_candidato_por_id(id)

    def get_proyecto(id: int):
        """Obtiene un proyecto por ID.

        Args:
            id: ID del proyecto.
        """
        return db_manager.obtener_proyecto_por_id(id)

    def get_coincidencias(proyecto_id: int):
        """Obtiene coincidencias por ID de proyecto.

        Args:
            proyecto_id: ID del proyecto.
        """
        return db_manager.obtener_coincidencias(proyecto_id)

    def buscar_candidatos_por_nombre(texto: str):
        """Busca candidatos por nombre o apellido (coincidencia parcial).

        Args:
            texto: Texto parcial a buscar en nombre o apellido.
        """
        query = (texto or "").strip().lower()
        if not query:
            return []

        candidatos = db_manager.listar_candidatos()
        resultados = []
        for candidato in candidatos:
            nombre = (candidato.get("nombre") or "").lower()
            apellido = (candidato.get("apellido") or "").lower()
            if query in nombre or query in apellido:
                resultados.append(
                    {
                        "id": candidato.get("id"),
                        "nombre": candidato.get("nombre"),
                        "apellido": candidato.get("apellido"),
                        "ubicacion": candidato.get("ubicacion"),
                    }
                )

        return resultados

    def buscar_proyectos_por_nombre(texto: str):
        """Busca proyectos por nombre de empresa o nombre del proyecto.

        Args:
            texto: Texto parcial a buscar en empresa o proyecto.
        """
        query = (texto or "").strip().lower()
        if not query:
            return []

        proyectos = db_manager.listar_proyectos()
        resultados = []
        for proyecto in proyectos:
            empresa = (proyecto.get("nombre_empresa") or "").lower()
            nombre = (proyecto.get("nombre_proyecto") or "").lower()
            if query in empresa or query in nombre:
                resultados.append(
                    {
                        "id": proyecto.get("id"),
                        "nombre_empresa": proyecto.get("nombre_empresa"),
                        "nombre_proyecto": proyecto.get("nombre_proyecto"),
                        "ubicacion": proyecto.get("ubicacion"),
                    }
                )

        return resultados

    def evaluar_candidato(
        proyecto_id: int,
        candidato_id: int,
        incluir_justificacion: bool = False,
    ):
        """Evalua un candidato frente a un proyecto y devuelve sus puntajes.

        Args:
            proyecto_id: ID del proyecto a evaluar.
            candidato_id: ID del candidato a evaluar.
            incluir_justificacion: Si se debe generar justificacion con IA.
        """
        error = _validar_matching()
        if error:
            return {"error": error}

        proyecto = db_manager.obtener_proyecto_por_id(proyecto_id)
        if not proyecto:
            return {"error": "Proyecto no encontrado"}

        candidato = db_manager.obtener_candidato_por_id(candidato_id)
        if not candidato:
            return {"error": "Candidato no encontrado"}

        scores, score_total = _calcular_scores(proyecto, candidato)

        resultado = {
            "proyecto_id": proyecto_id,
            "candidato_id": candidato_id,
            "porcentaje_match": round(score_total * 100, 2),
            "idiomas_match": list(
                set(proyecto.get("idiomas_requeridos", []))
                & set(candidato.get("idiomas", []))
            ),
            "habilidades_match": list(
                set(proyecto.get("habilidades_requeridas", []))
                & set(candidato.get("habilidades", []))
            ),
            "ubicacion_match": scores["ubicacion"] == 1.0,
            "salario_match": scores["salario"] == 1.0,
            "scores": {key: round(value * 100, 1) for key, value in scores.items()},
        }

        if incluir_justificacion:
            resultado["justificacion_ia"] = matching_algorithm.generar_justificacion(
                proyecto,
                candidato,
                scores,
                score_total,
            )

        return resultado

    def evaluar_proyecto(
        proyecto_id: int,
        limite: int = 5,
        incluir_justificacion: bool = False,
    ):
        """Evalua candidatos para un proyecto y devuelve un ranking.

        Args:
            proyecto_id: ID del proyecto a evaluar.
            limite: Maximo de resultados a devolver.
            incluir_justificacion: Si se debe generar justificacion con IA.
        """
        error = _validar_matching()
        if error:
            return {"error": error}

        proyecto = db_manager.obtener_proyecto_por_id(proyecto_id)
        if not proyecto:
            return {"error": "Proyecto no encontrado"}

        candidatos = db_manager.listar_candidatos()
        resultados = []
        for candidato in candidatos:
            scores, score_total = _calcular_scores(proyecto, candidato)
            resultados.append(
                {
                    "candidato_id": candidato.get("id"),
                    "nombre": candidato.get("nombre"),
                    "apellido": candidato.get("apellido"),
                    "porcentaje_match": round(score_total * 100, 2),
                    "scores": {
                        key: round(value * 100, 1) for key, value in scores.items()
                    },
                }
            )

        resultados.sort(key=lambda item: item["porcentaje_match"], reverse=True)
        top = resultados[: max(1, limite)]

        if incluir_justificacion:
            candidatos_map = {c.get("id"): c for c in candidatos}
            for entry in top:
                candidato = candidatos_map.get(entry.get("candidato_id"))
                if not candidato:
                    continue
                scores, score_total = _calcular_scores(proyecto, candidato)
                entry["justificacion_ia"] = matching_algorithm.generar_justificacion(
                    proyecto,
                    candidato,
                    scores,
                    score_total,
                )

        return {
            "proyecto_id": proyecto_id,
            "resultados": top,
        }

    return [
        list_candidatos,
        list_proyectos,
        get_candidato,
        get_proyecto,
        get_coincidencias,
        buscar_candidatos_por_nombre,
        buscar_proyectos_por_nombre,
        evaluar_candidato,
        evaluar_proyecto,
    ]
