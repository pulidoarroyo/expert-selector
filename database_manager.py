import sqlite3

class DatabaseManager:
    def __init__(self, db_name='expert_selector.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Tabla de idiomas predeterminados
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS idiomas (
            id INTEGER PRIMARY KEY,
            nombre TEXT UNIQUE
        )
        ''')

        # Tabla de habilidades predeterminadas
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS habilidades (
            id INTEGER PRIMARY KEY,
            nombre TEXT UNIQUE
        )
        ''')

        # Tabla de países de Latinoamérica
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS paises (
            id INTEGER PRIMARY KEY,
            nombre TEXT UNIQUE
        )
        ''')

        # Tabla de salarios predeterminados
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS salarios (
            id INTEGER PRIMARY KEY,
            rango TEXT UNIQUE
        )
        ''')

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

        # Tabla de coincidencias
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS coincidencias (
            id INTEGER PRIMARY KEY,
            nombre_candidato TEXT,
            nombre_proyecto TEXT,
            porcentaje_coincidencia REAL
        )
        ''')

        # Insertar datos predeterminados
        self.insertar_datos_predeterminados()
        self.conn.commit()

    def insertar_datos_predeterminados(self):
        # Idiomas
        idiomas = ['Español', 'Inglés', 'Portugués', 'Francés']
        for idioma in idiomas:
            self.cursor.execute('INSERT OR IGNORE INTO idiomas (nombre) VALUES (?)', (idioma,))

        # Habilidades
        habilidades = [
            'Python', 'JavaScript', 'React', 'SQL', 'Gestión de Proyectos', 
            'Diseño UX/UI', 'Marketing Digital', 'Machine Learning'
        ]
        for habilidad in habilidades:
            self.cursor.execute('INSERT OR IGNORE INTO habilidades (nombre) VALUES (?)', (habilidad,))

        # Países de Latinoamérica
        paises = [
            'Argentina', 'Bolivia', 'Brasil', 'Chile', 'Colombia', 
            'Costa Rica', 'Cuba', 'Ecuador', 'El Salvador', 'Guatemala', 
            'Honduras', 'México', 'Nicaragua', 'Panamá', 'Paraguay', 
            'Perú', 'República Dominicana', 'Uruguay', 'Venezuela'
        ]
        for pais in paises:
            self.cursor.execute('INSERT OR IGNORE INTO paises (nombre) VALUES (?)', (pais,))

        # Rangos salariales
        salarios = [
            '1000-2000', '2000-3000', '3000-4000', 
            '4000-5000', '5000-6000', '6000+'
        ]
        for salario in salarios:
            self.cursor.execute('INSERT OR IGNORE INTO salarios (rango) VALUES (?)', (salario,))

    def obtener_idiomas(self):
        self.cursor.execute('SELECT nombre FROM idiomas')
        return [idioma[0] for idioma in self.cursor.fetchall()]

    def obtener_habilidades(self):
        self.cursor.execute('SELECT nombre FROM habilidades')
        return [habilidad[0] for habilidad in self.cursor.fetchall()]

    def obtener_paises(self):
        self.cursor.execute('SELECT nombre FROM paises')
        return [pais[0] for pais in self.cursor.fetchall()]

    def obtener_salarios(self):
        self.cursor.execute('SELECT rango FROM salarios')
        return [salario[0] for salario in self.cursor.fetchall()]

    def close(self):
        self.conn.close()