import sys
import json
from PyQt5.QtWidgets import QApplication
from expert_selector import ExpertSelector

def main():
    app = QApplication(sys.argv)
    ventana = ExpertSelector()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()