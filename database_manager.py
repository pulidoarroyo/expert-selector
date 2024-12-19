import sqlite3
import json

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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_empresa TEXT,
            nombre_proyecto TEXT,
            descripcion TEXT,
            ubicacion TEXT,
            idiomas_requeridos TEXT,
            habilidades_requeridas TEXT,
            salario_minimo TEXT
        )
        ''')

        # Tabla de coincidencias
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

    def obtener_idiomas(self):
        """Devuelve una lista de idiomas predefinidos"""
        return ['Español', 'Inglés', 'Portugués', 'Francés', 'Alemán']

    def obtener_habilidades(self):
        """Devuelve una lista de habilidades predefinidas"""
        return ['Python', 'JavaScript', 'React', 'SQL', 'Java', 'C++', 'Data Science', 'Machine Learning']

    def obtener_salarios(self):
        """Devuelve rangos de salarios predefinidos"""
        return ['2000-3000', '3000-4000', '4000-5000', '5000-6000', '6000+']

    def obtener_paises(self):
        """Devuelve lista de países de Latinoamérica"""
        return ['Argentina', 'Brasil', 'Chile', 'Colombia', 'México', 'Perú', 'Uruguay','Venezuela','Estados Unidos']

    def guardar_candidato(self, candidato):
        """Guarda un nuevo candidato en la base de datos"""
        try:
            # Convertir listas a JSON strings
            idiomas_json = json.dumps(candidato.get('idiomas', []))
            habilidades_json = json.dumps(candidato.get('habilidades', []))

            self.cursor.execute('''
            INSERT INTO candidatos 
            (nombre, apellido, idiomas, habilidades, preferencia_salarial, ubicacion) 
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                candidato['nombre'], 
                candidato['apellido'], 
                idiomas_json,
                habilidades_json,
                candidato['salario'], 
               candidato['ubicacion']
            ))
            self.conn.commit()
            return self.cursor.lastrowid
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
            proyectos.append(proyecto)
        
        return proyectos
    
    def guardar_proyecto(self, proyecto):
        """Guarda un nuevo proyecto en la base de datos"""
        # Convertir listas de idiomas y habilidades a cadenas
        idiomas = ', '.join(proyecto.get('idiomas_requeridos', []))
        habilidades = ', '.join(proyecto.get('habilidades_requeridas', []))

        self.cursor.execute('''
        INSERT INTO proyectos 
        (nombre_empresa, nombre_proyecto, descripcion, ubicacion, 
        idiomas_requeridos, habilidades_requeridas, salario_minimo) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            proyecto['nombre_empresa'], 
            proyecto['nombre_proyecto'], 
            proyecto['descripcion'], 
            proyecto['ubicacion'], 
            idiomas, 
            habilidades, 
            proyecto['salario_minimo']
        ))
        self.conn.commit()
        return self.cursor.lastrowid
    
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
    

    def __del__(self):
        """Cierra la conexión a la base de datos"""
        self.conn.close()