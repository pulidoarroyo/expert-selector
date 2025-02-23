from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QComboBox, QPushButton, QStackedWidget, 
    QTableWidget, QTableWidgetItem, QFormLayout, QCheckBox, QDialog, 
    QMessageBox, QTextEdit, QScrollArea, QFrame, QTabWidget, QGridLayout, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from database_manager import DatabaseManager
from matching_algorithm import MatchingAlgorithm
from modern_style import ModernStyle

class ExpertSelector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.matching_algorithm = MatchingAlgorithm()
        
        self.setWindowIcon(QIcon('icon.png'))
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Expert Selector")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(f"background-color: {ModernStyle.BACKGROUND_COLOR};")

        # Widget principal
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Panel lateral de navegación
        nav_panel = QFrame()
        nav_panel.setStyleSheet(f"""
            QFrame {{
                background-color: {ModernStyle.CARD_COLOR};
                border-right: 1px solid #E0E0E0;
            }}
        """)
        nav_panel.setFixedWidth(250)
        nav_layout = QVBoxLayout(nav_panel)
        nav_layout.setContentsMargins(0, 20, 0, 20)
        nav_layout.setSpacing(5)

        # Logo o título en el panel de navegación
        logo_label = QLabel("Expert\nSelector")
        logo_label.setFont(ModernStyle.TITLE_FONT)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet(f"color: {ModernStyle.PRIMARY_COLOR};")
        logo_label.setContentsMargins(0, 0, 0, 30)
        nav_layout.addWidget(logo_label)

        # Botones de navegación
        nav_buttons = [
            ("Candidatos", self.mostrar_candidatos),
            ("Proyectos", self.mostrar_proyectos),
            ("Coincidencias", self.mostrar_coincidencias)
        ]

        for texto, funcion in nav_buttons:
            btn = QPushButton(texto)
            btn.setStyleSheet(ModernStyle.NAV_BUTTON_STYLE)
            btn.setFont(ModernStyle.NORMAL_FONT)
            btn.clicked.connect(funcion)
            nav_layout.addWidget(btn)

        nav_layout.addStretch(1)

        # Contenedor principal de contenido
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(30, 30, 30, 30)

        # Contenedor de contenido con scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #F5F5F5;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #BDBDBD;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #9E9E9E;
            }
        """)

        self.stacked_widget = QStackedWidget()
        scroll_area.setWidget(self.stacked_widget)
        content_layout.addWidget(scroll_area)

        # Crear secciones
        self.crear_seccion_candidatos()
        self.crear_seccion_proyectos()
        self.crear_seccion_coincidencias()

        # Añadir widgets al layout principal
        main_layout.addWidget(nav_panel)
        main_layout.addWidget(content_container, 1)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def crear_seccion_candidatos(self):
        candidatos_widget = QWidget()
        candidatos_layout = QVBoxLayout()
        candidatos_layout.setSpacing(20)

        # Título de la sección
        titulo = QLabel("Gestión de Candidatos")
        titulo.setFont(ModernStyle.HEADER_FONT)
        titulo.setStyleSheet(f"color: {ModernStyle.TEXT_COLOR};")
        candidatos_layout.addWidget(titulo)

        # Contenedor de botones
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        # Botones de acción
        botones = [
            ("Ver Candidatos", self.listar_candidatos),
            ("Agregar Candidato", self.agregar_candidato),
            ("Actualizar Candidato", self.actualizar_candidato_por_id),
            ("Eliminar Candidato", self.eliminar_candidato_por_id)
        ]

        for texto, funcion in botones:
            btn = QPushButton(texto)
            btn.setStyleSheet(ModernStyle.BUTTON_STYLE)
            btn.setFont(ModernStyle.NORMAL_FONT)
            btn.clicked.connect(funcion)
            buttons_layout.addWidget(btn)

        buttons_container.setLayout(buttons_layout)
        candidatos_layout.addWidget(buttons_container)
        candidatos_layout.addStretch(1)

        candidatos_widget.setLayout(candidatos_layout)
        self.stacked_widget.addWidget(candidatos_widget)

    def crear_seccion_proyectos(self):
        proyectos_widget = QWidget()
        proyectos_layout = QVBoxLayout()
        proyectos_layout.setSpacing(20)

        # Título de la sección
        titulo = QLabel("Gestión de Proyectos")
        titulo.setFont(ModernStyle.HEADER_FONT)
        titulo.setStyleSheet(f"color: {ModernStyle.TEXT_COLOR};")
        proyectos_layout.addWidget(titulo)

        # Contenedor de botones
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        # Botones de acción
        botones = [
            ("Ver Proyectos", self.listar_proyectos),
            ("Agregar Proyecto", self.agregar_proyecto),
            ("Actualizar Proyecto", self.actualizar_proyecto_por_id),
            ("Eliminar Proyecto", self.eliminar_proyecto_por_id)
        ]

        for texto, funcion in botones:
            btn = QPushButton(texto)
            btn.setStyleSheet(ModernStyle.BUTTON_STYLE)
            btn.setFont(ModernStyle.NORMAL_FONT)
            btn.clicked.connect(funcion)
            buttons_layout.addWidget(btn)

        buttons_container.setLayout(buttons_layout)
        proyectos_layout.addWidget(buttons_container)
        proyectos_layout.addStretch(1)

        proyectos_widget.setLayout(proyectos_layout)
        self.stacked_widget.addWidget(proyectos_widget)

    def mostrar_candidatos(self):
        self.stacked_widget.setCurrentIndex(0)

    def mostrar_proyectos(self):
        self.stacked_widget.setCurrentIndex(1)

    def listar_candidatos(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Lista de Candidatos")
        dialog.setGeometry(300, 300, 1000, 700)
        dialog.setStyleSheet("""
        QDialog {
            background-color: #f5f5f5;
        }
        QTableWidget {
            background: white;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        QTableWidget::item {
            padding: 5px;
        }
        QTableWidget QHeaderView::section {
            background: #e0e0e0;
            padding: 8px;
            border: none;
            font-weight: bold;
        }
        QTableWidget QHeaderView::section:selected {
            background: #2196F3;
            color: white;
        }
        QPushButton {
            background-color: #2196F3;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #1976D2;
        }
        QLineEdit {
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: white;
            margin-bottom: 10px;
        }
    """)

        main_layout = QVBoxLayout(dialog)

        # Añadir barra de búsqueda
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Buscar candidatos...")
        search_bar.setFixedWidth(300)
        search_layout.addWidget(search_bar)
        search_layout.addStretch()
        main_layout.addWidget(search_container)
  
        # Configurar tabla
        tabla = QTableWidget()
        tabla.setColumnCount(4)  
        tabla.setHorizontalHeaderLabels([
            "ID", "Nombre", "Apellido", "Ubicación"
        ])

        # Estilo para la tabla
        tabla.setAlternatingRowColors(True)
        tabla.setSelectionBehavior(QTableWidget.SelectRows)
        tabla.setSelectionMode(QTableWidget.SingleSelection)
        tabla.verticalHeader().setVisible(False)
        tabla.horizontalHeader().setStretchLastSection(True)
        tabla.setShowGrid(False)

        # Obtener y mostrar candidatos
        candidatos = self.db_manager.listar_candidatos()
        tabla.setRowCount(len(candidatos))
        for fila, candidato in enumerate(candidatos):
            for col, key in enumerate(["id", "nombre", "apellido", "ubicacion"]):
                tabla.setItem(fila, col, QTableWidgetItem(str(candidato.get(key, ''))))

        tabla.resizeColumnsToContents()
        tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Ajustar todas las columnas para ocupar el mismo espacio
        tabla.setSortingEnabled(True)
        main_layout.addWidget(tabla)

        # Implementar búsqueda en tiempo real
        def filtrar_candidatos(text):
            for row in range(tabla.rowCount()):
                mostrar = any(text.lower() in (tabla.item(row, col).text().lower() if tabla.item(row, col) else '') for col in range(tabla.columnCount()))
                tabla.setRowHidden(row, not mostrar)

        search_bar.textChanged.connect(filtrar_candidatos)

        dialog.exec_()

    def listar_proyectos(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Lista de Proyectos")
        dialog.setGeometry(300, 300, 1000, 700)
        dialog.setStyleSheet("""
        QDialog {
            background-color: #f5f5f5;
        }
        QTableWidget {
            background: white;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        QTableWidget::item {
            padding: 5px;
        }
        QTableWidget QHeaderView::section {
            background: #e0e0e0;
            padding: 8px;
            border: none;
            font-weight: bold;
        }
        QTableWidget QHeaderView::section:selected {
            background: #2196F3;
            color: white;
        }
        QPushButton {
            background-color: #2196F3;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #1976D2;
        }
        QLineEdit {
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: white;
            margin-bottom: 10px;
        }
        """)

        main_layout = QVBoxLayout(dialog)

        # Añadir barra de búsqueda
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Buscar proyectos...")
        search_bar.setFixedWidth(300)
        search_layout.addWidget(search_bar)
        search_layout.addStretch()
        main_layout.addWidget(search_container)

        # Configurar tabla
        tabla = QTableWidget()
        tabla.setColumnCount(4)
        tabla.setHorizontalHeaderLabels([
            "ID", "Empresa", "Nombre Proyecto", "Descripción"
        ])

        # Estilo para la tabla
        tabla.setAlternatingRowColors(True)
        tabla.setSelectionBehavior(QTableWidget.SelectRows)
        tabla.setSelectionMode(QTableWidget.SingleSelection)
        tabla.verticalHeader().setVisible(False)
        tabla.horizontalHeader().setStretchLastSection(True)
        tabla.setShowGrid(False)

        # Obtener y mostrar proyectos
        proyectos = self.db_manager.listar_proyectos()
        tabla.setRowCount(len(proyectos))
        for fila, proyecto in enumerate(proyectos):
            for col, key in enumerate(["id", "nombre_empresa", "nombre_proyecto", "descripcion"]):
                tabla.setItem(fila, col, QTableWidgetItem(str(proyecto.get(key, ''))))

        tabla.resizeColumnsToContents()
        tabla.setSortingEnabled(True)
        main_layout.addWidget(tabla)

        # Implementar búsqueda en tiempo real
        def filtrar_proyectos(text):
            for row in range(tabla.rowCount()):
                mostrar = any(text.lower() in (tabla.item(row, col).text().lower() if tabla.item(row, col) else '') for col in range(tabla.columnCount()))
                tabla.setRowHidden(row, not mostrar)

        search_bar.textChanged.connect(filtrar_proyectos)

        dialog.exec_()
    
    def agregar_candidato(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Candidato")
        dialog.setGeometry(250, 250, 800, 600)
        dialog.setStyleSheet("""
        QDialog {
            background-color: #f5f5f5;
        }
        QTabWidget::pane {
            border: 1px solid #ddd;
            background: white;
            border-radius: 5px;
        }
        QTabBar::tab {
            background: #e0e0e0;
            padding: 8px 20px;
            margin: 2px;
            border-radius: 4px;
        }
        QTabBar::tab:selected {
            background: #2196F3;
            color: white;
        }
        QLineEdit, QComboBox {
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: white;
        }
        QPushButton {
            background-color: #2196F3;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #1976D2;
        }
        QCheckBox {
            padding: 5px;
        }
        QLabel {
            font-weight: bold;
        }
    """)

        main_layout = QVBoxLayout(dialog)
        tab_widget = QTabWidget()

    # Tab 1: Información Personal
        personal_tab = QWidget()
        personal_layout = QFormLayout(personal_tab)
    
        nombre = QLineEdit()
        nombre.setPlaceholderText("Ingrese nombre")
        apellido = QLineEdit()
        apellido.setPlaceholderText("Ingrese apellido")
    
        ubicacion = QComboBox()
        ubicacion.addItems(self.db_manager.obtener_paises())
    
        salario = QComboBox()
        salario.addItems(self.db_manager.obtener_salarios())
    
        personal_layout.addRow("Nombre:", nombre)
        personal_layout.addRow("Apellido:", apellido)
        personal_layout.addRow("Ubicación:", ubicacion)
        personal_layout.addRow("Preferencia Salarial:", salario)
  
    # Tab 2: Idiomas
        idiomas_tab = QWidget()
        idiomas_layout = QVBoxLayout(idiomas_tab)
    
        search_idiomas = QLineEdit()
        search_idiomas.setPlaceholderText("Buscar idiomas...")
        idiomas_layout.addWidget(search_idiomas)
    
        idiomas_scroll = QScrollArea()
        idiomas_scroll.setWidgetResizable(True)
        idiomas_content = QWidget()
        idiomas_grid = QGridLayout(idiomas_content)
    
        idiomas_checks = []
        idiomas_list = self.db_manager.obtener_idiomas()
        for i, idioma in enumerate(idiomas_list):
            check = QCheckBox(idioma)
            idiomas_checks.append(check)
            idiomas_grid.addWidget(check, i // 3, i % 3)  # 3 columnas
    
        idiomas_scroll.setWidget(idiomas_content)
        idiomas_layout.addWidget(idiomas_scroll)

    # Tab 3: Habilidades
        habilidades_tab = QWidget()
        habilidades_layout = QVBoxLayout(habilidades_tab)
    
        search_habilidades = QLineEdit()
        search_habilidades.setPlaceholderText("Buscar habilidades...")
        habilidades_layout.addWidget(search_habilidades)
      
        habilidades_scroll = QScrollArea()
        habilidades_scroll.setWidgetResizable(True)
        habilidades_content = QWidget()
        habilidades_grid = QGridLayout(habilidades_content)
    
        habilidades_checks = []
        habilidades_list = self.db_manager.obtener_habilidades()
        for i, habilidad in enumerate(habilidades_list):
            check = QCheckBox(habilidad)
            habilidades_checks.append(check)
            habilidades_grid.addWidget(check, i // 3, i % 3)  # 3 columnas
    
        habilidades_scroll.setWidget(habilidades_content)
        habilidades_layout.addWidget(habilidades_scroll)

    # Añadir tabs
        tab_widget.addTab(personal_tab, "Información Personal")
        tab_widget.addTab(idiomas_tab, "Idiomas")
        tab_widget.addTab(habilidades_tab, "Habilidades")
    
        main_layout.addWidget(tab_widget)

    # Botón guardar
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.addStretch()
    
        btn_guardar = QPushButton("Guardar Candidato")
        btn_guardar.setFixedWidth(200)
        btn_guardar.clicked.connect(lambda: self.guardar_candidato(
            nombre.text(),
            apellido.text(),
            [check.text() for check in idiomas_checks if check.isChecked()],
            [check.text() for check in habilidades_checks if check.isChecked()],
            salario.currentText(),
            ubicacion.currentText(),
            dialog
        ))
    
        btn_layout.addWidget(btn_guardar)
        main_layout.addWidget(btn_container)

    # Implementar búsqueda en tiempo real para idiomas
        def filtrar_idiomas(text):
            for check in idiomas_checks:
                check.setVisible(text.lower() in check.text().lower())
    
        search_idiomas.textChanged.connect(filtrar_idiomas)

        # Implementar búsqueda en tiempo real para habilidades
        def filtrar_habilidades(text):
            for check in habilidades_checks:
                check.setVisible(text.lower() in check.text().lower())
    
        search_habilidades.textChanged.connect(filtrar_habilidades)

        dialog.exec_()
        
    def agregar_proyecto(self):
        """Diálogo para agregar un nuevo proyecto"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Proyecto")
        dialog.setGeometry(250, 250, 900, 600)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                background: white;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #e0e0e0;
                padding: 8px 20px;
                margin: 2px;
                border-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #2196F3;
                color: white;
            }
            QLineEdit, QComboBox, QTextEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background: white;
            }
            QTextEdit {
                min-height: 100px;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QCheckBox {
                padding: 5px;
            }
            QLabel {
                font-weight: bold;
                color: #333;
            }
        """)

        main_layout = QVBoxLayout(dialog)
        tab_widget = QTabWidget()

        # Tab 1: Información del Proyecto
        info_tab = QWidget()
        info_layout = QFormLayout(info_tab)
        
        nombre_empresa = QLineEdit()
        nombre_empresa.setPlaceholderText("Ingrese nombre de la empresa")
        
        nombre_proyecto = QLineEdit()
        nombre_proyecto.setPlaceholderText("Ingrese nombre del proyecto")
        
        descripcion = QTextEdit()
        descripcion.setPlaceholderText("Describa el proyecto...")
        
        ubicacion = QComboBox()
        ubicacion.addItems(self.db_manager.obtener_paises())
        
        salario_minimo = QComboBox()
        salario_minimo.addItems(self.db_manager.obtener_salarios())
        
        info_layout.addRow("Nombre de la Empresa:", nombre_empresa)
        info_layout.addRow("Nombre del Proyecto:", nombre_proyecto)
        info_layout.addRow("Descripción:", descripcion)
        info_layout.addRow("Ubicación:", ubicacion)
        info_layout.addRow("Salario Mínimo:", salario_minimo)

        # Tab 2: Idiomas Requeridos
        idiomas_tab = QWidget()
        idiomas_layout = QVBoxLayout(idiomas_tab)
        
        search_idiomas = QLineEdit()
        search_idiomas.setPlaceholderText("Buscar idiomas...")
        idiomas_layout.addWidget(search_idiomas)
        
        idiomas_scroll = QScrollArea()
        idiomas_scroll.setWidgetResizable(True)
        idiomas_content = QWidget()
        idiomas_grid = QGridLayout(idiomas_content)
        idiomas_grid.setSpacing(10)
        
        idiomas_checks = []
        idiomas_list = self.db_manager.obtener_idiomas()
        for i, idioma in enumerate(idiomas_list):
            container = QWidget()
            container_layout = QHBoxLayout(container)
            container_layout.setContentsMargins(5, 5, 5, 5)
            
            check = QCheckBox(idioma)
            idiomas_checks.append(check)
            container_layout.addWidget(check)
            
            idiomas_grid.addWidget(container, i // 3, i % 3)  # 3 columnas
        
        idiomas_scroll.setWidget(idiomas_content)
        idiomas_layout.addWidget(idiomas_scroll)

        # Tab 3: Habilidades Requeridas
        habilidades_tab = QWidget()
        habilidades_layout = QVBoxLayout(habilidades_tab)
        
        search_habilidades = QLineEdit()
        search_habilidades.setPlaceholderText("Buscar habilidades...")
        habilidades_layout.addWidget(search_habilidades)
        
        habilidades_scroll = QScrollArea()
        habilidades_scroll.setWidgetResizable(True)
        habilidades_content = QWidget()
        habilidades_grid = QGridLayout(habilidades_content)
        habilidades_grid.setSpacing(10)
        
        habilidades_checks = []
        habilidades_list = self.db_manager.obtener_habilidades()
        for i, habilidad in enumerate(habilidades_list):
            container = QWidget()
            container_layout = QHBoxLayout(container)
            container_layout.setContentsMargins(5, 5, 5, 5)
            
            check = QCheckBox(habilidad)
            habilidades_checks.append(check)
            container_layout.addWidget(check)
            
            habilidades_grid.addWidget(container, i // 3, i % 3)  # 3 columnas
        
        habilidades_scroll.setWidget(habilidades_content)
        habilidades_layout.addWidget(habilidades_scroll)

        # Añadir tabs al widget principal
        tab_widget.addTab(info_tab, "Información del Proyecto")
        tab_widget.addTab(idiomas_tab, "Idiomas Requeridos")
        tab_widget.addTab(habilidades_tab, "Habilidades Requeridas")
        
        main_layout.addWidget(tab_widget)

        # Contenedor de botones
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.addStretch()
        
        btn_guardar = QPushButton("Guardar Proyecto")
        btn_guardar.setFixedWidth(200)
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
        
        btn_layout.addWidget(btn_guardar)
        main_layout.addWidget(btn_container)

        # Implementar búsqueda en tiempo real para idiomas
        def filtrar_idiomas(text):
            for check in idiomas_checks:
                check.parent().setVisible(text.lower() in check.text().lower())
        
        search_idiomas.textChanged.connect(filtrar_idiomas)

        # Implementar búsqueda en tiempo real para habilidades
        def filtrar_habilidades(text):
            for check in habilidades_checks:
                check.parent().setVisible(text.lower() in check.text().lower())
        
        search_habilidades.textChanged.connect(filtrar_habilidades)

        dialog.exec_()        

    def guardar_candidato(self, nombre, apellido, idiomas, habilidades, salario, ubicacion, dialog):
        
    # Validar campos obligatorios
      if not nombre or not apellido:
            QMessageBox.warning(self, "Error", "Nombre y apellido son obligatorios")
            return

    # Validar que nombre y apellido solo contengan letras
      if not nombre.isalpha() or not apellido.isalpha():
            QMessageBox.warning(self, "Error", "Nombre y apellido solo deben contener letras")
            return
    
      if not idiomas or not habilidades:
            QMessageBox.warning(self, "Error", "Debe seleccionar al menos un idioma y una habilidad")
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
        if not nombre_empresa or not nombre_proyecto or not descripcion:
            QMessageBox.warning(self, "Error", "Nombre de empresa, proyecto y descripción son obligatorios")
            return

        if not idiomas_requeridos or not habilidades_requeridas:
            QMessageBox.warning(self, "Error", "Debe seleccionar requerimientos")
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

    def actualizar_candidato(self, candidato):
        dialog = QDialog(self)
        dialog.setWindowTitle("Actualizar Candidato")
        dialog.setGeometry(250, 250, 800, 600)
        dialog.setStyleSheet("""
        QDialog {
            background-color: #f5f5f5;
        }
        QTabWidget::pane {
            border: 1px solid #ddd;
            background: white;
            border-radius: 5px;
        }
        QTabBar::tab {
            background: #e0e0e0;
            padding: 8px 20px;
            margin: 2px;
            border-radius: 4px;
        }
        QTabBar::tab:selected {
            background: #2196F3;
            color: white;
        }
        QLineEdit, QComboBox {
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: white;
        }
        QPushButton {
            background-color: #2196F3;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #1976D2;
        }
        QCheckBox {
            padding: 5px;
        }
        QLabel {
            font-weight: bold;
        }
    """)

        main_layout = QVBoxLayout(dialog)
        tab_widget = QTabWidget()

    # Tab 1: Información Personal
        personal_tab = QWidget()
        personal_layout = QFormLayout(personal_tab)
    
        nombre = QLineEdit(candidato['nombre'])
        nombre.setPlaceholderText("Ingrese nombre")
        apellido = QLineEdit(candidato['apellido'])
        apellido.setPlaceholderText("Ingrese apellido")
    
        ubicacion = QComboBox()
        ubicacion.addItems(self.db_manager.obtener_paises())
        ubicacion.setCurrentText(candidato['ubicacion'])
    
        salario = QComboBox()
        salario.addItems(self.db_manager.obtener_salarios())
        salario.setCurrentText(str(candidato['preferencia_salarial']))
    
        personal_layout.addRow("Nombre:", nombre)
        personal_layout.addRow("Apellido:", apellido)
        personal_layout.addRow("Ubicación:", ubicacion)
        personal_layout.addRow("Preferencia Salarial:", salario)
  
    # Tab 2: Idiomas
        idiomas_tab = QWidget()
        idiomas_layout = QVBoxLayout(idiomas_tab)
    
        search_idiomas = QLineEdit()
        search_idiomas.setPlaceholderText("Buscar idiomas...")
        idiomas_layout.addWidget(search_idiomas)
    
        idiomas_scroll = QScrollArea()
        idiomas_scroll.setWidgetResizable(True)
        idiomas_content = QWidget()
        idiomas_grid = QGridLayout(idiomas_content)
    
        idiomas_checks = []
        idiomas_list = self.db_manager.obtener_idiomas()
        candidato_idiomas = candidato['idiomas'] if isinstance(candidato['idiomas'], list) else eval(candidato['idiomas'])
    
        for i, idioma in enumerate(idiomas_list):
            check = QCheckBox(idioma)
            check.setChecked(idioma in candidato_idiomas)
            idiomas_checks.append(check)
            idiomas_grid.addWidget(check, i // 3, i % 3)  # 3 columnas
    
        idiomas_scroll.setWidget(idiomas_content)
        idiomas_layout.addWidget(idiomas_scroll)

    # Tab 3: Habilidades
        habilidades_tab = QWidget()
        habilidades_layout = QVBoxLayout(habilidades_tab)
    
        search_habilidades = QLineEdit()
        search_habilidades.setPlaceholderText("Buscar habilidades...")
        habilidades_layout.addWidget(search_habilidades)
      
        habilidades_scroll = QScrollArea()
        habilidades_scroll.setWidgetResizable(True)
        habilidades_content = QWidget()
        habilidades_grid = QGridLayout(habilidades_content)
    
        habilidades_checks = []
        habilidades_list = self.db_manager.obtener_habilidades()
        candidato_habilidades = candidato['habilidades'] if isinstance(candidato['habilidades'], list) else eval(candidato['habilidades'])
    
        for i, habilidad in enumerate(habilidades_list):
            check = QCheckBox(habilidad)
            check.setChecked(habilidad in candidato_habilidades)
            habilidades_checks.append(check)
            habilidades_grid.addWidget(check, i // 3, i % 3)  # 3 columnas
    
        habilidades_scroll.setWidget(habilidades_content)
        habilidades_layout.addWidget(habilidades_scroll)

    # Añadir tabs
        tab_widget.addTab(personal_tab, "Información Personal")
        tab_widget.addTab(idiomas_tab, "Idiomas")
        tab_widget.addTab(habilidades_tab, "Habilidades")
    
        main_layout.addWidget(tab_widget)

    # Botón actualizar
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.addStretch()
    
        btn_actualizar = QPushButton("Actualizar Candidato")
        btn_actualizar.setFixedWidth(200)
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
    
        btn_layout.addWidget(btn_actualizar)
        main_layout.addWidget(btn_container)

    # Implementar búsqueda en tiempo real para idiomas
        def filtrar_idiomas(text):
            for check in idiomas_checks:
                check.setVisible(text.lower() in check.text().lower())
    
        search_idiomas.textChanged.connect(filtrar_idiomas)

    # Implementar búsqueda en tiempo real para habilidades
        def filtrar_habilidades(text):
            for check in habilidades_checks:
                check.setVisible(text.lower() in check.text().lower())
    
        search_habilidades.textChanged.connect(filtrar_habilidades)

        dialog.exec_()

    def actualizar_proyecto(self, proyecto):
        dialog = QDialog(self)
        dialog.setWindowTitle("Actualizar Proyecto")
        dialog.setGeometry(250, 250, 800, 600)
        dialog.setStyleSheet("""
        QDialog {
            background-color: #f5f5f5;
        }
        QTabWidget::pane {
            border: 1px solid #ddd;
            background: white;
            border-radius: 5px;
        }
        QTabBar::tab {
            background: #e0e0e0;
            padding: 8px 20px;
            margin: 2px;
            border-radius: 4px;
        }
        QTabBar::tab:selected {
            background: #2196F3;
            color: white;
        }
        QLineEdit, QComboBox, QTextEdit {
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: white;
        }
        QPushButton {
            background-color: #2196F3;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #1976D2;
        }
        QCheckBox {
            padding: 5px;
        }
        QLabel {
            font-weight: bold;
        }
    """)

        main_layout = QVBoxLayout(dialog)
        tab_widget = QTabWidget()

        # Tab 1: Información General
        info_tab = QWidget()
        info_layout = QFormLayout(info_tab)
        
        nombre_empresa = QLineEdit(proyecto['nombre_empresa'])
        nombre_empresa.setPlaceholderText("Ingrese nombre de la empresa")
        
        nombre_proyecto = QLineEdit(proyecto['nombre_proyecto'])
        nombre_proyecto.setPlaceholderText("Ingrese nombre del proyecto")
        
        descripcion = QTextEdit()
        descripcion.setText(proyecto['descripcion'])
        descripcion.setMinimumHeight(100)
        
        ubicacion = QComboBox()
        ubicacion.addItems(self.db_manager.obtener_paises())
        ubicacion.setCurrentText(proyecto['ubicacion'])
        
        salario_minimo = QComboBox()
        salario_minimo.addItems(self.db_manager.obtener_salarios())
        salario_minimo.setCurrentText(proyecto['salario_minimo'])
        
        info_layout.addRow("Nombre de la Empresa:", nombre_empresa)
        info_layout.addRow("Nombre del Proyecto:", nombre_proyecto)
        info_layout.addRow("Descripción:", descripcion)
        info_layout.addRow("Ubicación:", ubicacion)
        info_layout.addRow("Salario Mínimo:", salario_minimo)

        # Tab 2: Idiomas Requeridos
        idiomas_tab = QWidget()
        idiomas_layout = QVBoxLayout(idiomas_tab)
        
        search_idiomas = QLineEdit()
        search_idiomas.setPlaceholderText("Buscar idiomas...")
        idiomas_layout.addWidget(search_idiomas)
        
        idiomas_scroll = QScrollArea()
        idiomas_scroll.setWidgetResizable(True)
        idiomas_content = QWidget()
        idiomas_grid = QGridLayout(idiomas_content)
        
        idiomas_checks = []
        idiomas_list = self.db_manager.obtener_idiomas()
        for i, idioma in enumerate(idiomas_list):
            check = QCheckBox(idioma)
            check.setChecked(idioma in proyecto['idiomas_requeridos'])
            idiomas_checks.append(check)
            idiomas_grid.addWidget(check, i // 3, i % 3)  # 3 columnas
        
        idiomas_scroll.setWidget(idiomas_content)
        idiomas_layout.addWidget(idiomas_scroll)

        # Tab 3: Habilidades Requeridas
        habilidades_tab = QWidget()
        habilidades_layout = QVBoxLayout(habilidades_tab)
        
        search_habilidades = QLineEdit()
        search_habilidades.setPlaceholderText("Buscar habilidades...")
        habilidades_layout.addWidget(search_habilidades)
        
        habilidades_scroll = QScrollArea()
        habilidades_scroll.setWidgetResizable(True)
        habilidades_content = QWidget()
        habilidades_grid = QGridLayout(habilidades_content)
        
        habilidades_checks = []
        habilidades_list = self.db_manager.obtener_habilidades()
        for i, habilidad in enumerate(habilidades_list):
            check = QCheckBox(habilidad)
            check.setChecked(habilidad in proyecto['habilidades_requeridas'])
            habilidades_checks.append(check)
            habilidades_grid.addWidget(check, i // 3, i % 3)  # 3 columnas
        
        habilidades_scroll.setWidget(habilidades_content)
        habilidades_layout.addWidget(habilidades_scroll)

        # Añadir tabs
        tab_widget.addTab(info_tab, "Información General")
        tab_widget.addTab(idiomas_tab, "Idiomas Requeridos")
        tab_widget.addTab(habilidades_tab, "Habilidades Requeridas")
        
        main_layout.addWidget(tab_widget)

        # Botón actualizar
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.addStretch()
        
        btn_actualizar = QPushButton("Actualizar Proyecto")
        btn_actualizar.setFixedWidth(200)
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
        
        btn_layout.addWidget(btn_actualizar)
        main_layout.addWidget(btn_container)

        # Implementar búsqueda en tiempo real para idiomas
        def filtrar_idiomas(text):
            for check in idiomas_checks:
                check.setVisible(text.lower() in check.text().lower())
        
        search_idiomas.textChanged.connect(filtrar_idiomas)

        # Implementar búsqueda en tiempo real para habilidades
        def filtrar_habilidades(text):
            for check in habilidades_checks:
                check.setVisible(text.lower() in check.text().lower())
        
        search_habilidades.textChanged.connect(filtrar_habilidades)

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

    def crear_seccion_coincidencias(self):
        """Crea la sección de coincidencias"""
        coincidencias_widget = QWidget()
        coincidencias_layout = QVBoxLayout()
        coincidencias_layout.setSpacing(20)

        # Título de la sección
        titulo = QLabel("Gestión de Coincidencias")
        titulo.setFont(ModernStyle.HEADER_FONT)
        titulo.setStyleSheet(f"color: {ModernStyle.TEXT_COLOR};")
        coincidencias_layout.addWidget(titulo)

        # Contenedor de botones
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        # Botones de acción
        botones = [
            ("Generar Coincidencias", self.generar_coincidencias),
            ("Listar Coincidencias", self.listar_coincidencias)
        ]

        for texto, funcion in botones:
            btn = QPushButton(texto)
            btn.setStyleSheet(ModernStyle.BUTTON_STYLE)
            btn.setFont(ModernStyle.NORMAL_FONT)
            btn.clicked.connect(funcion)
            buttons_layout.addWidget(btn)

        buttons_container.setLayout(buttons_layout)
        coincidencias_layout.addWidget(buttons_container)
        coincidencias_layout.addStretch(1)

        coincidencias_widget.setLayout(coincidencias_layout)
        self.stacked_widget.addWidget(coincidencias_widget)

    def mostrar_coincidencias(self):
        """Muestra la sección de coincidencias"""
        self.stacked_widget.setCurrentIndex(2)

    def generar_coincidencias(self):
        """Diálogo para generar coincidencias para un proyecto específico"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Generar Coincidencias")
        dialog.setGeometry(250, 250, 300, 150)

        layout = QVBoxLayout()

        # Campo para ID del proyecto
        id_label = QLabel("ID del Proyecto:")
        id_input = QLineEdit()
        id_input.setPlaceholderText("Ingrese ID del proyecto")

        # Botón para generar
        btn_generar = QPushButton("Generar Coincidencias")
        btn_generar.clicked.connect(lambda: self.ejecutar_generacion_coincidencias(id_input.text(), dialog))

        layout.addWidget(id_label)
        layout.addWidget(id_input)
        layout.addWidget(btn_generar)

        dialog.setLayout(layout)
        dialog.exec_()

    def ejecutar_generacion_coincidencias(self, id_proyecto, dialog):
        """Ejecuta el proceso de generación de coincidencias"""
        try:
            if not id_proyecto.isdigit():
                QMessageBox.warning(self, "Error", "Por favor ingrese un ID válido")
                return

            proyecto_id = int(id_proyecto)
        
            # Obtener proyecto
            proyecto = self.db_manager.obtener_proyecto_por_id(proyecto_id)
    
            if not proyecto:
                QMessageBox.warning(self, "Error", "No se encontró el proyecto especificado")
                return

            # Asegurarnos que el proyecto tenga su ID
            proyecto['id'] = proyecto_id
 
            # Obtener todos los candidatos
            candidatos = self.db_manager.listar_candidatos()
     
            if not candidatos:
                QMessageBox.warning(self, "Error", "No hay candidatos registrados en el sistema")
                return

            # Generar coincidencias usando el algoritmo de matching
            coincidencias = self.matching_algorithm.generar_coincidencias(proyecto, candidatos)
    
            # Asegurarnos que cada coincidencia tenga el proyecto_id
            for coincidencia in coincidencias:
                coincidencia['proyecto_id'] = proyecto_id
     
            # Guardar coincidencias en la base de datos
            self.db_manager.guardar_coincidencias(proyecto_id, coincidencias)
    
            QMessageBox.information(
                self, 
                "Éxito", 
                f"Se generaron {len(coincidencias)} coincidencias para el proyecto"
            )
            dialog.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar coincidencias: {str(e)}")

    def listar_coincidencias(self):
        """Diálogo para mostrar coincidencias de un proyecto específico"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Listar Coincidencias")
        dialog.setGeometry(250, 250, 300, 150)

        layout = QVBoxLayout()

        # Campo para ID del proyecto
        id_label = QLabel("ID del Proyecto:")
        id_input = QLineEdit()
        id_input.setPlaceholderText("Ingrese ID del proyecto")

        # Botón para buscar
        btn_buscar = QPushButton("Buscar Coincidencias")
        btn_buscar.clicked.connect(lambda: self.mostrar_lista_coincidencias(id_input.text(), dialog))

        layout.addWidget(id_label)
        layout.addWidget(id_input)
        layout.addWidget(btn_buscar)

        dialog.setLayout(layout)
        dialog.exec_()

    def mostrar_lista_coincidencias(self, id_proyecto, dialog_previo):
        """Muestra la lista de coincidencias para un proyecto específico"""
        try:
            if not id_proyecto.isdigit():
                QMessageBox.warning(self, "Error", "Por favor ingrese un ID válido")
                return

            # Obtener coincidencias
            coincidencias = self.db_manager.obtener_coincidencias(int(id_proyecto))
            
            if not coincidencias:
                QMessageBox.information(self, "Info", "No se encontraron coincidencias para este proyecto")
                return

            # Crear nuevo diálogo para mostrar coincidencias
            lista_dialog = QDialog(self)
            lista_dialog.setWindowTitle(f"Coincidencias del Proyecto {id_proyecto}")
            lista_dialog.setGeometry(200, 200, 900, 500)

            layout = QVBoxLayout()
            
            # Crear tabla
            tabla = QTableWidget()
            tabla.setColumnCount(7)
            tabla.setHorizontalHeaderLabels([
                "ID Candidato", "Nombre", "Apellido", 
                "Porcentaje Match", "Idiomas", "Habilidades", 
                "Ubicación"
            ])

            # Poblar tabla
            tabla.setRowCount(len(coincidencias))
            for fila, coincidencia in enumerate(coincidencias):
                tabla.setItem(fila, 0, QTableWidgetItem(str(coincidencia['id_candidato'])))
                tabla.setItem(fila, 1, QTableWidgetItem(coincidencia['nombre']))
                tabla.setItem(fila, 2, QTableWidgetItem(coincidencia['apellido']))
                tabla.setItem(fila, 3, QTableWidgetItem(f"{coincidencia['porcentaje_match']}%"))
                tabla.setItem(fila, 4, QTableWidgetItem(str(coincidencia['idiomas'])))
                tabla.setItem(fila, 5, QTableWidgetItem(str(coincidencia['habilidades'])))
                tabla.setItem(fila, 6, QTableWidgetItem(coincidencia['ubicacion']))

            tabla.resizeColumnsToContents()
            tabla.setSortingEnabled(True)

            layout.addWidget(tabla)
            lista_dialog.setLayout(layout)
            
            dialog_previo.accept()
            lista_dialog.exec_()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al listar coincidencias: {str(e)}")