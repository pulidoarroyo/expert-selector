import traceback

from google.genai import types

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTextEdit,
)
from PyQt5.QtGui import QTextDocument

from ai import GENAI_MODEL, genai_client
from modern_style import ModernStyle
from chat_tools import make_chat_tools


class ChatSection(QWidget):
    def __init__(self, db_manager, matching_algorithm, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.matching_algorithm = matching_algorithm
        self.default_model = GENAI_MODEL
        self.chat_session = None
        self.chat_session_model = None
        self.chat_session_instruction = None
        self.genai_tools = make_chat_tools(self.db_manager, self.matching_algorithm)
        self.chat_history_markdown = []
        self.chat_messages = self._build_initial_chat_messages()
        self._build_ui()
        self._cargar_modelos()

    def _build_ui(self):
        chat_layout = QVBoxLayout()
        chat_layout.setSpacing(12)

        titulo = QLabel("Chat de la Aplicacion")
        titulo.setFont(ModernStyle.HEADER_FONT)
        titulo.setStyleSheet(f"color: {ModernStyle.TEXT_COLOR};")
        chat_layout.addWidget(titulo)

        config_container = QWidget()
        config_layout = QHBoxLayout(config_container)
        config_layout.setContentsMargins(0, 0, 0, 0)

        model_label = QLabel("Modelo GenAI:")
        model_label.setFont(ModernStyle.NORMAL_FONT)

        self.chat_model_select = QComboBox()
        self.chat_model_select.setEditable(True)
        self.chat_model_select.setFixedWidth(240)
        self.chat_model_select.setPlaceholderText("Modelo")
        if self.default_model:
            self.chat_model_select.addItem(self.default_model)
            self.chat_model_select.setCurrentText(self.default_model)

        btn_actualizar_modelos = QPushButton("Actualizar modelos")
        btn_actualizar_modelos.setStyleSheet(ModernStyle.BUTTON_STYLE)
        btn_actualizar_modelos.clicked.connect(self._cargar_modelos)

        btn_limpiar = QPushButton("Limpiar chat")
        btn_limpiar.setStyleSheet(ModernStyle.BUTTON_STYLE)
        btn_limpiar.clicked.connect(self.limpiar_chat)

        config_layout.addWidget(model_label)
        config_layout.addWidget(self.chat_model_select)
        config_layout.addWidget(btn_actualizar_modelos)
        config_layout.addStretch()
        config_layout.addWidget(btn_limpiar)
        chat_layout.addWidget(config_container)

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet("""
            QTextEdit {
                background: white;
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        chat_layout.addWidget(self.chat_history, 1)

        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)

        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText(
            "Escribe una pregunta sobre candidatos, proyectos o coincidencias..."
        )
        self.chat_input.returnPressed.connect(self.enviar_mensaje_chat)

        btn_enviar = QPushButton("Enviar")
        btn_enviar.setStyleSheet(ModernStyle.BUTTON_STYLE)
        btn_enviar.clicked.connect(self.enviar_mensaje_chat)

        input_layout.addWidget(self.chat_input, 1)
        input_layout.addWidget(btn_enviar)
        chat_layout.addWidget(input_container)

        self.setLayout(chat_layout)

    def limpiar_chat(self):
        self.chat_messages = self._build_initial_chat_messages()
        self.chat_history_markdown = []
        self.chat_history.clear()

    def enviar_mensaje_chat(self):
        texto = self.chat_input.text().strip()
        if not texto:
            return

        self.chat_input.clear()
        self._append_chat_history("Usuario", texto)
        self.chat_messages.append({"role": "user", "content": texto})

        try:
            respuesta = self._obtener_respuesta_genai(self.chat_messages)
        except Exception as exc:
            # print debug errror trace
            print("Error al obtener respuesta de GenAI:", exc)
            traceback.print_exc()
            self._append_chat_history(
                "Sistema",
                f"No se pudo contactar a GenAI: {str(exc)}",
            )
            return

        if respuesta:
            self.chat_messages.append({"role": "assistant", "content": respuesta})
            self._append_chat_history("Asistente", respuesta)

    def _append_chat_history(self, titulo, texto):
        entry = f"**{titulo}:**\n\n{texto}".strip()
        self.chat_history_markdown.append(entry)
        combined = "\n\n---\n\n".join(self.chat_history_markdown)
        if hasattr(self.chat_history, "setMarkdown"):
            self.chat_history.setMarkdown(combined)
        else:
            doc = QTextDocument()
            doc.setMarkdown(combined)
            self.chat_history.setHtml(doc.toHtml())

    def _build_initial_chat_messages(self):
        system_prompt = self._cargar_system_prompt()
        return [{"role": "system", "content": system_prompt}]

    def _cargar_system_prompt(self):
        try:
            with open("system_prompt.md", "r", encoding="utf-8") as prompt_file:
                contenido = prompt_file.read().strip()
            return contenido or "Eres un asistente de la aplicacion Expert Selector."
        except OSError:
            return "Eres un asistente de la aplicacion Expert Selector."

    def _cargar_modelos(self):
        try:
            respuesta = genai_client.models.list()
            modelos = list(respuesta)

            nombres = sorted(
                set(modelo.name for modelo in modelos if modelo.name is not None)
            )

            current = self.chat_model_select.currentText().strip() or self.default_model

            self.chat_model_select.clear()
            if nombres:
                self.chat_model_select.addItems(nombres)
            if current:
                if current not in nombres:
                    self.chat_model_select.insertItem(0, current)
                self.chat_model_select.setCurrentText(current)
            if current != self.chat_session_model:
                self.chat_session = None
        except Exception as exc:
            self.chat_model_select.clear()
            self._append_chat_history(
                "Sistema",
                f"No se pudo listar modelos: {str(exc)}",
            )

    def _obtener_respuesta_genai(self, messages):
        model = self.chat_model_select.currentText().strip() or self.default_model
        if not model:
            raise Exception("Selecciona un modelo antes de continuar")
        chat = self._get_chat_session(model, self._get_system_instruction(messages))
        content = messages[-1].get("content", "")
        response = chat.send_message(content)
        return response.text

    def _get_system_instruction(self, messages):
        for message in messages:
            if message.get("role") == "system":
                return message.get("content", "")
        return ""

    def _get_chat_session(self, model, system_instruction):
        if (
            self.chat_session is None
            or self.chat_session_model != model
            or self.chat_session_instruction != system_instruction
        ):
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=self.genai_tools,
            )
            self.chat_session = genai_client.chats.create(model=model, config=config)
            self.chat_session_model = model
            self.chat_session_instruction = system_instruction
        return self.chat_session
