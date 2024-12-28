import sqlite3
import json
import random

class DatabaseManager:
    def __init__(self, db_path='expert_selector.db'):
        """Inicializa conexión con la db y crea tablas"""
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.crear_tablas()

    def crear_tablas(self):
        """Crea tablas si no existen"""
        # Tabla de candidatos
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidatos (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            apellido TEXT,
            idiomas TEXT,
            habilidades TEXT,
            preferencia_salarial TEXT,
            ubicacion TEXT
        )
        ''')

        # Tabla de proyectos
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY,
            nombre_empresa TEXT,
            nombre_proyecto TEXT,
            descripcion TEXT,
            ubicacion TEXT,
            idiomas_requeridos TEXT,
            habilidades_requeridas TEXT,
            salario_minimo TEXT
        )
        ''')

        # Tabla de coincidencias con la estructura corregida
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS coincidencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proyecto_id INTEGER,
            candidato_id INTEGER,
            porcentaje_coincidencia REAL,
            detalles TEXT,
            FOREIGN KEY(proyecto_id) REFERENCES proyectos(id),
            FOREIGN KEY(candidato_id) REFERENCES candidatos(id)
        )
        ''')
        self.conn.commit()

    def generar_id(self):
            """Genera un ID único de 6 dígitos"""
            base = random.randint(100000, 999999)
            # Verifica que el ID no exista ya en ninguna tabla
            while True:
             # Verificar en todas las tablas
                self.cursor.execute("SELECT 1 FROM candidatos WHERE id = ?", (base,))
                if self.cursor.fetchone():
                    base = random.randint(100000, 999999)
                    continue
                
                self.cursor.execute("SELECT 1 FROM proyectos WHERE id = ?", (base,))
                if self.cursor.fetchone():
                    base = random.randint(100000, 999999)
                    continue
                
                self.cursor.execute("SELECT 1 FROM coincidencias WHERE id = ?", (base,))
                if self.cursor.fetchone():
                    base = random.randint(100000, 999999)
                    continue
                
                return base

    def obtener_idiomas(self):
        """Devuelve una lista de idiomas predefinidos"""
        return ['Español', 'Inglés', 'Portugués', 'Francés', 'Alemán']

    def obtener_habilidades(self):
        """Devuelve una lista de habilidades predefinidas"""
        return [
            'Python', 'JavaScript', 'React', 'SQL', 'Java', 'C++', 'C', 'C#', 'Ciencia de datos', 
            'Machine Learning','HTML', 'Blockchain', 'Cyberseguridad', 'Diseño UI', 'Manejo de proyectos',
            'Análisis de datos', 'Inteligencia Artificial', 'Desarrollo móvil', 'Desarrollo web',
            'Bases de datos', 'Administración de sistemas','Big Data', 'Gestión de equipos', 'Automatización'
        ]

    def obtener_salarios(self):
        """Devuelve rangos de salarios predefinidos"""
        return [
            '2000-3000', '3000-4000', '4000-5000', '5000-6000', '6000-7000', 
            '7000-8000', '8000-9000', '9000-10000', '10000+'
        ]

    def obtener_paises(self):
        """Devuelve lista de países de Latinoamérica y otros"""
        return [
            'Argentina', 'Brasil', 'Chile', 'Colombia', 'México', 'Perú', 'Uruguay', 
            'Venezuela', 'Estados Unidos', 'Canadá', 'España', 'Portugal', 'Alemania', 
            'Francia', 'Reino Unido', 'Italia', 'Australia', 'Nueva Zelanda', 'India', 
            'China', 'Japón', 'Corea del Sur', 'Sudáfrica'
        ]

    def guardar_candidato(self, candidato):
        """Guarda un nuevo candidato en la base de datos"""
        try:
            id_candidato = self.generar_id()
            # Convertir listas a JSON strings
            idiomas_json = json.dumps(candidato.get('idiomas', []))
            habilidades_json = json.dumps(candidato.get('habilidades', []))

            self.cursor.execute('''
            INSERT INTO candidatos 
            (id, nombre, apellido, idiomas, habilidades, preferencia_salarial, ubicacion) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                id_candidato,
                candidato['nombre'], 
                candidato['apellido'], 
                idiomas_json,
                habilidades_json,
                candidato['salario'], 
               candidato['ubicacion']
            ))
            self.conn.commit()
            return id_candidato
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error al guardar candidato: {str(e)}")

    def obtener_candidato_por_id(self, id_candidato):
        try:
            self.cursor.execute('''
                SELECT id, nombre, apellido, idiomas, habilidades, 
                       preferencia_salarial, ubicacion 
                FROM candidatos 
                WHERE id = ?
            ''', (id_candidato,))
        
            candidato = self.cursor.fetchone()
        
            if candidato:
            # Convertir strings JSON a listas
                try:
                    idiomas = json.loads(candidato[3]) if candidato[3] else []
                    habilidades = json.loads(candidato[4]) if candidato[4] else []
                except json.JSONDecodeError:
                    # Si no es JSON válido, asumimos que es string separado por comas
                    idiomas = [x.strip() for x in candidato[3].split(',')] if candidato[3] else []
                    habilidades = [x.strip() for x in candidato[4].split(',')] if candidato[4] else []
            
                return {
                    'id': candidato[0],
                    'nombre': candidato[1],
                    'apellido': candidato[2],
                    'idiomas': idiomas,
                    'habilidades': habilidades,
                    'preferencia_salarial': candidato[5],
                    'ubicacion': candidato[6]
                }
            return None
        
        except sqlite3.Error as e:
            raise Exception(f"Error en la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error al obtener candidato: {str(e)}")

    def listar_candidatos(self):
        try:
            self.cursor.execute('''
                SELECT 
                    id,
                    nombre, 
                    apellido, 
                    idiomas, 
                    habilidades, 
                    preferencia_salarial as preferencia_salarial, 
                    ubicacion
                FROM candidatos
            ''')
        
        # Obtener los nombres de las columnas
            columnas = [column[0] for column in self.cursor.description]
        
        # Convertir resultados a lista de diccionarios
            candidatos = []
            for fila in self.cursor.fetchall():
                candidato = dict(zip(columnas, fila))
            
            # Convertir strings JSON a listas
                try:
                   candidato['idiomas'] = json.loads(candidato['idiomas']) if candidato['idiomas'] else []
                   candidato['habilidades'] = json.loads(candidato['habilidades']) if candidato['habilidades'] else []
                except json.JSONDecodeError:
                # Si no es JSON válido, asumimos que es string separado por comas
                    candidato['idiomas'] = [x.strip() for x in candidato['idiomas'].split(',')] if candidato['idiomas'] else []
                    candidato['habilidades'] = [x.strip() for x in candidato['habilidades'].split(',')] if candidato['habilidades'] else []
            
                candidatos.append(candidato)
          
            return candidatos
        except Exception as e:
            raise Exception(f"Error al listar candidatos: {str(e)}")
     
    def actualizar_candidato(self, candidato):
        """Actualiza un candidato existente en la base de datos"""
        try:
            self.cursor.execute("""
                UPDATE candidatos 
                SET nombre = ?, apellido = ?, idiomas = ?, habilidades = ?, 
                    preferencia_salarial = ?, ubicacion = ?
                WHERE id = ?
            """, (
                candidato['nombre'],
                candidato['apellido'],
                json.dumps(candidato['idiomas']),
                json.dumps(candidato['habilidades']),
                candidato['salario'],
                candidato['ubicacion'],
                candidato['id']
            ))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def eliminar_candidato(self, id_candidato):
        """Elimina un candidato de la base de datos"""
        try:
            self.cursor.execute("DELETE FROM candidatos WHERE id = ?", (id_candidato,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def listar_proyectos(self):
        self.cursor.execute('''
            SELECT 
                id,
                nombre_empresa, 
                nombre_proyecto, 
                descripcion, 
                ubicacion, 
                idiomas_requeridos, 
                habilidades_requeridas, 
                salario_minimo 
            FROM proyectos
        ''')
    
        # Obtener los nombres de las columnas
        columnas = [column[0] for column in self.cursor.description]
    
        # Convertir resultados a lista de diccionarios
        proyectos = []
        for fila in self.cursor.fetchall():
            proyecto = dict(zip(columnas, fila))
        
            # Convertir strings de idiomas y habilidades a listas
            try:
                proyecto['idiomas_requeridos'] = proyecto['idiomas_requeridos'].split(', ') if proyecto['idiomas_requeridos'] else []
                proyecto['habilidades_requeridas'] = proyecto['habilidades_requeridas'].split(', ') if proyecto['habilidades_requeridas'] else []
            except AttributeError:
                proyecto['idiomas_requeridos'] = []
                proyecto['habilidades_requeridas'] = []
            
            proyectos.append(proyecto)
    
        return proyectos
    
    def guardar_proyecto(self, proyecto):
        """Guarda un nuevo proyecto en la base de datos"""
        try:
            id_proyecto = self.generar_id()
            # Convertir listas de idiomas y habilidades a cadenas
            idiomas = ', '.join(proyecto.get('idiomas_requeridos', []))
            habilidades = ', '.join(proyecto.get('habilidades_requeridas', []))

            self.cursor.execute('''
            INSERT INTO proyectos 
            (id, nombre_empresa, nombre_proyecto, descripcion, ubicacion, 
            idiomas_requeridos, habilidades_requeridas, salario_minimo) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                id_proyecto,
                proyecto['nombre_empresa'], 
                proyecto['nombre_proyecto'], 
                proyecto['descripcion'], 
                proyecto['ubicacion'], 
                idiomas, 
                habilidades, 
                proyecto['salario_minimo']
            ))
            self.conn.commit()
            return id_proyecto
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error al guardar proyecto: {str(e)}")
        
    def obtener_proyecto_por_id(self, id_proyecto):
        """Obtiene un proyecto específico por su ID"""
        try:
            self.cursor.execute('''
                SELECT id, nombre_empresa, nombre_proyecto, descripcion, 
                       ubicacion, idiomas_requeridos, habilidades_requeridas, 
                       salario_minimo 
                FROM proyectos 
                WHERE id = ?
            ''', (id_proyecto,))
    
            proyecto = self.cursor.fetchone()
    
            if proyecto:
                try:
                    idiomas = proyecto[5].split(', ') if proyecto[5] else []
                    habilidades = proyecto[6].split(', ') if proyecto[6] else []
                except AttributeError:
                    idiomas = []
                    habilidades = []
            
                return {
                    'id': proyecto[0],
                    'nombre_empresa': proyecto[1],
                    'nombre_proyecto': proyecto[2],
                    'descripcion': proyecto[3],
                    'ubicacion': proyecto[4],
                    'idiomas_requeridos': idiomas,
                    'habilidades_requeridas': habilidades,
                    'salario_minimo': proyecto[7]
                }
            return None
    
        except sqlite3.Error as e:
            raise Exception(f"Error en la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error al obtener proyecto: {str(e)}")

    def actualizar_proyecto(self, proyecto):
        """Actualiza un proyecto existente en la base de datos"""
        try:
          # Convertir listas a strings
            idiomas = ', '.join(proyecto['idiomas_requeridos'])
            habilidades = ', '.join(proyecto['habilidades_requeridas'])
        
            self.cursor.execute("""
                UPDATE proyectos 
                SET nombre_empresa = ?, 
                    nombre_proyecto = ?, 
                    descripcion = ?, 
                    ubicacion = ?, 
                    idiomas_requeridos = ?, 
                    habilidades_requeridas = ?, 
                    salario_minimo = ?
                WHERE id = ?
            """, (
                proyecto['nombre_empresa'],
                proyecto['nombre_proyecto'],
                proyecto['descripcion'],
                proyecto['ubicacion'],
                idiomas,
                habilidades,
                proyecto['salario_minimo'],
                proyecto['id']
            ))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def eliminar_proyecto(self, id_proyecto):
        """Elimina un proyecto de la base de datos"""
        try:
            # Primero eliminar las coincidencias asociadas
            self.cursor.execute("DELETE FROM coincidencias WHERE proyecto_id = ?", (id_proyecto,))
            # Luego eliminar el proyecto
            self.cursor.execute("DELETE FROM proyectos WHERE id = ?", (id_proyecto,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
    
    def guardar_coincidencias(self, proyecto_id, coincidencias):
        """
        Guarda las coincidencias generadas para un proyecto específico
        Args:
            proyecto_id (int): ID del proyecto
            coincidencias (list): Lista de diccionarios con las coincidencias
        """
        try:
            # Primero eliminamos coincidencias existentes para este proyecto
            self.cursor.execute("DELETE FROM coincidencias WHERE proyecto_id = ?", (proyecto_id,))
    
            # Insertar las nuevas coincidencias
            for coincidencia in coincidencias:
                detalles = json.dumps({
                    'idiomas_match': coincidencia.get('idiomas_match', []),
                    'habilidades_match': coincidencia.get('habilidades_match', []),
                    'ubicacion_match': coincidencia.get('ubicacion_match', False),
                    'salario_match': coincidencia.get('salario_match', False)
            })
        
                self.cursor.execute('''
                    INSERT INTO coincidencias 
                    (proyecto_id, candidato_id, porcentaje_coincidencia, detalles)
                    VALUES (?, ?, ?, ?)
            ''', (
                    proyecto_id,
                    coincidencia['id_candidato'],
                    coincidencia['porcentaje_match'],
                    detalles
                ))
    
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error al guardar coincidencias: {str(e)}")
        
    def obtener_coincidencias(self, proyecto_id):
        """
        Obtiene las coincidencias para un proyecto específico
    
        Args:
            proyecto_id (int): ID del proyecto
        
        Returns:
            list: Lista de diccionarios con las coincidencias y detalles de los candidatos
        """
        try:
            self.cursor.execute('''
                    SELECT 
                    c.id,
                    c.candidato_id as id_candidato,
                    ca.nombre,
                    ca.apellido,
                    c.porcentaje_coincidencia as porcentaje_match,
                    ca.idiomas,
                    ca.habilidades,
                    ca.ubicacion,
                    c.detalles
                FROM coincidencias c
                JOIN candidatos ca ON c.candidato_id = ca.id
                WHERE c.proyecto_id = ?
                ORDER BY c.porcentaje_coincidencia DESC
            ''', (proyecto_id,))
        
         # Obtener los nombres de las columnas
            columnas = [column[0] for column in self.cursor.description]
        
         # Convertir resultados a lista de diccionarios
            coincidencias = []
            for fila in self.cursor.fetchall():
                coincidencia = dict(zip(columnas, fila))
            
             # Convertir strings JSON a listas
                try:
                    coincidencia['idiomas'] = json.loads(coincidencia['idiomas']) if coincidencia['idiomas'] else []
                    coincidencia['habilidades'] = json.loads(coincidencia['habilidades']) if coincidencia['habilidades'] else []
                    coincidencia['detalles'] = json.loads(coincidencia['detalles']) if coincidencia['detalles'] else {}
                except json.JSONDecodeError:
                 # Si no es JSON válido, asumimos que es string separado por comas
                    coincidencia['idiomas'] = [x.strip() for x in coincidencia['idiomas'].split(',')] if coincidencia['idiomas'] else []
                    coincidencia['habilidades'] = [x.strip() for x in coincidencia['habilidades'].split(',')] if coincidencia['habilidades'] else []
                    coincidencia['detalles'] = {}
            
                coincidencias.append(coincidencia)
        
            return coincidencias
        except Exception as e:
            raise Exception(f"Error al obtener coincidencias: {str(e)}")
    
    def __del__(self):
        """Cierra la conexión a la base de datos"""
        self.conn.close()