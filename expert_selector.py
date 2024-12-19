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
        btn_actualizar_por_id = QPushButton("Actualizar Candidato por ID")
        btn_actualizar_por_id.clicked.connect(self.actualizar_candidato_por_id)
        btn_eliminar_por_id = QPushButton("Eliminar Candidato por ID")
        btn_eliminar_por_id.clicked.connect(self.eliminar_candidato_por_id)

        candidatos_layout.addWidget(btn_ver_candidatos)
        candidatos_layout.addWidget(btn_agregar_candidato)
        candidatos_layout.addWidget(btn_actualizar_por_id)
        candidatos_layout.addWidget(btn_eliminar_por_id)
        candidatos_layout.addStretch(1)

        candidatos_widget.setLayout(candidatos_layout)
        self.stacked_widget.addWidget(candidatos_widget)

    def crear_seccion_proyectos(self):
        """Actualización del método existente para incluir botones de actualizar y eliminar"""
        proyectos_widget = QWidget()
        proyectos_layout = QVBoxLayout()

     # Botones de acciones de proyectos
        btn_ver_proyectos = QPushButton("Ver Proyectos")
        btn_ver_proyectos.clicked.connect(self.listar_proyectos)
        btn_agregar_proyecto = QPushButton("Agregar Proyecto")
        btn_agregar_proyecto.clicked.connect(self.agregar_proyecto)
        btn_actualizar_proyecto = QPushButton("Actualizar Proyecto por ID")
        btn_actualizar_proyecto.clicked.connect(self.actualizar_proyecto_por_id)
        btn_eliminar_proyecto = QPushButton("Eliminar Proyecto por ID")
        btn_eliminar_proyecto.clicked.connect(self.eliminar_proyecto_por_id)
        btn_ver_coincidencias = QPushButton("Ver Coincidencias")
       # btn_ver_coincidencias.clicked.connect(self.ver_coincidencias)

        proyectos_layout.addWidget(btn_ver_proyectos)
        proyectos_layout.addWidget(btn_agregar_proyecto)
        proyectos_layout.addWidget(btn_actualizar_proyecto)
        proyectos_layout.addWidget(btn_eliminar_proyecto)
      #  proyectos_layout.addWidget(btn_ver_coincidencias)
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
     tabla.setColumnCount(6)  # Added two columns for action buttons
     tabla.setHorizontalHeaderLabels([
        "Nombre", "Apellido", 
        "Idiomas", "Habilidades", "Salario", 
        "Ubicación", "Actualizar", "Eliminar"
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
     
    def actualizar_candidato(self, candidato):
    # Diálogo para actualizar candidato
        dialog = QDialog(self)
        dialog.setWindowTitle("Actualizar Candidato")
        dialog.setGeometry(250, 250, 500, 600)

        layout = QFormLayout()

    # Campos del formulario pre-poblados
        nombre = QLineEdit(candidato['nombre'])
        apellido = QLineEdit(candidato['apellido'])

    # Idiomas (múltiple selección)
        idiomas = QWidget()
        idiomas_layout = QVBoxLayout()
        idiomas_checks = []
        candidato_idiomas = candidato['idiomas'] if isinstance(candidato['idiomas'], list) else eval(candidato['idiomas'])
        for idioma in self.db_manager.obtener_idiomas():
            check = QCheckBox(idioma)
            check.setChecked(idioma in candidato_idiomas)
            idiomas_layout.addWidget(check)
            idiomas_checks.append(check)
        idiomas.setLayout(idiomas_layout)

    # Habilidades (múltiple selección)
        habilidades = QWidget()
        habilidades_layout = QVBoxLayout()
        habilidades_checks = []
        candidato_habilidades = candidato['habilidades'] if isinstance(candidato['habilidades'], list) else eval(candidato['habilidades'])
        for habilidad in self.db_manager.obtener_habilidades():
            check = QCheckBox(habilidad)
            check.setChecked(habilidad in candidato_habilidades)
            habilidades_layout.addWidget(check)
            habilidades_checks.append(check)
        habilidades.setLayout(habilidades_layout)

    # Preferencia salarial
        salario = QComboBox()
        salario.addItems(self.db_manager.obtener_salarios())
        salario.setCurrentText(str(candidato['preferencia_salarial']))

    # Ubicación
        ubicacion = QComboBox()
        ubicacion.addItems(self.db_manager.obtener_paises())
        ubicacion.setCurrentText(candidato['ubicacion'])

    # Botón actualizar
        btn_actualizar = QPushButton("Actualizar Candidato")
        btn_actualizar.clicked.connect(lambda: self.guardar_actualizacion_candidato(
            candidato['id'],
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
        layout.addRow(btn_actualizar)

        dialog.setLayout(layout)
        dialog.exec_()

    def guardar_actualizacion_candidato(self, id_candidato, nombre, apellido, idiomas, habilidades, salario, ubicacion, dialog):
    # Validar campos obligatorios
        if not nombre or not apellido:
           QMessageBox.warning(self, "Error", "Nombre y apellido son obligatorios")
           return

    # Preparar datos actualizados del candidato
        candidato_actualizado = {
            'id': id_candidato,
            'nombre': nombre,
            'apellido': apellido,
            'idiomas': idiomas,
            'habilidades': habilidades,
            'salario': salario,
            'ubicacion': ubicacion
        }

        try:
            self.db_manager.actualizar_candidato(candidato_actualizado)
            QMessageBox.information(self, "Éxito", "Candidato actualizado correctamente.")
            dialog.accept()
            self.listar_candidatos()  # Refrescar la lista
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar el candidato: {str(e)}")

    def actualizar_candidato_por_id(self):
    # Diálogo para ingresar ID
        dialog = QDialog(self)
        dialog.setWindowTitle("Actualizar Candidato por ID")
        dialog.setGeometry(250, 250, 300, 100)
    
        layout = QVBoxLayout()
    
     # Campo para ID
        id_input = QLineEdit()
        id_input.setPlaceholderText("Ingrese ID del candidato")
    
    # Botón buscar
        btn_buscar = QPushButton("Buscar y Actualizar")
        btn_buscar.clicked.connect(lambda: self.buscar_y_actualizar_candidato(id_input.text(), dialog))
    
        layout.addWidget(QLabel("ID del Candidato:"))
        layout.addWidget(id_input)
        layout.addWidget(btn_buscar)
    
        dialog.setLayout(layout)
        dialog.exec_()
 
    def buscar_y_actualizar_candidato(self, id_candidato, dialog_previo):
       try:
        # Validar que el ID sea un número
            if not id_candidato.isdigit():
                QMessageBox.warning(self, "Error", "Por favor ingrese un ID válido")
                return
            
        # Buscar candidato por ID
            candidato = self.db_manager.obtener_candidato_por_id(int(id_candidato))
        
            if candidato:
                dialog_previo.accept()  # Cerrar diálogo de búsqueda
                self.actualizar_candidato(candidato)  # Usar el método existente
            else:
                QMessageBox.warning(self, "Error", "No se encontró un candidato con ese ID")
            
       except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar candidato: {str(e)}")
    
    def eliminar_candidato_por_id(self):
    # Diálogo para ingresar ID
        dialog = QDialog(self)
        dialog.setWindowTitle("Eliminar Candidato por ID")
        dialog.setGeometry(250, 250, 300, 100)
    
        layout = QVBoxLayout()
    
    # Campo para ID
        id_input = QLineEdit()
        id_input.setPlaceholderText("Ingrese ID del candidato")
    
    # Botón eliminar
        btn_eliminar = QPushButton("Buscar y Eliminar")
        btn_eliminar.clicked.connect(lambda: self.buscar_y_eliminar_candidato(id_input.text(), dialog))
    
        layout.addWidget(QLabel("ID del Candidato:"))
        layout.addWidget(id_input)
        layout.addWidget(btn_eliminar)
    
        dialog.setLayout(layout)
        dialog.exec_()

    def buscar_y_eliminar_candidato(self, id_candidato, dialog):
        try:
        # Validar que el ID sea un número
            if not id_candidato.isdigit():
                QMessageBox.warning(self, "Error", "Por favor ingrese un ID válido")
                return
            
        # Buscar candidato por ID
            candidato = self.db_manager.obtener_candidato_por_id(int(id_candidato))
        
            if candidato:
            # Confirmar eliminación
                confirmacion = QMessageBox.question(
                    self,
                    "Confirmar Eliminación",
                    f"¿Está seguro de que desea eliminar al candidato {candidato['nombre']} {candidato['apellido']}?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
            
                if confirmacion == QMessageBox.Yes:
                    self.db_manager.eliminar_candidato(candidato['id'])
                    QMessageBox.information(self, "Éxito", "Candidato eliminado correctamente")
                    dialog.accept()
            else:
                QMessageBox.warning(self, "Error", "No se encontró un candidato con ese ID")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar candidato: {str(e)}")

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

    def actualizar_proyecto_por_id(self):
        """Diálogo para actualizar un proyecto existente"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Actualizar Proyecto por ID")
        dialog.setGeometry(250, 250, 300, 100)
    
        layout = QVBoxLayout()
    
    # Campo para ID
        id_input = QLineEdit()
        id_input.setPlaceholderText("Ingrese ID del proyecto")
    
    # Botón buscar
        btn_buscar = QPushButton("Buscar y Actualizar")
        btn_buscar.clicked.connect(lambda: self.buscar_y_actualizar_proyecto(id_input.text(), dialog))
    
        layout.addWidget(QLabel("ID del Proyecto:"))
        layout.addWidget(id_input)
        layout.addWidget(btn_buscar)
    
        dialog.setLayout(layout)
        dialog.exec_()

    def buscar_y_actualizar_proyecto(self, id_proyecto, dialog_previo):
        try:
            if not id_proyecto.isdigit():
                QMessageBox.warning(self, "Error", "Por favor ingrese un ID válido")
                return
            
            proyecto = self.db_manager.obtener_proyecto_por_id(int(id_proyecto))
        
            if proyecto:
                dialog_previo.accept()
                self.actualizar_proyecto(proyecto)
            else:
                QMessageBox.warning(self, "Error", "No se encontró un proyecto con ese ID")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar proyecto: {str(e)}")

    def actualizar_proyecto(self, proyecto):
        """Diálogo para actualizar los datos del proyecto"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Actualizar Proyecto")
        dialog.setGeometry(250, 250, 600, 700)

        layout = QFormLayout()

    # Campos del formulario pre-poblados
        nombre_empresa = QLineEdit(proyecto['nombre_empresa'])
        nombre_proyecto = QLineEdit(proyecto['nombre_proyecto'])
        descripcion = QTextEdit()
        descripcion.setText(proyecto['descripcion'])

    # Ubicación
        ubicacion = QComboBox()
        ubicacion.addItems(self.db_manager.obtener_paises())
        ubicacion.setCurrentText(proyecto['ubicacion'])

    # Idiomas requeridos
        idiomas = QWidget()
        idiomas_layout = QVBoxLayout()
        idiomas_checks = []
        for idioma in self.db_manager.obtener_idiomas():
            check = QCheckBox(idioma)
            check.setChecked(idioma in proyecto['idiomas_requeridos'])
            idiomas_layout.addWidget(check)
            idiomas_checks.append(check)
        idiomas.setLayout(idiomas_layout)

    # Habilidades requeridas
        habilidades = QWidget()
        habilidades_layout = QVBoxLayout()
        habilidades_checks = []
        for habilidad in self.db_manager.obtener_habilidades():
            check = QCheckBox(habilidad)
            check.setChecked(habilidad in proyecto['habilidades_requeridas'])
            habilidades_layout.addWidget(check)
            habilidades_checks.append(check)
        habilidades.setLayout(habilidades_layout)

    # Salario mínimo
        salario_minimo = QComboBox()
        salario_minimo.addItems(self.db_manager.obtener_salarios())
        salario_minimo.setCurrentText(proyecto['salario_minimo'])

    # Botón actualizar
        btn_actualizar = QPushButton("Actualizar Proyecto")
        btn_actualizar.clicked.connect(lambda: self.guardar_actualizacion_proyecto(
            proyecto['id'],
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
        layout.addRow("Descripción:", descripcion)
        layout.addRow("Ubicación:", ubicacion)
        layout.addRow("Idiomas Requeridos:", idiomas)
        layout.addRow("Habilidades Requeridas:", habilidades)
        layout.addRow("Salario Mínimo:", salario_minimo)
        layout.addRow(btn_actualizar)

        dialog.setLayout(layout)
        dialog.exec_()

    def guardar_actualizacion_proyecto(self, id_proyecto, nombre_empresa, nombre_proyecto, 
                                     descripcion, ubicacion, idiomas_requeridos, 
                                     habilidades_requeridas, salario_minimo, dialog):
        """Guarda la actualización de un proyecto"""
        if not nombre_empresa or not nombre_proyecto:
            QMessageBox.warning(self, "Error", "Nombre de empresa y proyecto son obligatorios")
            return
   
        proyecto_actualizado = {
            'id': id_proyecto,
            'nombre_empresa': nombre_empresa,
            'nombre_proyecto': nombre_proyecto,
            'descripcion': descripcion,
            'ubicacion': ubicacion,
            'idiomas_requeridos': idiomas_requeridos,
            'habilidades_requeridas': habilidades_requeridas,
            'salario_minimo': salario_minimo
        }

        try:
            self.db_manager.actualizar_proyecto(proyecto_actualizado)
            QMessageBox.information(self, "Éxito", "Proyecto actualizado correctamente.")
            dialog.accept()
            self.listar_proyectos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar el proyecto: {str(e)}")

    def eliminar_proyecto_por_id(self):
        """Diálogo para eliminar un proyecto"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Eliminar Proyecto por ID")
        dialog.setGeometry(250, 250, 300, 100)
      
        layout = QVBoxLayout()
    
    # Campo para ID
        id_input = QLineEdit()
        id_input.setPlaceholderText("Ingrese ID del proyecto")
    
    # Botón eliminar
        btn_eliminar = QPushButton("Buscar y Eliminar")
        btn_eliminar.clicked.connect(lambda: self.buscar_y_eliminar_proyecto(id_input.text(), dialog))
      
        layout.addWidget(QLabel("ID del Proyecto:"))
        layout.addWidget(id_input)
        layout.addWidget(btn_eliminar)
    
        dialog.setLayout(layout)
        dialog.exec_()

    def buscar_y_eliminar_proyecto(self, id_proyecto, dialog):
        """Busca y elimina un proyecto específico"""
        try:
            if not id_proyecto.isdigit():
                QMessageBox.warning(self, "Error", "Por favor ingrese un ID válido")
                return
            
            proyecto = self.db_manager.obtener_proyecto_por_id(int(id_proyecto))
        
            if proyecto:
                confirmacion = QMessageBox.question(
                    self,
                    "Confirmar Eliminación",
                    f"¿Está seguro de que desea eliminar el proyecto {proyecto['nombre_proyecto']} de la empresa {proyecto['nombre_empresa']} ?\n"
                    "Esta acción también eliminará todas las coincidencias asociadas.",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                
                if confirmacion == QMessageBox.Yes:
                    self.db_manager.eliminar_proyecto(proyecto['id'])
                    QMessageBox.information(self, "Éxito", "Proyecto eliminado correctamente")
                    dialog.accept()
            else:
                   QMessageBox.warning(self, "Error", "No se encontró un proyecto con ese ID")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar proyecto: {str(e)}")

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
        """Diálogo para agregar un nuevo proyecto"""
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
        btn_guardar = QPushButton("Guardar Proyecto")
        btn_guardar.clicked.connect(lambda: self.guardar_proyecto(
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

    def guardar_proyecto(self, 
                        nombre_empresa, 
                        nombre_proyecto, 
                        descripcion, 
                        ubicacion, 
                        idiomas_requeridos, 
                        habilidades_requeridas, 
                        salario_minimo, 
                        dialog):
        """Guarda el proyecto en la base de datos"""
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

        try:
          # Guardar proyecto en base de datos
            self.db_manager.guardar_proyecto(proyecto)
        
         # Mostrar mensaje de éxito
            QMessageBox.information(self, "Éxito", "Proyecto guardado correctamente.")
        
        # Cerrar diálogo
            dialog.accept()
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el proyecto: {str(e)}")
