from PyQt4.QtCore import Qt
from PyQt4.QtGui import QPalette, QColor

background_clr = '#1A1A1D'
qpalette_background_clr = QColor(26, 26, 29)

title_clr = '#E6E6FA'
title_font_size = 40

button_clr = background_clr
button_border_clr = '#6F2232' 
button_font_clr = '#4E4E50'
button_font_family='Arial, Helvetica, Sans-serif'
button_font_size = '12px'

button_hover_clr = '#E6E6FA'
button_hover_font_clr = '#6F2232'

progress_bar_clr_1  = '#845EC2'
progress_bar_clr_2  = '#C34A36'
progress_bar_bckgrnd_clr = '#4E4E50'
progress_bar_txt_clr = '#E6E6FA'

def window_app_style(app):
   app.setStyle("Fusion")
   palette = QPalette()
   palette.setColor(QPalette.Window, qpalette_background_clr)
   palette.setColor(QPalette.WindowText, Qt.gray)
   palette.setColor(QPalette.Base, qpalette_background_clr) 
   palette.setColor(QPalette.AlternateBase, qpalette_background_clr)
   palette.setColor(QPalette.ToolTipBase, Qt.white)
   palette.setColor(QPalette.ToolTipText, Qt.black)
   palette.setColor(QPalette.Text, Qt.gray)
   # palette.setColor(QPalette.Button, qpalette_background_clr)
   # palette.setColor(QPalette.ButtonText, Qt.gray)
   # palette.setColor(QPalette.BrightText, Qt.gray)
   # palette.setColor(QPalette.Link, QColor(111,34,50))
   palette.setColor(QPalette.Highlight, QColor(230, 230, 250))
   palette.setColor(QPalette.HighlightedText, QColor(111,34,50))
   app.setPalette(palette)

window_style = '''
      #MainTitle {
         color: ''' + title_clr + ''';
      }
      QPushButton {
         background-color: '''+ button_clr +''';
         border-style: outset;
         border-width: 0.5px;
         border-radius: 10px;
         border-color:''' + button_border_clr +''';
         padding: 6px; 
         
         font-family: ''' + button_font_family + ''';
         font-weight: bold;
         color:'''+ button_font_clr +''';
         font-size:'''+ button_font_size +''';
      }
      QPushButton::hover
      {
         background-color :''' + button_hover_clr + ''';
         color: ''' + button_hover_font_clr + ''';
      }
      QComboBox::hover
      {
         background-color :''' + button_hover_clr +''';
         color:  ''' + button_hover_font_clr + ''';
      }
      QComboBox {
         background-color:''' + button_clr + ''';
         border-style: outset;
         border-width: 0.5px;
         border-radius: 10px;
         border-color:'''+ button_border_clr +''';
         padding: 6px; 
         
         font-family: ''' + button_font_family + ''';
         color: ''' + button_font_clr + ''';
         font-size: '''+ button_font_size +''';
         font-weight: bold;  
      }
      QComboBox::drop-down
      {
         background-color: transparent;
      }
      QComboBox::down-arrow
      {
         image: url(images/down-arrow.png);
         width: 14px;
         height: 14px;
      }

      QProgressBar 
      {
         background-color: '''+ progress_bar_bckgrnd_clr +''';
         color: '''+ progress_bar_txt_clr +''';
         border-style: none;
         border-radius: 10px;
         text-align: center;
         font-size: 30px;
      } 
      QProgressBar::chunk 
      {      
         border-radius: 10px;
         background-color: qlineargradient(spread:pad x1:0, x2:1, y1:0.511364, y2:0.523, stop:0 '''+ progress_bar_clr_1 +''', stop:1 '''+ progress_bar_clr_2 +''');
      }
      QMessageBox{
         background-color: '''+ background_clr +''';
         color:'''+ button_font_clr +''';
         font-size: 15px;
      }
      '''
