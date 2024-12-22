import sys
import json
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QComboBox, QPushButton, QStackedWidget, 
    QTableWidget, QTableWidgetItem, QFormLayout, QCheckBox, QDialog, 
    QMessageBox, QTextEdit, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
from modern_style import ModernStyle

class ModernDialog(QDialog):
    def __init__(self, parent=None, title="Dialog"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setStyleSheet(f"background-color: {ModernStyle.BACKGROUND_COLOR};")
        self.setFont(ModernStyle.NORMAL_FONT)