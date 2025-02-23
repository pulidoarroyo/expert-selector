from PyQt5.QtWidgets import QDialog
from modern_style import ModernStyle

class ModernDialog(QDialog):
    def __init__(self, parent=None, title="Dialog"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setStyleSheet(f"background-color: {ModernStyle.BACKGROUND_COLOR};")
        self.setFont(ModernStyle.NORMAL_FONT)