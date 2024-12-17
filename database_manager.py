import sqlite3
import json

class DatabaseManager:
    def __init__(self, db_path='expert_selector.db'):
        """Initialize database connection and create tables"""
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.crear_tablas()

    def crear_tablas(self):
        """Create necessary tables if they don't exist"""
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
        # Convertir listas de idiomas y habilidades a cadenas
        idiomas = ', '.join(candidato.get('idiomas', []))
        habilidades = ', '.join(candidato.get('habilidades', []))

        self.cursor.execute('''
        INSERT INTO candidatos 
        (nombre, apellido, idiomas, habilidades, preferencia_salarial, ubicacion) 
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            candidato['nombre'], 
            candidato['apellido'], 
            idiomas, 
            habilidades, 
            candidato['salario'], 
            candidato['ubicacion']
        ))
        self.conn.commit()
        return self.cursor.lastrowid

    def listar_candidatos(self):
   
        self.cursor.execute('''
            SELECT 
                nombre, 
                apellido, 
                idiomas, 
                habilidades, 
                preferencia_salarial, 
                ubicacion
            FROM candidatos
        ''')
        
        # Obtener los nombres de las columnas
        columnas = [column[0] for column in self.cursor.description]
        
        # Convertir resultados a lista de diccionarios
        candidatos = []
        for fila in self.cursor.fetchall():
            candidato = dict(zip(columnas, fila))
            candidatos.append(candidato)
        
        return candidatos
    
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

    def __del__(self):
        """Cierra la conexión a la base de datos"""
        self.conn.close()