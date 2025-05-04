import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

from ui import MemeGeneratorUI


def main():
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    app = QApplication(sys.argv)
    
    
    ui = MemeGeneratorUI()
    ui.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 