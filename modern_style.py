from PyQt5.QtGui import QFont

class ModernStyle:
    # Color scheme
    PRIMARY_COLOR = "#2196F3"  # Blue
    SECONDARY_COLOR = "#FFC107"  # Amber
    BACKGROUND_COLOR = "#F5F5F5"  # Light Grey
    CARD_COLOR = "#FFFFFF"  # White
    TEXT_COLOR = "#333333"  # Dark Grey
    
    # Font styles
    TITLE_FONT = QFont("Segoe UI", 24, QFont.Bold)
    HEADER_FONT = QFont("Segoe UI", 16)
    NORMAL_FONT = QFont("Segoe UI", 10)
    
    # Button styles
    BUTTON_STYLE = """
        QPushButton {
            background-color: #2196F3;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #1976D2;
        }
        QPushButton:pressed {
            background-color: #0D47A1;
        }
    """
    
    NAV_BUTTON_STYLE = """
        QPushButton {
            background-color: transparent;
            color: #333333;
            border: none;
            padding: 12px 24px;
            text-align: left;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #E3F2FD;
        }
        QPushButton:pressed {
            background-color: #BBDEFB;
        }
    """
    
    # Table styles
    TABLE_STYLE = """
        QTableWidget {
            background-color: white;
            gridline-color: #E0E0E0;
            border: 1px solid #E0E0E0;
            border-radius: 4px;
        }
        QTableWidget::item {
            padding: 8px;
        }
        QHeaderView::section {
            background-color: #F5F5F5;
            padding: 8px;
            border: none;
            font-weight: bold;
        }
    """