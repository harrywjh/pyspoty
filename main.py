import sys  
from PyQt5.QtWidgets import QApplication, QWidget
import ui

app = QApplication(sys.argv)
widget = ui.LyricsWidget()
widget.show()
sys.exit(app.exec_())