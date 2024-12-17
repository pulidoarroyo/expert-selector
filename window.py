import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QComboBox, QPushButton, QStackedWidget, 
    QTableWidget, QTableWidgetItem, QFormLayout, QCheckBox, QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from database_manager import DatabaseManager 

class ExpertSelector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Expert Selector")
        self.setGeometry(100, 100, 1000, 600)

        # Widget principal
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # Panel lateral de navegación
        nav_layout = QVBoxLayout()
        
        # Botones de navegación
        nav_buttons = [
            ("Candidatos", self.mostrar_candidatos),
            ("Proyectos", self.mostrar_proyectos)
        ]

        for texto, funcion in nav_buttons:
            btn = QPushButton(texto)
            btn.clicked.connect(funcion)
            nav_layout.addWidget(btn)

        nav_layout.addStretch(1)

        # Título principal
        titulo = QLabel("Expert Selector")
        titulo.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(24)
        titulo.setFont(font)

        # Contenedor de contenido
        self.stacked_widget = QStackedWidget()

        # Layouts de secciones
        self.crear_seccion_candidatos()
        self.crear_seccion_proyectos()

        # Layout principal
        main_layout.addLayout(nav_layout)
        
        content_layout = QVBoxLayout()
        content_layout.addWidget(titulo)
        content_layout.addWidget(self.stacked_widget)

        main_layout.addLayout(content_layout)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def crear_seccion_candidatos(self):
        # Página de candidatos
        candidatos_widget = QWidget()
        candidatos_layout = QVBoxLayout()

        # Botones de acciones de candidatos
        btn_ver_candidatos = QPushButton("Ver Candidatos")
        btn_ver_candidatos.clicked.connect(self.listar_candidatos)
        btn_agregar_candidato = QPushButton("Agregar Candidato")
        btn_agregar_candidato.clicked.connect(self.agregar_candidato)

        candidatos_layout.addWidget(btn_ver_candidatos)
        candidatos_layout.addWidget(btn_agregar_candidato)
        candidatos_layout.addStretch(1)

        candidatos_widget.setLayout(candidatos_layout)
        self.stacked_widget.addWidget(candidatos_widget)

    def crear_seccion_proyectos(self):
        # Página de proyectos
        proyectos_widget = QWidget()
        proyectos_layout = QVBoxLayout()

        # Botones de acciones de proyectos
        btn_ver_proyectos = QPushButton("Ver Proyectos")
        btn_ver_proyectos.clicked.connect(self.listar_proyectos)
        btn_agregar_proyecto = QPushButton("Agregar Proyecto")
        btn_agregar_proyecto.clicked.connect(self.agregar_proyecto)
        btn_ver_coincidencias = QPushButton("Ver Coincidencias")
        btn_ver_coincidencias.clicked.connect(self.ver_coincidencias)

        proyectos_layout.addWidget(btn_ver_proyectos)
        proyectos_layout.addWidget(btn_agregar_proyecto)
        proyectos_layout.addWidget(btn_ver_coincidencias)
        proyectos_layout.addStretch(1)

        proyectos_widget.setLayout(proyectos_layout)
        self.stacked_widget.addWidget(proyectos_widget)

    def mostrar_candidatos(self):
        self.stacked_widget.setCurrentIndex(0)

    def mostrar_proyectos(self):
        self.stacked_widget.setCurrentIndex(1)

    def listar_candidatos(self):
        # Diálogo para mostrar lista de candidatos
        dialog = QDialog(self)
        dialog.setWindowTitle("Lista de Candidatos")
        dialog.setGeometry(200, 200, 800, 500)

        layout = QVBoxLayout()
        tabla = QTableWidget()
        tabla.setColumnCount(7)
        tabla.setHorizontalHeaderLabels([
            "Nombre", "Apellido", "Idiomas", "Habilidades", 
            "Preferencia Salarial", "Ubicación", "Acciones"
        ])

        # Aquí iría la lógica para cargar candidatos desde la base de datos
        # Por ahora, un ejemplo de datos
        datos_ejemplo = [
            ["Juan", "Pérez", "Español, Inglés", "Python, SQL", "3000-4000", "Argentina", ""],
            ["María", "García", "Inglés", "React, JavaScript", "4000-5000", "México", ""]
        ]

        tabla.setRowCount(len(datos_ejemplo))
        for fila, datos in enumerate(datos_ejemplo):
            for columna, valor in enumerate(datos):
                tabla.setItem(fila, columna, QTableWidgetItem(valor))

        layout.addWidget(tabla)
        dialog.setLayout(layout)
        dialog.exec_()

    def agregar_candidato(self):
        # Diálogo para agregar candidato
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Candidato")
        dialog.setGeometry(250, 250, 500, 600)

        layout = QFormLayout()

        # Campos del formulario
        nombre = QLineEdit()
        apellido = QLineEdit()

        # Idiomas (múltiple selección)
        idiomas = QWidget()
        idiomas_layout = QVBoxLayout()
        idiomas_checks = []
        for idioma in self.db_manager.obtener_idiomas():
            check = QCheckBox(idioma)
            idiomas_layout.addWidget(check)
            idiomas_checks.append(check)
        idiomas.setLayout(idiomas_layout)

        # Habilidades (múltiple selección)
        habilidades = QWidget()
        habilidades_layout = QVBoxLayout()
        habilidades_checks = []
        for habilidad in self.db_manager.obtener_habilidades():
            check = QCheckBox(habilidad)
            habilidades_layout.addWidget(check)
            habilidades_checks.append(check)
        habilidades.setLayout(habilidades_layout)

        # Preferencia salarial
        salario = QComboBox()
        salario.addItems(self.db_manager.obtener_salarios())

        # Ubicación
        ubicacion = QComboBox()
        ubicacion.addItems(self.db_manager.obtener_paises())

        # Botón guardar
        btn_guardar = QPushButton("Guardar Candidato")

        # Agregar al layout
        layout.addRow("Nombre:", nombre)
        layout.addRow("Apellido:", apellido)
        layout.addRow("Idiomas:", idiomas)
        layout.addRow("Habilidades:", habilidades)
        layout.addRow("Preferencia Salarial:", salario)
        layout.addRow("Ubicación:", ubicacion)
        layout.addRow(btn_guardar)

        dialog.setLayout(layout)
        dialog.exec_()

    def listar_proyectos(self):
        # Similar a listar_candidatos, pero para proyectos
        pass

    def agregar_proyecto(self):
        # Similar a agregar_candidato, pero para proyectos
        pass

    def ver_coincidencias(self):
        # Diálogo para mostrar coincidencias
        pass

def main():
    app = QApplication(sys.argv)
    ventana = ExpertSelector()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()