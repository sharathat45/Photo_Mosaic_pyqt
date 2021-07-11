import style_sheet
from mosaic_window import window
from PyQt4.QtGui import QApplication
import sys

if __name__ == '__main__':
   app = QApplication(sys.argv)
   style_sheet.window_app_style(app)
   win = window()
   win.show()
   sys.exit(app.exec_())
