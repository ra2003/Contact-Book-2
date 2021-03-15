import sys
from PyQt6.QtWidgets import QApplication
from .views import Window
from .database import createConnection


def main():
    app = QApplication(sys.argv)
    if not createConnection("contacts.sqlite"):
        sys.exit(1)
    win = Window()
    win.show()
    sys.exit(app.exec())

