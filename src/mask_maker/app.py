import sys
from PySide6.QtWidgets import QApplication , QMainWindow

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Open Mask Maker")
    window.show()
    return app.exec()
