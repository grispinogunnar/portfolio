from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
import sys
import os

def load_stylesheet():
    """
    Load the QSS stylesheet for the application.
    """
    # Determine the base path (different for PyInstaller and regular execution)
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS  # PyInstaller's temporary directory
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    qss_path = os.path.join(base_path, "gui", "styles.qss")
    with open(qss_path, "r") as file:
        return file.read()


def main():
    app = QApplication(sys.argv)

    # Load and apply stylesheet
    stylesheet = load_stylesheet()
    app.setStyleSheet(stylesheet)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
