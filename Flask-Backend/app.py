# app.py (in the project root)
import sys
import os

# Add the 'src' folder to sys.path
src_path = os.path.join(os.path.dirname(__file__), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from main_window import MainWindow  # Now import from the src folder
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
