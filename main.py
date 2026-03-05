import signal
import sys
from PyQt5.QtWidgets import QApplication
from expert_selector import ExpertSelector


def main():
    app = QApplication(sys.argv)
    ventana = ExpertSelector()
    ventana.show()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
