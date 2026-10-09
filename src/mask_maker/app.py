import sys
from PySide6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    app.show()
    return app.exec()
