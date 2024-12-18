import sys
import json
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QComboBox, QPushButton, QStackedWidget, 
    QTableWidget, QTableWidgetItem, QFormLayout, QCheckBox, QDialog, 
    QMessageBox, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from database_manager import DatabaseManager
from matching_algorithm import MatchingAlgorithm

# Metodos de la creación de la ventana, las vistas y la carga de datos desde la bd
class ExpertSelector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.matching_algorithm = MatchingAlgorithm()
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
     dialog.setWindowTitle("Lista de candidatos")
     dialog.setGeometry(200, 200, 900, 500)
 
     layout = QVBoxLayout()
     tabla = QTableWidget()
     tabla.setColumnCount(6)
     tabla.setHorizontalHeaderLabels([
        "Nombre", "Apellido", 
        "Idiomas", "Habilidades", "Salario", 
        "Ubicación"
    ])

    # Obtener candidatos desde la base de datos
     candidatos = self.db_manager.listar_candidatos()

     tabla.setRowCount(len(candidatos))
     for fila, candidato in enumerate(candidatos):
        tabla.setItem(fila, 0, QTableWidgetItem(str(candidato.get('nombre', ''))))
        tabla.setItem(fila, 1, QTableWidgetItem(str(candidato.get('apellido', ''))))
        tabla.setItem(fila, 2, QTableWidgetItem(str(candidato.get('idiomas', ''))))
        tabla.setItem(fila, 3, QTableWidgetItem(str(candidato.get('habilidades', ''))))
        tabla.setItem(fila, 4, QTableWidgetItem(str(candidato.get('preferencia_salarial', ''))))
        tabla.setItem(fila, 5, QTableWidgetItem(str(candidato.get('ubicacion', ''))))

    # Hacer que la tabla sea editable y expandible
     tabla.resizeColumnsToContents()
     tabla.setSortingEnabled(True)

     layout.addWidget(tabla)
     dialog.setLayout(layout)
     dialog.exec_()   
    
        
    def listar_proyectos(self):
    # Diálogo para mostrar lista de proyectos
     dialog = QDialog(self)
     dialog.setWindowTitle("Lista de Proyectos")
     dialog.setGeometry(200, 200, 900, 500)
 
     layout = QVBoxLayout()
     tabla = QTableWidget()
     tabla.setColumnCount(7)
     tabla.setHorizontalHeaderLabels([
        "Empresa", "Nombre Proyecto", "Descripción", 
        "Ubicación", "Idiomas Requeridos", "Habilidades Requeridas", 
        "Salario Mínimo"
    ])

    # Obtener proyectos desde la base de datos
     proyectos = self.db_manager.listar_proyectos()

     tabla.setRowCount(len(proyectos))
     for fila, proyecto in enumerate(proyectos):
        tabla.setItem(fila, 0, QTableWidgetItem(str(proyecto.get('nombre_empresa', ''))))
        tabla.setItem(fila, 1, QTableWidgetItem(str(proyecto.get('nombre_proyecto', ''))))
        tabla.setItem(fila, 2, QTableWidgetItem(str(proyecto.get('descripcion', ''))))
        tabla.setItem(fila, 3, QTableWidgetItem(str(proyecto.get('ubicacion', ''))))
        tabla.setItem(fila, 4, QTableWidgetItem(str(proyecto.get('idiomas_requeridos', ''))))
        tabla.setItem(fila, 5, QTableWidgetItem(str(proyecto.get('habilidades_requeridas', ''))))
        tabla.setItem(fila, 6, QTableWidgetItem(str(proyecto.get('salario_minimo', ''))))

    # Hacer que la tabla sea editable y expandible
     tabla.resizeColumnsToContents()
     tabla.setSortingEnabled(True)

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
        btn_guardar.clicked.connect(lambda: self.guardar_candidato(
        nombre.text(), 
        apellido.text(), 
        [check.text() for check in idiomas_checks if check.isChecked()],
        [check.text() for check in habilidades_checks if check.isChecked()],
        salario.currentText(), 
        ubicacion.currentText(),
        dialog
        ))

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

    def guardar_candidato(self, nombre, apellido, idiomas, habilidades, salario, ubicacion, dialog):
    # Validar campos obligatorios
      if not nombre or not apellido:
        QMessageBox.warning(self, "Error", "Nombre y apellido son obligatorios")
        return

    # Preparar datos del candidato
      candidato = {
        'nombre': nombre,
        'apellido': apellido,
        'idiomas': idiomas,
        'habilidades': habilidades,
        'salario': salario,
        'ubicacion': ubicacion
    }

    # Guardar candidato en base de datos
      try:
        self.db_manager.guardar_candidato(candidato)
        QMessageBox.information(self, "Éxito", "Candidato guardado correctamente.")
        dialog.accept()
      except Exception as e:
        QMessageBox.critical(self, "Error", f"No se pudo guardar el candidato: {str(e)}")

    def agregar_proyecto(self):
        """Diálogo para agregar un nuevo proyecto con generación de coincidencias"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Proyecto")
        dialog.setGeometry(250, 250, 600, 700)

        layout = QFormLayout()

        # Campos del formulario
        nombre_empresa = QLineEdit()
        nombre_proyecto = QLineEdit()
        descripcion = QTextEdit()

        # Ubicación (países de Latinoamérica)
        ubicacion = QComboBox()
        ubicacion.addItems(self.db_manager.obtener_paises())

        # Idiomas requeridos (múltiple selección)
        idiomas = QWidget()
        idiomas_layout = QVBoxLayout()
        idiomas_checks = []
        for idioma in self.db_manager.obtener_idiomas():
            check = QCheckBox(idioma)
            idiomas_layout.addWidget(check)
            idiomas_checks.append(check)
        idiomas.setLayout(idiomas_layout)

        # Habilidades requeridas (múltiple selección)
        habilidades = QWidget()
        habilidades_layout = QVBoxLayout()
        habilidades_checks = []
        for habilidad in self.db_manager.obtener_habilidades():
            check = QCheckBox(habilidad)
            habilidades_layout.addWidget(check)
            habilidades_checks.append(check)
        habilidades.setLayout(habilidades_layout)

        # Salario mínimo
        salario_minimo = QComboBox()
        salario_minimo.addItems(self.db_manager.obtener_salarios())

        # Botón guardar
        btn_guardar = QPushButton("Guardar Proyecto y Generar Coincidencias")
        btn_guardar.clicked.connect(lambda: self.guardar_proyecto_y_generar_coincidencias(
            nombre_empresa.text(),
            nombre_proyecto.text(),
            descripcion.toPlainText(),
            ubicacion.currentText(),
            [check.text() for check in idiomas_checks if check.isChecked()],
            [check.text() for check in habilidades_checks if check.isChecked()],
            salario_minimo.currentText(),
            dialog
        ))

        # Agregar al layout
        layout.addRow("Nombre de la Empresa:", nombre_empresa)
        layout.addRow("Nombre del Proyecto:", nombre_proyecto)
        layout.addRow("Descripción del Proyecto:", descripcion)
        layout.addRow("Ubicación:", ubicacion)
        layout.addRow("Idiomas Requeridos:", idiomas)
        layout.addRow("Habilidades Requeridas:", habilidades)
        layout.addRow("Salario Mínimo:", salario_minimo)
        layout.addRow(btn_guardar)

        dialog.setLayout(layout)
        dialog.exec_()

    def guardar_proyecto_y_generar_coincidencias(self, 
                                                 nombre_empresa, 
                                                 nombre_proyecto, 
                                                 descripcion, 
                                                 ubicacion, 
                                                 idiomas_requeridos, 
                                                 habilidades_requeridas, 
                                                 salario_minimo, 
                                                 dialog):
        """Guarda el proyecto y genera coincidencias automáticamente"""
        # Validar campos obligatorios
        if not nombre_empresa or not nombre_proyecto:
            QMessageBox.warning(self, "Error", "Nombre de empresa y proyecto son obligatorios")
            return

        # Preparar datos del proyecto
        proyecto = {
            'nombre_empresa': nombre_empresa,
            'nombre_proyecto': nombre_proyecto,
            'descripcion': descripcion,
            'ubicacion': ubicacion,
            'idiomas_requeridos': idiomas_requeridos,
            'habilidades_requeridas': habilidades_requeridas,
            'salario_minimo': salario_minimo
        }

        # Guardar proyecto en base de datos
        proyecto_id = self.db_manager.guardar_proyecto(proyecto)

        # Generar coincidencias
        try:
            coincidencias = self.matching_algorithm.generar_coincidencias(proyecto_id)
            
            # Guardar coincidencias
            self.db_manager.guardar_coincidencias(coincidencias)

            # Mostrar mensaje de éxito
            QMessageBox.information(self, "Éxito", 
                f"Proyecto guardado. Se encontraron {len(coincidencias)} coincidencias.")

            # Cerrar diálogo
            dialog.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron generar coincidencias: {str(e)}")

    def ver_coincidencias(self):
        """Diálogo para seleccionar y mostrar coincidencias de proyectos"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Coincidencias de Proyectos")
        dialog.setGeometry(250, 250, 800, 600)

        layout = QVBoxLayout()

        # Selector de proyectos
        proyectos_combo = QComboBox()
        self.cursor.execute('SELECT id, nombre_proyecto FROM proyectos')
        proyectos = self.cursor.fetchall()
        proyectos_combo.addItems([p[1] for p in proyectos])

        # Tabla de coincidencias
        tabla_coincidencias = QTableWidget()
        tabla_coincidencias.setColumnCount(5)
        tabla_coincidencias.setHorizontalHeaderLabels([
            "Candidato", "Proyecto", "% Coincidencia", 
            "Habilidades", "Idiomas"
        ])

        # Función para cargar coincidencias
        def cargar_coincidencias():
            # Obtener ID del proyecto seleccionado
            proyecto_seleccionado = proyectos[proyectos_combo.currentIndex()][0]
            
            # Obtener coincidencias
            coincidencias = self.db_manager.obtener_coincidencias_proyecto(proyecto_seleccionado)
            
            # Llenar tabla
            tabla_coincidencias.setRowCount(len(coincidencias))
            for fila, coincidencia in enumerate(coincidencias):
                tabla_coincidencias.setItem(fila, 0, QTableWidgetItem(coincidencia['nombre_candidato']))
                tabla_coincidencias.setItem(fila, 1, QTableWidgetItem(coincidencia['nombre_proyecto']))
                tabla_coincidencias.setItem(fila, 2, QTableWidgetItem(str(coincidencia['porcentaje_coincidencia'])))
                tabla_coincidencias.setItem(fila, 3, QTableWidgetItem(str(coincidencia['detalles']['habilidades'])))
                tabla_coincidencias.setItem(fila, 4, QTableWidgetItem(str(coincidencia['detalles']['idiomas'])))

        proyectos_combo.currentIndexChanged.connect(cargar_coincidencias)

        # Agregar widgets al layout
        layout.addWidget(QLabel("Seleccionar Proyecto:"))
        layout.addWidget(proyectos_combo)
        layout.addWidget(tabla_coincidencias)

        dialog.setLayout(layout)
        dialog.exec_()